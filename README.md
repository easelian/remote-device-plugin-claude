# Remote Device Hub for Claude

Connect Claude to your authorized Linux, macOS, and Windows devices through
Remote Device Hub (RDH) by Easelian. Use file tools, managed processes, and browser
operations according to your account access and each device's permissions.

This repository provides two ways to use the same service:

| Integration | Contents | Setup |
| --- | --- | --- |
| [Plugin](plugins/remote-device-hub/README.md) | MCP connection configuration and an operating skill | Install in Claude Code, or upload to claude.ai or Cowork; instructions are below |
| [Connector](connector/README.md) | Connection, authentication, and tool documentation | Add the MCP URL in Claude's connector settings and authorize access |

Both use `https://rdh.easelian.com/mcp`, so an account that has the Connector
and the plugin sees one set of tools. The plugin adds the operating skill; the
Connector alone supplies only the tools. The installable plugin is in
`plugins/remote-device-hub/`. The server implementation is maintained separately.

See [RDH terminology](docs/terminology.md) for the shared product, Agent, authorization and execution concepts.

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

### Claude Code

Use a Claude Code installation that supports plugins and HTTP MCP. Obtain this
repository or extract its source archive, then run from the repository root:

```bash
claude plugin marketplace add .
claude plugin install remote-device-hub@easelian-rdh --scope user
```

With access to the GitHub repository, add the marketplace as
`easelian/remote-device-plugin-claude` in place of the local path.

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

### claude.ai and Cowork

Build the plugin archive as described under [Validate and package](#validate-and-package),
or obtain `remote-device-hub-plugin-<version>.zip` from a release. In Claude, open
**Customize > Plugins > Add > Upload plugin** and select that archive. Then open
the plugin's **Connectors** tab, connect Remote Device Hub, and complete OAuth
sign-in. On Team and Enterprise plans an Owner adds the connector for the
organization before members connect their own accounts.

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

The package command creates two versioned ZIP files in `dist/`, each with a
SHA-256 file. `remote-device-hub-claude-<version>.zip` is the source archive: the
plugin, Connector documentation, and build scripts. Extract it and follow the
Claude Code steps above. `remote-device-hub-plugin-<version>.zip` holds only the
plugin folder, the layout that the claude.ai and Cowork upload accepts. These
checks validate the source and packages; OAuth and device operations require a
live account and device.

Repository text is maintained in English. Keep working notes, review preparation,
credentials, and validation output outside version control. Packaging uses an
explicit file list.

For a self-hosted service, update the plugin's `.mcp.json` and the Connector
connection reference together. Use HTTPS and configure discovery metadata,
resource URLs, and client callbacks for that service. Keep bearer tokens out of
configuration files.

License: Apache-2.0. See [LICENSE](LICENSE).
