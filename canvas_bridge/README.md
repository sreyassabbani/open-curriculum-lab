# MATH 2551 Canvas bridge

**Status: deferred experiment; no deployed service or live ChatGPT connection.**
For the plain-language account of the whole project, see the
[project review](../docs/review.md). The current review concerns lesson quality
and the practicality of supplying source files. This prototype is retained for
reference; it is not the current setup path for course members.

## Earlier proposed ChatGPT experience

The proposal was for the plugin owner to operate a shared HTTPS MCP service.
A course member would choose **Connect Canvas**, sign in to Canvas, and grant
access within their existing course permissions, without running code or
managing an API token. That sign-in flow and permission enforcement have not
been implemented. There is no working Connect Canvas option in the plugin.

## Current status

`server.py` implements local, single-token, read-only source tools for the course
outline, Topic/Lesson pages, and captions. It is **not** a public or multi-user
service and must not be exposed over HTTP or attached to a distributed plugin.
Focused tests cover topic selection, URL sanitization, and partial caption
failure; they do not establish a working live ChatGPT integration. Kaltura
captions can still require a browser-authenticated export when sessionless
retrieval fails. No production endpoint, Canvas OAuth integration, or ChatGPT
connection has been deployed.

## Requirements if this is reconsidered

The following describes unbuilt requirements, not completed features or an
approved implementation plan. Hosting ownership and institutional approval
remain unresolved. The [administrator inquiry](ADMIN_REQUEST.md) is an unsent
draft, retained as a reference.

1. Georgia Tech Canvas administrators would need to issue and enable an API developer key with the necessary read scopes. Canvas requires OAuth for applications used by multiple users. The operator's personal token used in the local prototype does not provide that shared sign-in flow.
2. The hosted service runs a user-facing Canvas authorization-code flow. It stores each consenting user’s Canvas refresh token encrypted, refreshes short-lived access tokens, and maps the resulting Canvas user to the ChatGPT connection. It checks live course access on each request. It never returns Canvas tokens, signed Kaltura URLs, or session IDs to ChatGPT.
3. ChatGPT connects to the HTTPS MCP endpoint with its supported OAuth 2.1 flow. The MCP resource server validates issuer, audience, expiry, and scopes on every request. Its authorization layer links the ChatGPT connection to the consenting Canvas user. Use an established identity provider for this layer where possible.
4. The MCP tools remain read-only and course-bounded. They return the full course outline, Topic/Lesson source pages, and complete caption status. The lesson skill uses those sources alongside OpenStax, with the actual MATH 2551 course sequence controlling scope.
5. Test with two Canvas users: one enrolled in the course and one without access. Confirm the second user cannot read course content, and that revoking the first user's Canvas authorization stops future reads. End-to-end caption retrieval and actual ChatGPT use would also need verification before any rollout.

The private OpenAI tunnel is for development and cannot provide a distributable plugin. The previous tunnel image and runner were removed from this branch.

## References

- [Canvas OAuth overview](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
- [Canvas developer keys](https://developerdocs.instructure.com/services/canvas/oauth2/file.developer_keys)
- [OpenAI plugin authentication](https://developers.openai.com/plugins/build/auth)
- [OpenAI MCP server setup](https://developers.openai.com/plugins/build/mcp-server)
