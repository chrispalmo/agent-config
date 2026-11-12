# Design collection

Three independently usable skills for exploring interface choices, sourcing device frames, and applying the default visual style or an explicit style choice. Collection membership does not require using all three.

| Skill | Use it when | Result |
| --- | --- | --- |
| [design-tool](design-tool/SKILL.md) | The user explicitly invokes design-tool to compare and refine design directions in a running application. | A temporary chooser, the selected product implementation, and removal of experiment-owned code. |
| [device-frames](device-frames/SKILL.md) | Show content inside a named phone/tablet or correct an inaccurate device outline. | A sourced frame with checked model geometry, content placement, and provenance. |
| [neon-neo-brutalist-minimal](neon-neo-brutalist-minimal/SKILL.md) | Visual work uses the default style, or the user selects it by name or reference. | Guidance for typography, color, interaction, and deliberate light and dark themes. |

Design-tool can compare proposals using the chosen style when that fits the request. It also works with other established visual systems; the style skill can guide ordinary design work without a chooser. Existing project and user direction governs each task.

## Install

```bash
./scripts/install.sh --skills --package design --cursor --claude --agents
```

This installs all three skills and their supporting resources. Installed names are `design-tool`, `device-frames`, and `neon-neo-brutalist-minimal`.
