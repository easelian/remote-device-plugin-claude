# Remote Device Hub Connector

Connect Claude to devices you own or are authorized to administer through
Easelian Remote Device Hub (RDH). The remote MCP service supplies device discovery,
file operations, managed processes, and browser tools. The companion
[Plugin](../plugins/remote-device-hub/README.md) adds operating instructions for
the same service. Its MCP configuration uses the same URL as this Connector, so
an account that has both sees one set of tools.

## Before connecting

Sign in at [RDH](https://rdh.easelian.com/), install the Agent using the service's
installation instructions, and approve pairing under the same account. RDH
supports Linux, macOS, and Windows Agents. Individual features depend on the
Agent version, host environment, account access, and configured permissions.
Browser operations require browser access to be enabled explicitly.

Claude must allow remote connectors for your account and organization. Keep a
small, non-sensitive sample file on an authorized device for the first read.

## Connect from Claude

1. Open **Settings → Connectors** in Claude and add a custom connector.
2. Use the name **Remote Device Hub** and URL `https://rdh.easelian.com/mcp`.
3. Complete OAuth sign-in with the RDH account that owns the paired devices.
4. Ask: “List my authorized devices and show which ones are online.”
5. Select a returned device, ask for its roots and permissions, then read the
   sample file using the root and relative path you chose.

An empty device list is a valid result: check the RDH account and Agent pairing.
An offline device or disabled capability is not permission to switch targets or
enable access. The first successful read establishes that particular account,
device, and operation; it does not validate every tool.

Claude Code users can load the Plugin using the [repository instructions](../README.md).
Use `/mcp` there for authentication. Check existing RDH connections before adding
another, especially when they use different accounts.

## Public connection details

| Setting | Value |
| --- | --- |
| MCP transport | Streamable HTTP over HTTPS |
| MCP URL / OAuth resource | `https://rdh.easelian.com/mcp` |
| Protected-resource metadata | `https://rdh.easelian.com/.well-known/oauth-protected-resource/mcp` |
| Authorization server | `https://auth.easelian.com/` |
| Authorization-server metadata | `https://auth.easelian.com/.well-known/oauth-authorization-server` |
| Authentication | OAuth authorization code, Dynamic Client Registration, PKCE S256 |
| Device-control scope | `devices:control` |
| Claude hosted callback | `https://claude.ai/api/mcp/auth_callback` |

[connection.json](connection.json) records these public values for maintainers;
it is a repository reference file, not a Claude import manifest. Read endpoint
URLs from discovery metadata rather than hard-coding token or registration URLs.
No preassigned client ID, client secret, or bearer token belongs in this repository.

For service operators, allow Claude's exact hosted callback in the authorization
server. An explicit redirect allowlist overrides the server defaults, so retain
existing client callbacks when adding Claude. Claude Code also requires
`allow_loopback_redirects: true` for its local HTTP callback on a dynamic port,
using `localhost` or `127.0.0.1`. Test both hosted and local callbacks after
deployment. MCP authorization uses `devices:control`,
not the website's `openid email` scopes. Metadata discovery alone does not prove
callback acceptance, login, token refresh, or successful tool execution.
See [Claude's authentication requirements](https://claude.com/docs/connectors/building/authentication).

## Tools, permissions, and troubleshooting

[Tools and permissions](tools.md) describes the available tool families and
limits. The live server's `tools/list` and the selected device's `device_info`
are authoritative. A Connector does not install the companion Plugin's Skill.

- If OAuth fails, reconnect through Claude's connection settings. Do not copy
  tokens into chat or retry an uncertain refresh-token exchange manually.
- For `invalid_redirect_uri`, the service operator must check the exact callback
  against the authorization server's configuration.
- If a file edit conflicts, reread the file and use its current whole-file hash.
- If a change times out, query its receipt, job, or browser session before any
  retry; a timeout does not establish that nothing happened.
- For quota or capability errors, report the actual result. Use
  `get_billing_status` for account allowance details; it does not purchase access.

Send the error code and `support_id` to [Easelian support](https://easelian.com/contact).
Exclude secrets and unrelated device content from support messages.

[Privacy](https://easelian.com/privacy) · [Terms](https://easelian.com/terms) ·
[Data handling](../docs/data-handling.md)
