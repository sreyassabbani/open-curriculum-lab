# Deferred draft: Georgia Tech Canvas access inquiry

**Not sent. Live integration work is deferred.** This is a historical draft,
not a current request to obtain approval or credentials. Start with the
[project review](../docs/review.md) for the current status and review questions.
The proposed shared service, sign-in flow, and hosting arrangements below have
not been implemented. These endpoint scopes describe the prototype; they are
not an approved production authorization design.

This is a draft for the plugin operator to send to the Georgia Tech Digital Learning Team at [canvas@gatech.edu](mailto:canvas@gatech.edu). Do not send a personal Canvas API token or a client secret in email. This is an initial feasibility question; the service URL and OAuth redirect URI can be supplied after the host is chosen.

**Subject:** Read-only Canvas OAuth developer key for MATH 2551 study assistant

Hello Digital Learning Team,

I am developing a read-only ChatGPT study assistant for members who already have access to MATH 2551 in Georgia Tech Canvas (course 588672). The assistant would let each person sign in with their own Canvas account and retrieve only the course materials that account can view. It would read course module order, Topic and Lesson pages, and video captions, then use those sources alongside the assigned OpenStax textbook to draft or review study lessons. It would not read grades, submissions, rosters, or messages, and it would not write to Canvas. Course pages and caption text selected by a user would be sent to ChatGPT/OpenAI as tool results; Canvas credentials and Kaltura session URLs would stay on the bridge.

Would Georgia Tech consider issuing and enabling a scoped **Canvas API OAuth developer key** for this external application? Canvas documentation says multi-user applications must obtain each user’s token through OAuth, rather than asking users to generate personal API tokens. Please let me know the request process, review requirements for this kind of external application, and any restrictions on sending course pages or Kaltura captions to ChatGPT. This is an external API integration, not an LTI tool installed in Canvas; please advise if a different review route applies.

The current prototype calls only these Canvas GET endpoints and would request these scopes:

```text
url:GET|/api/v1/courses/:id
url:GET|/api/v1/courses/:course_id/modules
url:GET|/api/v1/courses/:course_id/modules/:module_id/items
url:GET|/api/v1/courses/:course_id/pages
url:GET|/api/v1/courses/:course_id/pages/:url_or_id
url:GET|/api/v1/courses/:course_id/external_tools/sessionless_launch
```

The final service would require each person to consent through Canvas and would check their access to the course on every request. I can provide the application URL, redirect URI, data retention details, and security design for review before a key is issued.

Thank you,
[Name]

## Sources checked

- [Georgia Tech Digital Learning Team contact](https://sites.gatech.edu/dlt-blog/2026/08/19/prepare-for-a-new-term-your-canvas-kickstart-guide/)
- [Canvas OAuth and multi-user token policy](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
- [Canvas API developer key scopes](https://developerdocs.instructure.com/services/canvas/oauth2/file.developer_keys)
- [Canvas courses API](https://developerdocs.instructure.com/services/canvas/resources/courses)
- [Canvas modules API](https://developerdocs.instructure.com/services/canvas/resources/modules)
- [Canvas pages API](https://developerdocs.instructure.com/services/canvas/resources/pages)
- [Canvas external tools API](https://developerdocs.instructure.com/services/canvas/resources/external_tools)
