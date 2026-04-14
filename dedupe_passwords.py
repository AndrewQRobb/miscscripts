#!/usr/bin/env python3
"""
dedupe_passwords.py

Compares a LastPass CSV export against an Apple Passwords CSV export and
outputs only the entries from LastPass that are NOT already in Apple Passwords.

Conflict resolution (same URL + username, different password):
  - If Apple's password is a known-deprecated password → LastPass wins automatically
  - Otherwise → interactive prompt lets you pick Apple, LastPass, or skip

Usage:
    python3 dedupe_passwords.py lastpass_export.csv apple_passwords.csv [options]

Options:
    --discard EMAIL      Discard all entries with this username/email (repeatable)
    --deprecated PASS    Add a known-deprecated password to the auto-resolve list (repeatable)
    --dry-run            Print summary counts without writing output files or prompting
"""

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Known-deprecated passwords — if Apple's stored password matches one of these,
# the LastPass version is assumed to be newer and wins automatically.
# ---------------------------------------------------------------------------
DEPRECATED_PASSWORDS = {
    "Vthokie9!",
    "vthokie9",
    "Vthokie10!",
    "HokieHi09!",
}

# ---------------------------------------------------------------------------
# Column name constants
# ---------------------------------------------------------------------------
LP_URL   = "url"
LP_USER  = "username"
LP_PASS  = "password"
LP_TOTP  = "totp"
LP_EXTRA = "extra"
LP_NAME  = "name"

AP_TITLE = "Title"
AP_URL   = "URL"
AP_USER  = "Username"
AP_PASS  = "Password"
AP_NOTES = "Notes"
AP_OTP   = "OTPAuth"

APPLE_FIELDNAMES = [AP_TITLE, AP_URL, AP_USER, AP_PASS, AP_NOTES, AP_OTP]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_url(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "https://" + raw
    try:
        parsed = urlparse(raw)
        host = (parsed.hostname or "").removeprefix("www.")
        path = parsed.path.rstrip("/")
        return (host + path).lower()
    except Exception:
        return raw.lower()


def url_user_key(url: str, username: str) -> tuple:
    return (normalize_url(url), username.strip().lower())


def title_user_key(title: str, username: str) -> tuple:
    return (title.strip().lower(), username.strip().lower())


def lp_to_apple(row: dict) -> dict:
    return {
        AP_TITLE: row.get(LP_NAME, "").strip() or row.get(LP_URL, "").strip(),
        AP_URL:   row.get(LP_URL, "").strip(),
        AP_USER:  row.get(LP_USER, "").strip(),
        AP_PASS:  row.get(LP_PASS, "").strip(),
        AP_NOTES: row.get(LP_EXTRA, "").strip(),
        AP_OTP:   row.get(LP_TOTP, "").strip(),
    }


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def prompt_conflict(index: int, total: int, ap_row: dict, lp_row: dict) -> str:
    """
    Show a side-by-side conflict prompt and return 'a', 'l', or 's'.
    """
    site  = ap_row.get(AP_URL) or ap_row.get(AP_TITLE) or "(no URL)"
    user  = ap_row.get(AP_USER, "")
    ap_pw = ap_row.get(AP_PASS, "")
    lp_pw = lp_row.get(LP_PASS, "").strip()

    print(f"\n{'─'*56}")
    print(f"CONFLICT {index} of {total}: {site}  /  {user}")
    print(f"{'─'*56}")
    print(f"  [a] Apple    : {ap_pw}")
    print(f"  [l] LastPass : {lp_pw}")
    print(f"  [s] Skip     : discard this entry entirely")

    while True:
        choice = input("Keep which version? [a/l/s]: ").strip().lower()
        if choice in ("a", "l", "s"):
            return choice
        print("      Please enter a, l, or s.")


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deduplicate LastPass CSV against Apple Passwords CSV"
    )
    parser.add_argument("lastpass_csv",  type=Path)
    parser.add_argument("apple_csv",     type=Path)
    parser.add_argument(
        "--discard", metavar="EMAIL", action="append", default=[],
        help="Discard all entries with this username/email (repeatable)"
    )
    parser.add_argument(
        "--deprecated", metavar="PASSWORD", action="append", default=[],
        help="Additional known-deprecated password; if Apple has it, LastPass wins (repeatable)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print counts only — no output files, no interactive prompts"
    )
    args = parser.parse_args()

    for f in (args.lastpass_csv, args.apple_csv):
        if not f.exists():
            print(f"Error: file not found: {f}")
            sys.exit(1)

    deprecated = DEPRECATED_PASSWORDS | set(args.deprecated)
    discard_users = {e.strip().lower() for e in args.discard}
    out_dir = Path(__file__).parent

    # --- Load ---
    lp_rows = read_csv(args.lastpass_csv)
    ap_rows = read_csv(args.apple_csv)
    print(f"Loaded {len(lp_rows)} LastPass entries, {len(ap_rows)} Apple Passwords entries")

    # --- Apply discard-username filter ---
    def should_discard(username: str) -> bool:
        return username.strip().lower() in discard_users

    lp_discarded = sum(1 for r in lp_rows if should_discard(r.get(LP_USER, "")))
    ap_discarded = sum(1 for r in ap_rows if should_discard(r.get(AP_USER, "")))
    lp_rows = [r for r in lp_rows if not should_discard(r.get(LP_USER, ""))]
    ap_rows = [r for r in ap_rows if not should_discard(r.get(AP_USER, ""))]

    if discard_users:
        print(f"  Discarded {lp_discarded} LastPass + {ap_discarded} Apple entries "
              f"matching: {', '.join(args.discard)}")

    # --- Build Apple lookup ---
    apple_by_url_user:   dict[tuple, dict] = {}
    apple_by_title_user: dict[tuple, dict] = {}
    for row in ap_rows:
        uk = normalize_url(row.get(AP_URL, ""))
        user = row.get(AP_USER, "")
        if uk:
            apple_by_url_user[url_user_key(row.get(AP_URL, ""), user)] = row
        else:
            apple_by_title_user[title_user_key(row.get(AP_TITLE, ""), user)] = row

    # --- Dedupe LastPass internally ---
    lp_seen: set[tuple] = set()
    lp_deduped: list[dict] = []
    lp_internal_dupes = 0
    for row in lp_rows:
        uk = normalize_url(row.get(LP_URL, ""))
        user = row.get(LP_USER, "")
        key = url_user_key(row.get(LP_URL, ""), user) if uk else title_user_key(row.get(LP_NAME, ""), user)
        if key in lp_seen:
            lp_internal_dupes += 1
            continue
        lp_seen.add(key)
        lp_deduped.append(row)

    # --- Identify conflicts up front (needed for "X of Y" counter) ---
    # A conflict = same URL+user, different password, Apple NOT deprecated
    pending_conflicts: list[tuple[dict, dict]] = []  # (ap_row, lp_row)

    pre_new:      list[dict] = []  # net-new LastPass entries (no Apple match)
    auto_lp_wins: list[dict] = []  # Apple had deprecated password → LastPass wins
    exact_matches = 0

    for lp_row in lp_deduped:
        uk   = normalize_url(lp_row.get(LP_URL, ""))
        user = lp_row.get(LP_USER, "").strip()
        key  = url_user_key(lp_row.get(LP_URL, ""), user) if uk else title_user_key(lp_row.get(LP_NAME, ""), user)

        apple_row = (apple_by_url_user if uk else apple_by_title_user).get(key)

        if apple_row is None:
            pre_new.append(lp_row)
        else:
            ap_pw = apple_row.get(AP_PASS, "").strip()
            lp_pw = lp_row.get(LP_PASS, "").strip()
            if ap_pw == lp_pw:
                exact_matches += 1
            elif ap_pw in deprecated:
                auto_lp_wins.append(lp_row)
            else:
                pending_conflicts.append((apple_row, lp_row))

    # --- Dry run: just print counts and exit ---
    if args.dry_run:
        print(f"\n{'='*40}")
        print("DRY RUN — no files written")
        print(f"{'='*40}")
        print(f"  Net-new from LastPass:            {len(pre_new)}")
        print(f"  Exact matches (already in Apple): {exact_matches}")
        print(f"  Auto-resolved (deprecated pw):    {len(auto_lp_wins)}  → LastPass wins")
        print(f"  Interactive conflicts pending:     {len(pending_conflicts)}")
        if discard_users:
            print(f"  Discarded (username filter):      {lp_discarded + ap_discarded}")
        return

    # --- Resolve conflicts interactively ---
    interactive_lp:   list[dict] = []  # user chose LastPass
    interactive_ap:   list[dict] = []  # user chose Apple — nothing to import
    interactive_skip: list[dict] = []  # user chose to discard both

    for i, (ap_row, lp_row) in enumerate(pending_conflicts, 1):
        choice = prompt_conflict(i, len(pending_conflicts), ap_row, lp_row)
        if choice == "l":
            interactive_lp.append(lp_row)
        elif choice == "a":
            interactive_ap.append(ap_row)
        else:
            interactive_skip.append(lp_row)

    print()

    # --- Assemble final output ---
    new_entries = (
        [lp_to_apple(r) for r in pre_new]
        + [lp_to_apple(r) for r in auto_lp_wins]
        + [lp_to_apple(r) for r in interactive_lp]
    )

    # conflicts.csv: auto-resolved (deprecated) + interactive choices — for audit
    conflict_rows: list[dict] = []
    for lp_row in auto_lp_wins:
        uk   = normalize_url(lp_row.get(LP_URL, ""))
        user = lp_row.get(LP_USER, "").strip()
        key  = url_user_key(lp_row.get(LP_URL, ""), user) if uk else title_user_key(lp_row.get(LP_NAME, ""), user)
        ap_row = (apple_by_url_user if uk else apple_by_title_user).get(key, {})
        conflict_rows.append({"Resolution": "LastPass (deprecated Apple pw)", AP_URL: lp_row.get(LP_URL,""), AP_USER: user, "Apple_Password": ap_row.get(AP_PASS,""), "LastPass_Password": lp_row.get(LP_PASS,"")})

    for ap_row, lp_row in pending_conflicts:
        user = lp_row.get(LP_USER, "").strip()
        resolution = (
            "LastPass (you chose)" if lp_row in interactive_lp
            else "Apple (you chose)" if ap_row in interactive_ap
            else "Skipped (you discarded both)"
        )
        conflict_rows.append({"Resolution": resolution, AP_URL: ap_row.get(AP_URL,""), AP_USER: user, "Apple_Password": ap_row.get(AP_PASS,""), "LastPass_Password": lp_row.get(LP_PASS,"")})

    # --- Write outputs ---
    new_path      = out_dir / "lastpass_new_entries.csv"
    conflict_path = out_dir / "conflicts.csv"
    summary_path  = out_dir / "summary.txt"

    write_csv(new_path, APPLE_FIELDNAMES, new_entries)
    write_csv(conflict_path, ["Resolution", AP_URL, AP_USER, "Apple_Password", "LastPass_Password"], conflict_rows)

    summary = (
        f"Password Deduplication Summary\n"
        f"{'='*42}\n"
        f"LastPass entries loaded:              {len(lp_rows) + lp_discarded}\n"
        f"Apple Passwords entries loaded:       {len(ap_rows) + ap_discarded}\n"
    )
    if discard_users:
        summary += (
            f"  Discarded (username filter):        {lp_discarded} LP + {ap_discarded} Apple\n"
        )
    summary += (
        f"  LastPass internal duplicates:       {lp_internal_dupes}\n"
        f"\n"
        f"Results:\n"
        f"  Already in Apple (exact match):     {exact_matches}\n"
        f"  Net-new from LastPass:              {len(pre_new)}\n"
        f"  Auto-resolved (deprecated Apple pw):{len(auto_lp_wins)}  → LastPass used\n"
        f"  Interactive — you chose LastPass:   {len(interactive_lp)}\n"
        f"  Interactive — you chose Apple:      {len(interactive_ap)}\n"
        f"  Interactive — skipped (discarded):  {len(interactive_skip)}\n"
        f"\n"
        f"  TOTAL entries to import:            {len(new_entries)}\n"
        f"\n"
        f"Output files (in {out_dir}):\n"
        f"  {new_path.name}  ← import into Apple Passwords\n"
        f"  {conflict_path.name}               ← audit log of all conflicts\n"
        f"\n"
        f"Next steps:\n"
        f"  1. Review counts above — do they look right?\n"
        f"  2. Apple Passwords > Settings > ... > Import\n"
        f"     Select: {new_path.name}\n"
        f"  3. Verify a few logins before deleting LastPass\n"
    )

    summary_path.write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
