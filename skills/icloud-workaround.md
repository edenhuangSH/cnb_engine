---
name: icloud-workaround
description: Handle iCloud "Optimize Mac Storage" evicting files written by tools
type: skill
---

## When to Use
When working in iCloud-synced directories (~/Documents on macOS with iCloud Drive enabled).

## The Problem
macOS iCloud Drive's "Optimize Mac Storage" feature can evict files from local disk, replacing them with cloud-only stubs. Files written by tools (Write, Agent) may appear to exist (Read works, full path works) but `ls` shows empty directories and `cp`/`cat` from relative paths fail.

## Key Patterns
- Write tool creates files at the iCloud path but they may be immediately evicted
- `find` with full path can locate evicted files
- `Read` tool can access evicted files (triggers iCloud download)
- `cp` with FULL path (not relative) can copy evicted files
- Bash `cat > file << 'EOF'` bypasses iCloud issues (creates local file directly)
- `git add`/`git mv` may fail on evicted files

## Workarounds
1. **Use Bash heredoc** instead of Write tool: `cat > file.py << 'PYEOF' ... PYEOF`
2. **Copy via full path**: `cp "/full/iCloud/path/file" ./local_copy`
3. **Store important files in git-tracked directories** — git objects persist locally
4. **Keep skills/configs in project root**, not in ~/Documents/claude/

## Checklist
- [ ] After Write tool, verify file exists with `ls -la`
- [ ] If missing, re-create with Bash heredoc
- [ ] For critical files, always commit to git immediately
- [ ] Store reusable config in project root, not iCloud-managed paths
