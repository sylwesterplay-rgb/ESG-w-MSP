# ACC-SOCIAL-GUARD-01 — ESG360 publication isolation

Status: **enforced for the GitHub TikTok Autopilot in `automation/tiktok/publish.py` only**.
Effective after the guarded code was committed to `main`; NOT a provider-wide Buffer/Metricool permission restriction.

## Only allowed write target

- Provider: Buffer.
- Organization: `6acd37f788a9ef6b52a7a556`.
- Channel: `6ad1dedb778b240e2f269549`.
- Service/type/name: `tiktok / account / esg360.academy`.
- External URL: `https://tiktok.com/@esg360.academy`.
- The connection must not be disconnected or locked.

`social_guard.py` checks all these properties on a fresh read; a mismatch or missing response stops the run. `publish.py` rejects any other target at the actual scheduling function, including the personal LinkedIn profile, the ESG360 LinkedIn company page, and TikTok Bazgranie Nocą.

## LinkedIn and Metricool

- **Automatic TikTok-to-LinkedIn cross-posting is disabled** in this scheduler, even on Tuesdays, Thursdays and Saturdays.
- No existing Buffer or Metricool post has been deleted, rescheduled, duplicated or migrated.
- Mixed Metricool brand `7358175` (`bazgranie_noca`) contains the ESG360 LinkedIn organization `urn:li:organization:145302737`; this scheduler does not write to Metricool.
- The company LinkedIn schedule already in Metricool continues unchanged. Before migrating any future content, read both providers' queues and check all statuses; the last known pending entry is 2026-11-09.
- Future Buffer LinkedIn automation requires a separate, approved implementation that checks a dedicated LinkedIn allowlist **and both** the Metricool and Buffer queues. Do not re-enable the legacy cross-post code.

## Fail-closed practices

- Buffer TikTok posts must be fully retrieved; if more than 100 entries exist, stop pending pagination support.
- Abort when the returned queue has missing/duplicate IDs or a post from another channel.
- Treat equal captions or an occupied posting slot as a collision irrespective of post status, requiring manual investigation rather than automatically repeating a failed/ambiguous post.
- Verify a new post by ID, channel, UTC schedule, `scheduled` status, and `automatic` scheduling type.
- The Buffer API currently provides no proven idempotency key for `createPost`. An unresolved timeout may require manual reconciliation and durable intent storage before absolute at-most-once semantics can be claimed.
- Buffer `sent` or Metricool `PUBLISHED` is not independent proof that a post is publicly viewable.

## Verification and scope

- Offline guard test suite: `python -m unittest discover -s automation/tiktok -p 'test_social_guard.py' -v`.
- The scheduled workflow runs these checks before the publishing step.
- This is **not** a blanket access-control layer for ChatGPT tools, external publishing clients, Metricool UI, Buffer UI, or Airtable, and does not alter their permissions. These require separate integration-specific controls.
- Rollback: revert the guard-related Git commits after a security review; do not restore unapproved LinkedIn cross-posts automatically.

No passwords, API keys, user data or secrets are stored in this file.
