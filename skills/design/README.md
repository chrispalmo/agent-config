# Design collection

Two independently usable skills for exploring interface choices and applying a selected visual style. Collection membership does not require using both.

| Skill | Use it when | Result |
| --- | --- | --- |
| [design-tool](design-tool/SKILL.md) | The user wants to compare and refine design directions in a running application. | A temporary chooser, the selected product implementation, and removal of experiment-owned code. |
| [neon-neo-brutalist-minimal](neon-neo-brutalist-minimal/SKILL.md) | The user selects this visual style by name or reference. | Guidance for typography, color, interaction, and deliberate light and dark themes. |

Design-tool can compare proposals using the chosen style when that fits the request. It also works with other established visual systems; the style skill can guide ordinary design work without a chooser. Existing project and user direction governs each task.

## Install

```bash
./scripts/install.sh --skills --package design --cursor --claude --agents
```

This installs both skills and their supporting resources. Installed names remain `design-tool` and `neon-neo-brutalist-minimal`.
