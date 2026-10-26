# Browser collection

| Skill | Purpose |
| --- | --- |
| [browser-session](browser-session/SKILL.md) | Register agent-created browser tabs, renew activity, and retain tabs needed for human action. |
| [browser-cleanup](browser-cleanup/SKILL.md) | Clean up eligible registered tabs using current browser evidence and the shared local registry. |

The [registry helper](browser-session/scripts/registry.py) manages records; it has no browser access. The collection uses the harness's supported browser tools and preserves tabs whose ownership or eligibility is unclear. Runtime state is local and is never committed.

```bash
./scripts/install.sh --skills --package browser --cursor --claude --agents
```

Installed names stay `browser-session` and `browser-cleanup`. Moving source folders does not move or reset the browser-session registry.
