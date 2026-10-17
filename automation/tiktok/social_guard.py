"""ACC-SOCIAL-GUARD-01. Pure fail-closed guard for ESG360 GitHub Autopilot.

Controls this scheduler, not Buffer/Metricool users or other API clients.
"""

POLICY_ID = "ACC-SOCIAL-GUARD-01"
ORG = "6acd37f788a9ef6b52a7a556"
TIKTOK = "6ad1dedb778b240e2f269549"
TIKTOK_NAME = "esg360.academy"
TIKTOK_LINK = "https://tiktok.com/@esg360.academy"


class SecurityGateError(RuntimeError):
    pass


def assert_tiktok_target(channels, target_id=TIKTOK):
    """Require a unique, live, exact ESG360 TikTok account before a write."""
    if target_id != TIKTOK:
        raise SecurityGateError("DENY: target not on ESG360 TikTok allowlist")
    if not isinstance(channels, list):
        raise SecurityGateError("DENY: invalid channel inventory")
    matches = [item for item in channels if isinstance(item, dict) and item.get("id") == target_id]
    if len(matches) != 1:
        raise SecurityGateError("DENY: missing/ambiguous TikTok channel")
    item = matches[0]
    required = {
        "id": TIKTOK,
        "organizationId": ORG,
        "name": TIKTOK_NAME,
        "service": "tiktok",
        "type": "account",
        "externalLink": TIKTOK_LINK,
        "isDisconnected": False,
        "isLocked": False,
    }
    for key, wanted in required.items():
        if key not in item or type(item[key]) is not type(wanted) or item[key] != wanted:
            raise SecurityGateError("DENY: TikTok identity mismatch on " + key)
    return True


def assert_tiktok_queue(posts, target_id=TIKTOK):
    """Only accept complete lists of records belonging to the expected channel."""
    if target_id != TIKTOK or not isinstance(posts, list):
        raise SecurityGateError("DENY: invalid queue target or result")
    seen = set()
    for item in posts:
        if not isinstance(item, dict) or not item.get("id") or item.get("channelId") != TIKTOK:
            raise SecurityGateError("DENY: mixed or incomplete Buffer queue")
        if item["id"] in seen:
            raise SecurityGateError("DENY: repeated post ID in Buffer queue")
        seen.add(item["id"])
    return True
