# Git Sync Guide - Keeping Local and GitHub in Sync

A practical guide for managing your local repositories and keeping them synchronized with GitHub.

---

## Understanding the Workflow

```
Local Changes → Stage → Commit → Push → GitHub
     ↓            ↓        ↓        ↓        ↓
  (edit files)  (git add)  (save)  (upload)  (remote)
```

**Key concept:** Local and GitHub are **separate** until you `git push`.

---

## Daily Workflow (Recommended)

### When You Make Changes

```bash
# 1. Navigate to project
cd /Users/andrewrobb/Coding\ Projects/kcookmeyer_website

# 2. Make your changes (edit files, add images, etc.)

# 3. Check what changed
git status

# 4. Stage all changes
git add .

# 5. Commit with descriptive message
git commit -m "Added new landscape photos to portfolio"

# 6. Push to GitHub
git push
```

**That's it!** Your changes are now on GitHub.

---

## Using Helper Scripts (Even Easier)

I've created scripts to simplify this:

```bash
# For kcookmeyer_website:
./deploy.sh  # Does steps 4-6 above, asks for commit message

# For other repos:
./push-to-github.sh  # Similar helper
```

**What the script does:**
1. Checks for changes
2. Asks you for a commit message
3. Commits everything
4. Pushes to GitHub
5. Confirms success

---

## Checking Sync Status

### See if you need to push:

```bash
git status
```

**Output examples:**

```bash
# ✅ Everything in sync
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean

# ⚠️ You have local changes not committed
On branch main
Changes not staged for commit:
  modified:   data/portfolio.json

# ⚠️ You have commits not pushed
On branch main
Your branch is ahead of 'origin/main' by 2 commits.
  (use "git push" to publish your local commits)
```

### See what's different:

```bash
git diff  # See changes in files (before staging)
git log --oneline -5  # See last 5 commits
```

---

## Common Scenarios

### Scenario 1: Made changes, forgot to push

```bash
git status  # Shows unpushed commits
git push    # Upload to GitHub
```

### Scenario 2: Not sure if I'm in sync

```bash
git status  # Check status
git log origin/main..HEAD  # See unpushed commits (if any)
```

### Scenario 3: Multiple repos to sync

```bash
cd /Users/andrewrobb/Coding\ Projects

# Check each repo
for repo in instascraper kcookmeyer_website network_diag SecurityTools office_cleanup; do
    cd "$repo"
    echo "=== $repo ==="
    git status
    cd ..
done
```

### Scenario 4: Made changes in GitHub web interface

```bash
# Pull changes from GitHub to local
git pull

# Now local is up to date with GitHub
```

---

## Automatic Reminders (Installed!)

I've set up a **post-commit hook** for kcookmeyer_website that reminds you to push after committing:

```bash
git commit -m "Updated photos"

# You'll see:
# ✅ Commit successful!
# 📤 You have 1 unpushed commit(s)
#
# 💡 To push to GitHub, run:
#    git push
```

---

## Best Practices

### ✅ DO:
- **Commit often** - Small, focused commits with clear messages
- **Push regularly** - At least once per day
- **Check status** - Run `git status` before and after work
- **Use descriptive messages** - "Added new portfolio images" not "updates"
- **Pull before you start** - `git pull` to get latest from GitHub

### ❌ DON'T:
- **Don't wait weeks to push** - Risk losing work if computer crashes
- **Don't commit broken code** - Test before committing
- **Don't use vague messages** - "fixes" or "stuff" are unhelpful
- **Don't forget to push** - Use the reminder hook or `./deploy.sh`

---

## Commit Message Best Practices

**Good commit messages:**
```
✅ "Add 5 new landscape photos to portfolio"
✅ "Update bio text and contact email"
✅ "Fix lightbox keyboard navigation bug"
✅ "Update dependencies to latest versions"
```

**Bad commit messages:**
```
❌ "updates"
❌ "changes"
❌ "fix stuff"
❌ "asdfasdf"
```

---

## Setting Up Automatic Sync (Optional)

If you want **truly automatic** syncing, I can set up:

### Option A: Auto-push on commit
Every commit automatically pushes to GitHub (no manual `git push` needed)

### Option B: Scheduled sync
Every hour, automatically commit and push any changes

### Option C: Watch mode
Watches for file changes and auto-commits/pushes immediately

**Trade-offs:**
- ✅ Never forget to sync
- ❌ Creates many small commits
- ❌ Less control over what gets committed
- ❌ Can accidentally push broken code

**My recommendation:** Stick with manual workflow or use `./deploy.sh` helper script.

---

## Multiple Computers (Bonus)

If you work on multiple computers:

**Computer A (make changes):**
```bash
git add .
git commit -m "Changes on laptop"
git push
```

**Computer B (get changes):**
```bash
git pull  # Downloads changes from GitHub
```

---

## Visualizing Your Git Status

```bash
# See a nice graph of commits
git log --oneline --graph --all --decorate

# See what's in each commit
git log -p -2  # Last 2 commits with diffs

# See commits not yet on GitHub
git log origin/main..HEAD
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Check status | `git status` |
| Stage all changes | `git add .` |
| Commit changes | `git commit -m "message"` |
| Push to GitHub | `git push` |
| Pull from GitHub | `git pull` |
| See unpushed commits | `git log origin/main..HEAD` |
| See what changed | `git diff` |
| Use helper script | `./deploy.sh` |

---

## Troubleshooting

### "Your branch is behind 'origin/main'"
Someone (or you on another computer) made changes on GitHub.

**Fix:**
```bash
git pull  # Get changes from GitHub
```

### "Merge conflict"
You and GitHub have different versions of the same file.

**Fix:**
```bash
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "Resolved merge conflict"
git push
```

### "Failed to push"
Usually means you need to pull first.

**Fix:**
```bash
git pull
git push
```

### "Detached HEAD state"
You're not on a branch.

**Fix:**
```bash
git checkout main  # Get back to main branch
```

---

## Summary

**Simple workflow:**
1. Make changes
2. `git add .`
3. `git commit -m "description"`
4. `git push`

**Even simpler:**
1. Make changes
2. `./deploy.sh`

**Check sync:**
- `git status` (do this often!)

**Golden rule:** Push at least once per day to avoid losing work.
