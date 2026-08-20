---
name: agents-md-canonical
description: Use AGENTS.md as canonical cross-agent project guidance with a Claude shim
alwaysApply: true
---

# Cross-Agent Project Guidance

When setting up or writing project agent rules, put shared guidance in `AGENTS.md`.

Always create `CLAUDE.md` as a Claude Code compatibility shim containing only:

```markdown
@AGENTS.md
```

Keep instructions vendor-neutral. Do not create vendor-specific rule trees such as `.cursor/rules/` or `.claude/rules/` unless the user explicitly asks for them.
