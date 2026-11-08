# Data handling

Remote Device Hub operates on devices explicitly enrolled in the user's account.
The plugin supplies connection configuration and operating instructions; the
host Claude app manages its credentials. The following describes the integration's
data paths. The published [Privacy Notice](https://easelian.com/privacy) and
[Terms of Use](https://easelian.com/terms) govern the service.

| Data | Purpose and recipients |
| --- | --- |
| Account and device identifiers | RDH associates the OAuth grant and device with the account, authorizes requests, and reports device availability |
| File paths and requested file contents | Claude sends task parameters through RDH to the Agent; requested results return through RDH to Claude |
| Commands, process input, and output | The Agent executes authorized commands with its OS account's permissions; requested output and status return to Claude |
| Browser URLs, page text, and screenshots | The Agent browser contacts the selected website; requested observations return through RDH to Claude |
| Browser uploads and downloads | Approved uploads disclose the selected file to the selected site; downloads and approval actions use authenticated RDH pages |
| Browser profile data | An explicitly selected persistent profile retains browser state on the device; closing its session does not remove the profile |
| Call and operation status | Identifiers, execution state, errors, and limited result summaries support recovery and accountability |

RDH does not need the user's entire conversation or Claude memory to carry out
these operations. The plugin includes no local credential reader, telemetry
script, or additional MCP endpoint. Task results can contain personal or
confidential data selected by the user. Authorized browser and command actions
can also send data to external services.

Claude processes the data it receives under the terms applicable to the user's
Claude account. Avoid unnecessary secrets in files, commands, screenshots, and
support messages.

## Retention and deletion

Account authorization, device records, audits, operation summaries, process
buffers, browser profiles, and browser artifacts have separate lifetimes.
For retention details or account-data deletion, consult the published
[Privacy Notice](https://easelian.com/privacy) or contact
[Easelian support](https://easelian.com/contact).

Closing a browser session, deleting a named profile, deleting a browser artifact,
and deleting an account are distinct operations. Closing a session does not
remove every retained record.
