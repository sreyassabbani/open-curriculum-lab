# MATH 2551 Canvas bridge

## Intended ChatGPT experience

The plugin owner operates one HTTPS MCP service. A course member opens the plugin in ChatGPT Chat, chooses **Connect Canvas**, signs in through Georgia Tech Canvas, and approves read access. They do not need GitHub, Python, a server, or an API token. Every tool call uses that member’s own Canvas authorization and is limited by their course permissions. A person without course access cannot obtain the live course content through this bridge.

## Current status

`server.py` is a local, single-token, read-only source prototype. It is **not** a public or multi-user service and must not be exposed over HTTP or attached to a distributed plugin. It demonstrates course outline, Topic/Lesson page, and caption retrieval. Kaltura captions can still require a browser-authenticated export when sessionless retrieval fails; the tool reports that explicitly. No production endpoint, Canvas OAuth integration, or ChatGPT connection has been deployed.

## Production connection

1. Georgia Tech Canvas administrators issue and enable an API developer key for this application with only the read scopes the source tools need. Canvas requires OAuth for applications used by multiple users; personal access tokens are for local testing only.
2. The hosted service runs a user-facing Canvas authorization-code flow. It stores each consenting user’s Canvas refresh token encrypted, refreshes short-lived access tokens, and maps the resulting Canvas user to the ChatGPT connection. It checks live course access on each request. It never returns Canvas tokens, signed Kaltura URLs, or session IDs to ChatGPT.
3. ChatGPT connects to the HTTPS MCP endpoint with its supported OAuth 2.1 flow. The MCP resource server validates issuer, audience, expiry, and scopes on every request. Its authorization layer links the ChatGPT connection to the consenting Canvas user. Use an established identity provider for this layer where possible.
4. The MCP tools remain read-only and course-bounded. They return the full course outline, Topic/Lesson source pages, and complete caption status. The lesson skill uses those sources alongside OpenStax, with the actual MATH 2551 course sequence controlling scope.
5. Test with two Canvas users: one enrolled in the course and one without access. Confirm the second user cannot read course content, and that revoking the first user’s Canvas authorization stops future reads. Only then connect and publish the plugin.

The private OpenAI tunnel is for development and cannot provide a distributable plugin. The previous tunnel image and runner were removed from this branch.

## References

- [Canvas OAuth overview](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
- [Canvas developer keys](https://developerdocs.instructure.com/services/canvas/oauth2/file.developer_keys)
- [OpenAI plugin authentication](https://developers.openai.com/plugins/build/auth)
- [OpenAI MCP server setup](https://developers.openai.com/plugins/build/mcp-server)
