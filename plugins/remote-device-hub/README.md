# Remote Device Hub

![Remote Device Hub icon](assets/icon.png)

Use Claude with your authorized Linux, macOS, and Windows devices through
Easelian Remote Device Hub (RDH). This plugin connects to RDH and provides a
skill for reading and editing files, running managed processes, inspecting
webpages, and recovering from uncertain operation results.

An RDH account and an enrolled, approved Agent are required. Each device's
permissions determine the available operations. Browser tasks also require
browser access to be enabled for the account and Agent.

## Install and connect

For a local Claude Code installation, obtain this repository or its source ZIP.
From the repository root, which contains `.claude-plugin/marketplace.json`, run:

```bash
claude plugin marketplace add .
claude plugin install remote-device-hub@easelian-rdh --scope user
```

Restart Claude Code, confirm the plugin is enabled in `/plugin`, then select its
Remote Device Hub entry in `/mcp` and complete OAuth sign-in. For a single-session
trial, run `claude --plugin-dir ./plugins/remote-device-hub` from the repository
root instead. The local marketplace and single-session methods are alternatives.

In another supported Claude app, use its plugin and connector settings. Component
support varies by app; successful installation does not establish that OAuth or
device operations work there.

The MCP URL is `https://rdh.easelian.com/mcp`. If RDH is also configured separately
as a Connector, check which connection and account you are using before operating
a device. Claude manages OAuth credentials; the plugin contains none.

## Example tasks

In Claude Code, invoke `/remote-device-hub:remote-device-operations` with a task,
or describe your task naturally:

- List my authorized devices and show which ones are online.
- On my selected device, show its file roots and read the README I specify.
- Create a new test file in the selected root, then read it back to verify it.
- Run an approved diagnostic command and report its output and exit status.
- Open a specified webpage on a browser-enabled device and inspect the page.

The skill starts with `list_devices` and `device_info`. It uses current file
hashes before editing, tracks process and browser session IDs, and checks receipts
after uncertain changes instead of blindly repeating them.

## Permissions and data

File tools use configured roots. Shell commands run with the Agent OS account's
permissions and are not confined by those roots. Browser actions can send data to
the selected website. Use only devices, files, commands, and websites you are
authorized to access. Claude's approval controls and RDH permission checks apply.

Requests and results pass through RDH to the selected Agent. Results supplied to
Claude can include device information, file contents, process output, webpage
text, or screenshots. Browser uploads require explicit human approval. Enter
passwords and complete human-only steps on the returned RDH page, not in chat.
Named browser profiles retain browser state until separately removed; closing a
session does not delete a named profile.

## Privacy Policy and support

Read the [Easelian Privacy Notice](https://easelian.com/privacy) and
[Terms of Use](https://easelian.com/terms). Claude also processes data under the
terms applicable to your Claude account. Contact
[Easelian support](https://easelian.com/contact) for service, privacy, or security
questions; include an error code and `support_id` where available, never tokens
or passwords. Manage your account and devices at [RDH](https://rdh.easelian.com/).

Publisher: [Easelian](https://easelian.com/). License: Apache-2.0.
