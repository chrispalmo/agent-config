# Cloud agent bootstrap

This is the human setup guide for getting this repo onto **Cursor Cloud Agents**, **Claude Code cloud sessions**, and **Codex Cloud**.

Cloud agents do not see your laptop. They never look for `install.sh` on this machine. You paste a short stub into each vendor **environment** once. The vendor runs that stub on a fresh VM **before** the agent starts. Later sessions from a phone or another computer use the same stored environment.

Do not paste `scripts/install.sh` or `scripts/cloud/bootstrap.sh` into a dashboard. Point at them with the stub below.

## What the stub does

```bash
set -euo pipefail
DEST="${HOME}/.agent-config"
if [ -d "${DEST}/.git" ]; then
  git -C "${DEST}" pull --ff-only
else
  git clone --depth 1 https://github.com/chrispalmo/agent-config.git "${DEST}"
fi
exec "${DEST}/scripts/cloud/bootstrap.sh"
```

That clone is public HTTPS, so the VM does not need a GitHub token.

`bootstrap.sh` then:

1. Updates the checkout if it can.
2. Runs `./scripts/install.sh --cursor --claude --agents`.
3. On Cursor cloud VMs (Linux, workspace at `/workspace`), links `/.cursor` to `~/.cursor` so Cursor can find generated user rules. Cursor walks up from `/workspace` and never reaches `~/.cursor` without that link.

The stub is idempotent. Cursor reruns the install script on every Build; a second `git clone` into the same directory would fail.

## After you change skills or rules

Push to `main` on [chrispalmo/agent-config](https://github.com/chrispalmo/agent-config). Then:

- **Cursor:** trigger a new environment Build (edit and save the install script, or start a Build from the environment page).
- **Claude:** edit the setup script (a no-op comment is enough) or wait for cache expiry, which is about seven days. The next **new** session rebuilds. Resumed sessions do not rerun the setup script.
- **Codex:** save the environment again, or reset the environment cache, then start a new cloud task.

## Verify

In a **new** cloud session, ask:

> Without reading files, are personal rules from chrispalmo/agent-config installed? Call me by name in this reply, and say whether you would write that name into a project file.

You want: it calls you Chris, and it refuses to write that name into project files.

On the VM you can also check:

```bash
test -f ~/.claude/rules/address-as-chris.md && echo claude-rules-ok
test -f ~/.codex/AGENTS.md && grep -F 'managed-by: chrispalmo/agent-config' ~/.codex/AGENTS.md
readlink ~/.codex/skills/design-tool/SKILL.md
```

Cursor cloud should also have `/.cursor` pointing at `~/.cursor`.

## Cursor Cloud Agents

Official overview: [Cloud environment setup](https://cursor.com/docs/cloud-agent/setup).

Prefer a **personal saved environment** on the dashboard. Do not add `.cursor/environment.json` to every project unless you want this bootstrap in that repo's Builds.

1. Open [cursor.com/dashboard/cloud-agents](https://cursor.com/dashboard/cloud-agents). You can also start guided setup from the Agents Window in the Cursor desktop app.
2. Connect GitHub (or GitLab / Azure DevOps / Bitbucket) if Cursor has not already connected it. This is so the agent can clone **the repo you are working on**. The agent-config clone in the stub is public HTTPS and does not need that connection.
3. Create an environment, or open an existing personal environment you use for most cloud agents.
4. Find the **install script** field. Cursor used to call this the update script. In `.cursor/environment.json` the same field is `install`.
5. Paste the stub from [What the stub does](#what-the-stub-does). Keep any repo-specific install commands you still need (`pnpm install`, and so on). Put those **after** the stub, or run them first and then `exec` only if this stub is the last thing. If you already `exec` the bootstrap, nothing after that line runs. Safer pattern when the repo also needs its own install:

   ```bash
   set -euo pipefail
   DEST="${HOME}/.agent-config"
   if [ -d "${DEST}/.git" ]; then
     git -C "${DEST}" pull --ff-only
   else
     git clone --depth 1 https://github.com/chrispalmo/agent-config.git "${DEST}"
   fi
   "${DEST}/scripts/cloud/bootstrap.sh"
   # repo-specific commands, for example:
   # pnpm install
   ```

6. Save. Cursor runs the install script while creating a **Build**, not when you type a prompt. Wait until the Build succeeds.
7. Start a cloud agent on any repo that uses this environment. Confirm with the [Verify](#verify) prompt.
8. If skills install but Cursor rules do not, the `/.cursor` symlink failed. Check the Build log for `could not create /.cursor`.

Resolution order if a repo has its own `.cursor/environment.json`: that file wins over your personal environment. In that case, put the stub in that repo's `install` field, or remove the file so the personal environment applies.

Do **not** put this bootstrap in `start` or `terminals`. Those run at agent start for live processes, not for installing files.

## Claude Code cloud (web and mobile)

Official overview: [Configure cloud environments](https://code.claude.com/docs/en/cloud-environments).

The same environment is used from [claude.ai/code](https://claude.ai/code), the Claude mobile Code tab, `claude --cloud`, and the Desktop app. **Remote Control** is your laptop and already sees local `~/.claude`. Do not use this stub for Remote Control.

1. Finish Claude Code on the web onboarding so you have at least the Default environment.
2. Open [claude.ai/code](https://claude.ai/code).
3. In the row above the message box, select the **cloud icon** that shows the current environment name. There is no separate settings URL for this selector.
4. Do **not** put the stub on **Default**. Default has no setup script. Select **Add cloud environment**, or hover an existing non-Default environment and open its settings icon.
5. Name it something you will recognize (for example `agent-config`).
6. Network access: **Trusted** is enough for a public `git clone` from GitHub and for common package registries. If clone fails with a network error, switch to **Custom** and allow `github.com`.
7. Leave environment variables empty for this bootstrap. Do not put secrets here.
8. Paste the stub from [What the stub does](#what-the-stub-does) into **Setup script**.
9. Save. Select this environment in the selector so web and mobile sessions use it.
10. From the CLI, run `/remote-env` and pick the same environment if you start cloud sessions with `claude --cloud`.
11. Start a **new** cloud session (not a resume). The setup script runs before Claude Code launches, then Anthropic snapshots the disk. Confirm with the [Verify](#verify) prompt.

If the setup script exits non-zero, the session fails to start. Keep the stub as written; it already uses `set -e`.

## Codex Cloud

Official overview: [Cloud environments](https://developers.openai.com/codex/cloud/environments).

1. Open Codex Cloud in the browser ([chatgpt.com/codex](https://chatgpt.com/codex)) and connect GitHub if you have not already.
2. Open environment settings for the environment you use for cloud tasks (create one if needed, bound to the repo you will work on).
3. Find the **setup script** field. Codex runs it after it clones **that** repo, with internet available, before the agent loop. Secrets in the environment are available to this script only; they are removed before the agent phase.
4. Paste the stub from [What the stub does](#what-the-stub-does).
5. Do not rely on `export` in the stub for later agent commands. This stub writes files under `$HOME`, which persist in the container snapshot.
6. Save. If Codex is using a cached container, change the setup script or reset the cache so the stub actually runs.
7. Start a new cloud task. Confirm with the [Verify](#verify) prompt.

Agent internet access is off by default during the task. That does not block this bootstrap: the setup phase has network. The clone happens then, not while the agent is working.

## What not to do

- Do not expect laptop `~/.cursor`, `~/.claude`, or `~/.codex` to appear on a cloud VM.
- Do not attach a second private repo for this bootstrap. `agent-config` is public.
- Do not use Claude Remote Control as a substitute for the Claude setup script.
- Do not commit this stub into other people's repositories unless you intend every clone of that repo to install your personal skills and rules.
