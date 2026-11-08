# Tools and permissions

The Connector discovers tools from the live MCP server. This guide groups the
public tool names by task; it is not an executable schema or a promise that every
device enables every tool. Read the current schemas and call `device_info` for
the selected device before operating it.

Each row below groups several MCP tools; the Connector itself is the single MCP
service. Every advertised tool has its own title, description, input schema,
and permission hints. Tools that change state carry `destructiveHint: true`,
including creating a directory, starting a managed search, or reserving an
operation receipt. These hints support client confirmation and do not replace
account authorization or device permissions.

| Task | Tools | Behavior and limits |
| --- | --- | --- |
| Discover devices | `list_devices`, `device_info` | Account-scoped devices, roots, permissions, and capabilities; an empty list is valid |
| Browse files | `list_directory`, `file_info`, `read_file`, `read_file_chunk`, `read_multiple_files` | Named roots and relative paths; bounded reads and pagination |
| Search files | `search_files`, `start_search`, `get_search_results`, `list_searches`, `stop_search` | Literal search or managed asynchronous search; preserve task IDs and offsets |
| Change files | `write_file`, `edit_file`, `make_directory`, `move_file` | Write permission, create-only checks, current whole-file hashes for edits, destination checks for moves |
| Run processes | `start_process`, `read_process`, `list_processes`, `write_process_stdin`, `terminate_process` | Shell permission; explicit job IDs; verify output and terminal status |
| Inspect browser state | `browser_sessions`, `browser_tabs`, `browser_observe`, `browser_screenshot`, `browser_wait`, `browser_files`, `browser_profiles` | Browser capability, bounded observations, screenshots, artifact and profile metadata |
| Operate a browser | `browser_open`, `browser_act`, `browser_control` | Session creation, input, human-control handoff, close, and authorized cleanup; fresh observation references and session epochs |
| Recover an operation | `prepare_operation`, `get_operation_status`, `list_operations`, `get_call_status`, `list_calls` | Reserve a supported operation ID before a change; inspect state after uncertainty without repeating it |
| Check account allowance | `get_billing_status` | Read entitlement and quota information; no checkout or payment operation |

## File and process boundaries

File paths are relative to the named roots returned by the device. A bounded
preview or chunk hash is not a whole-file hash. Creating a new file with
`write_file` uses an empty `expected_sha256` to require that the path does not
exist; replacing or editing an existing file requires its current whole-file
hash. Read back the result before reporting success.

Commands run with the Agent's operating-system account permissions. The selected
working directory and file roots do not confine shell commands. A denied file
operation must not be bypassed through a command. Track the `job_id` returned by
`start_process`; a job ID alone is not evidence of completion. The file tool set
does not include a general delete-file tool.

## Browser boundaries

Browser operations require account access and an enabled, usable Agent browser.
`browser_open` normally creates an isolated temporary profile, separate from the
user's daily browser. A named persistent profile is opt-in and retains state;
closing its session does not delete the profile.

Observe the page before acting and use the current references and session epoch.
Screenshots contain the current viewport and can include sensitive page data.
For login or another human step, use the returned authenticated `human_url`.
Passwords must not be sent through AI tool input. Human control pauses AI input
until the user hands the session back.

Uploads require the user's approval on the returned files page and a one-use
grant for the selected site. Selecting a file can itself disclose it to that
site. Downloads use the authenticated `files_url`; the model must not invent
download links. Browser cleanup actions can delete retained data and require
authorization for the specific session, profile, or artifact.

## Uncertain results

Reserve an operation receipt for supported important changes. After a lost
response, use the original operation, call, process, or session identifier to
check what happened. Receipts contain status and limited summaries, not a full
copy of every output. An `unknown` result must remain unknown until independent
inspection establishes the outcome. Never blindly replay a command, page
submission, or one-use upload grant.
