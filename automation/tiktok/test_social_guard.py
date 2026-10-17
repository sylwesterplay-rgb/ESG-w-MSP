"""Offline policy tests: no API calls and no account mutations."""
import unittest
from social_guard import SecurityGateError, assert_tiktok_target, assert_tiktok_queue, TIKTOK, ORG, TIKTOK_LINK


def good():
    return {"id": TIKTOK, "organizationId": ORG, "name": "esg360.academy", "service": "tiktok", "type": "account", "externalLink": TIKTOK_LINK, "isDisconnected": False, "isLocked": False}

class GuardTests(unittest.TestCase):
    def test_allow_exact(self): self.assertTrue(assert_tiktok_target([good()]))
    def test_wrong_id(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_target([good()], "6acd3857778b240e2febc3c2")
    def test_missing(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_target([])
    def test_duplicated(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_target([good(), good()])
    def test_org(self): self._reject("organizationId", "another")
    def test_name(self): self._reject("name", "bazgranie_noca")
    def test_service(self): self._reject("service", "instagram")
    def test_type(self): self._reject("type", "profile")
    def test_link(self): self._reject("externalLink", "https://tiktok.com/@bazgranie_noca")
    def test_disconnected(self): self._reject("isDisconnected", True)
    def test_locked(self): self._reject("isLocked", True)
    def test_unknown_field(self):
        d=good(); del d["type"]
        with self.assertRaises(SecurityGateError): assert_tiktok_target([d])
    def test_null_inventory(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_target(None)
    def test_queue_valid(self): self.assertTrue(assert_tiktok_queue([{"id":"abc", "channelId":TIKTOK}]))
    def test_queue_wrong_channel(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_queue([{"id":"abc", "channelId":"other"}])
    def test_queue_duplicate_id(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_queue([{"id":"abc", "channelId":TIKTOK},{"id":"abc", "channelId":TIKTOK}])
    def test_queue_missing_id(self):
        with self.assertRaises(SecurityGateError): assert_tiktok_queue([{"channelId":TIKTOK}])
    def _reject(self, field, value):
        d=good(); d[field]=value
        with self.assertRaises(SecurityGateError): assert_tiktok_target([d])

if __name__ == '__main__': unittest.main()
