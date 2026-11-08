# Remote Device Hub for Claude

Connect Claude to your authorized Linux, macOS, and Windows devices through
Easelian Remote Device Hub (RDH). Use file tools, managed processes, and browser
operations according to your account access and each device's permissions.

This repository provides two ways to use the same service:

| Integration | Contents | Setup |
| --- | --- | --- |
| [Plugin](plugins/remote-device-hub/README.md) | MCP connection configuration and an operating skill | Install in a Claude app that supports these components; Claude Code instructions are below |
| [Connector](connector/README.md) | Connection, authentication, and tool documentation | Add the MCP URL in Claude's connector settings and authorize access |

Both use `https://rdh.easelian.com/mcp`. The installable plugin is in
`plugins/remote-device-hub/`. The server implementation is maintained separately.

## Before connecting

Sign in at [RDH](https://rdh.easelian.com/), follow its Agent installation
instructions, and approve device pairing under the same account. File tools use
configured roots and permissions. Commands run with the Agent OS account's
permissions; file roots do not confine shell commands. Browser operations also
require browser access to be enabled for the account and Agent.

Claude manages OAuth sign-in and credential storage. Only connect devices you
own or are authorized to administer. Complete password entry, upload approval,
and other human steps on the pages returned by RDH.

## Install the plugin

Use a Claude Code installation that supports plugins and HTTP MCP. Obtain this
repository or extract its source archive, then run from the repository root:

```bash
claude plugin marketplace add .
claude plugin install remote-device-hub@easelian-rdh --scope user
```

Restart Claude Code, confirm the plugin is enabled in `/plugin`, then select its
Remote Device Hub entry in `/mcp` and complete OAuth sign-in.

For a single-session trial, use this command instead:

```bash
claude --plugin-dir ./plugins/remote-device-hub
```

Choose one loading method. If you already have an RDH MCP connection, check which
connection and account you intend to use. Organization policies may require an
administrator to allow the plugin or MCP service.

Start with this request:

```text
/remote-device-hub:remote-device-operations List my authorized remote devices.
```

An empty device list is a valid result. After selecting a device, ask for its
roots, permissions, and capabilities through `device_info` before starting a task.

## Connect without the plugin

In Claude, open **Settings > Connectors**, add a custom connector named
**Remote Device Hub** with URL `https://rdh.easelian.com/mcp`, and complete OAuth
sign-in. Availability depends on your Claude account and organization settings.

Ask Claude to list your authorized devices. The
[Connector guide](connector/README.md) covers setup, authentication, and
troubleshooting. A Connector supplies the tools without installing the plugin's
operating skill.

## Documentation and support

- [Connector setup and authentication](connector/README.md)
- [Tools and permissions](connector/tools.md)
- [Data handling](docs/data-handling.md)
- [Plugin instructions](plugins/remote-device-hub/README.md)

Manage your devices at [RDH](https://rdh.easelian.com/). Read the
[Privacy Notice](https://easelian.com/privacy) and
[Terms of Use](https://easelian.com/terms), or contact
[Easelian support](https://easelian.com/contact).

## Validate and package

Source checks and packaging require Python 3. Official plugin validation requires
Claude Code:

```bash
python3 scripts/check.py
claude plugin validate ./plugins/remote-device-hub
claude plugin validate .
python3 scripts/package.py
```

The package command creates a versioned ZIP and SHA-256 file in `dist/`. The
archive contains the plugin, Connector documentation, and build scripts. Extract
it and follow the installation steps above. These checks validate the source and
package; OAuth and device operations require a live account and device.

Repository text is maintained in English. Keep working notes, review preparation,
credentials, and validation output outside version control. Packaging uses an
explicit file list.

For a self-hosted service, update the plugin's `.mcp.json` and the Connector
connection reference together. Use HTTPS and configure discovery metadata,
resource URLs, and client callbacks for that service. Keep bearer tokens out of
configuration files.

License: Apache-2.0. See [LICENSE](LICENSE).
