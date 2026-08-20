# Cloud environment stub

Cloud agents never see your laptop. Paste this stub into each vendor environment once. Later sessions, including ones started from a phone, run the stored script on the VM before the agent starts.

```bash
git clone --depth 1 https://github.com/chrispalmo/agent-config.git ~/.agent-config
exec ~/.agent-config/scripts/cloud/bootstrap.sh
```

`bootstrap.sh` runs the root installer for Cursor, Claude Code, and Codex. On Cursor cloud VMs with workspaces at `/workspace`, it also links `/.cursor` to `~/.cursor` so Cursor rule discovery can find generated user rules.

## Where to paste it

- Cursor: Cloud Agents environment `install` on the Cursor dashboard.
- Claude Code: environment setup script at claude.ai/code. Claude Remote Control runs on this machine and does not need the stub.
- Codex: environment setup script in Codex settings.
