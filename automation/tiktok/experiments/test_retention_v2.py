"""Offline QA for ESG360 retention-first experiments. No social API access."""
import ast
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORYBOARDS = ROOT / "retention_v2_storyboards.json"
RENDERER = ROOT / "retention_v2.py"
IDS = {"bank-esg-3-rzeczy", "vsme-dobrowolne-klient", "faktura-energia-esg"}


class RetentionExperimentQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.episodes = json.loads(STORYBOARDS.read_text(encoding="utf-8"))

    def test_three_unique_approved_storyboards(self):
        self.assertEqual(len(self.episodes), 3)
        self.assertEqual({ep["id"] for ep in self.episodes}, IDS)

    def test_duration_and_first_frame(self):
        for ep in self.episodes:
            with self.subTest(ep=ep["id"]):
                beats = ep["beats"]
                self.assertEqual(len(beats), 5)
                self.assertEqual(sum(b["duration"] for b in beats), 14)
                self.assertEqual(beats[0]["duration"], 2)
                self.assertTrue(all(1 <= b["duration"] <= 3 for b in beats))
                self.assertTrue(beats[0]["headline"])

    def test_every_beat_has_message(self):
        for ep in self.episodes:
            with self.subTest(ep=ep["id"]):
                self.assertIn("#ESG", ep["caption"])
                self.assertIn("#ESG360Academy", ep["caption"])
                self.assertTrue(ep["title"].strip())
                for beat in ep["beats"]:
                    self.assertTrue(all(beat[k].strip() for k in ("headline", "eyebrow", "detail")))
                    self.assertLess(len(beat["detail"]), 100)

    def test_no_social_network_api_in_renderer(self):
        raw = RENDERER.read_text(encoding="utf-8")
        tree = ast.parse(raw)
        banned_modules = {"requests", "urllib", "httpx", "socket", "boto3", "cloudinary"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse({alias.name.split(".")[0] for alias in node.names} & banned_modules)
            if isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module.split(".")[0], banned_modules)
        for forbidden in ("api.buffer.com", "createPost", "BUFFER_API_KEY",
                          "CLOUDINARY_UPLOAD_PRESET", "@bazgranie_noca"):
            self.assertNotIn(forbidden, raw)

    def test_no_overlap_with_production_episode_ids(self):
        existing = json.loads((ROOT.parent/"episodes.json").read_text(encoding="utf-8"))
        self.assertTrue(IDS.isdisjoint({item["id"] for item in existing}))

    def test_full_preview_streams(self):
        """Pass with --render-dir only; tests all rendered samples and audio."""
        if not hasattr(self, "render_dir"):
            self.skipTest("Supply --render-dir DIR for MP4 codec validation")
        for ident in IDS:
            path = self.render_dir / (ident + ".mp4")
            self.assertTrue(path.exists(), f"Missing preview: {path}")
            raw = subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration:stream=codec_name,codec_type,width,height",
                 "-of", "json", str(path)], text=True)
            data = json.loads(raw)
            self.assertAlmostEqual(float(data["format"]["duration"]), 14, delta=0.08)
            streams = {s["codec_type"]: s for s in data["streams"]}
            self.assertEqual(streams["video"]["codec_name"], "h264")
            self.assertEqual((streams["video"]["width"], streams["video"]["height"]),
                             (720, 1280))
            self.assertEqual(streams["audio"]["codec_name"], "aac")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-dir", type=Path)
    args, unittest_args = parser.parse_known_args()
    if args.render_dir:
        RetentionExperimentQA.render_dir = args.render_dir
    unittest.main(argv=["test_retention_v2.py"] + unittest_args, verbosity=2)
