"""Unit tests có mock S3/DynamoDB; KHÔNG phải minh chứng chạy AWS."""
import base64
import contextlib
import importlib.util
import io
import json
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("faq_lambda", ROOT / "backend/lambda_function.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
FAQS = json.loads((ROOT / "data/faq.json").read_text(encoding="utf-8-sig"))


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"FAQ_BUCKET": "test-data", "FAQ_KEY": "faq.json",
                             "LOG_TABLE": "test-logs", "SIMILARITY_THRESHOLD": "0.30"})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.s3 = SimpleNamespace(get_object=lambda **kw: {
            "Body": io.BytesIO(json.dumps(FAQS).encode()), "ETag": '"test-etag"'})
        self.items = []
        self.table = SimpleNamespace(put_item=lambda **kw: self.items.append(kw["Item"]))
        p1 = patch.object(app, "get_s3", return_value=self.s3)
        p2 = patch.object(app, "get_table", return_value=self.table)
        p1.start(); p2.start()
        self.addCleanup(p1.stop); self.addCleanup(p2.stop)

    def call(self, raw=None, method="POST", path="/chat", **extra):
        e = dict(version="2.0", rawPath=path,
                 headers={"content-type": "application/json"},
                 requestContext={"requestId": "api-test", "http": {"method": method}},
                 body=raw if raw is not None else json.dumps({"question": FAQS[16]["question"]}))
        e.update(extra)
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            r = app.lambda_handler(e, SimpleNamespace(aws_request_id="lambda-test"))
        self.last_log = json.loads(stream.getvalue().splitlines()[-1])
        return r["statusCode"], json.loads(r["body"])

    def test_success_and_correlation(self):
        status, body = self.call()
        self.assertEqual(status, 200)
        self.assertEqual(body["matchedFaqId"], "FAQ017")
        self.assertTrue(body["logSaved"])
        self.assertEqual(body["requestId"], self.items[0]["requestId"])
        self.assertEqual(body["apiRequestId"], self.last_log["apiRequestId"])
        self.assertNotIn("question", self.last_log)
        self.assertEqual(body["faqCount"], 24)

    def test_health_does_not_access_dependencies(self):
        with patch.object(app, "get_s3", side_effect=AssertionError("must not call")):
            self.assertEqual(self.call(method="GET", path="/health")[1]["status"], "ok")
        self.assertEqual(len(self.items), 0)

    def test_invalid_bodies(self):
        for raw in ('{', 'null', '[]', '{}', '{"question":null}', '{"question":22}', '{"question":"  "}'):
            with self.subTest(raw=raw):
                self.assertEqual(self.call(raw)[0], 400)
        self.assertEqual(self.items, [])

    def test_501_characters(self):
        self.assertEqual(self.call(json.dumps({"question": "a" * 501}))[0], 400)

    def test_body_byte_limit_and_content_type(self):
        self.assertEqual(self.call(" " * 4097)[0], 413)
        self.assertEqual(self.call(headers={"Content-Type": "text/plain"})[0], 415)

    def test_base64(self):
        raw = base64.b64encode(json.dumps({"question": FAQS[16]["question"]}).encode()).decode()
        self.assertEqual(self.call(raw, isBase64Encoded=True)[0], 200)
        self.assertEqual(self.call("%%%", isBase64Encoded=True)[0], 400)

    def test_unmatched_saved(self):
        status, body = self.call(json.dumps({"question": "Hôm nay trời mưa không?"}))
        self.assertEqual(status, 200)
        self.assertFalse(body["matched"])
        self.assertIsNone(body["matchedFaqId"])
        self.assertEqual(self.items[0]["matchedFaqId"], "NONE")

    def test_s3_failure(self):
        with patch.object(app, "get_s3", side_effect=RuntimeError("private-detail")):
            status, body = self.call()
        self.assertEqual(status, 500)
        self.assertNotIn("private-detail", str(body))
        self.assertEqual(self.last_log["applicationError"], 1)

    def test_ddb_failure_keeps_answer_but_emits_application_error(self):
        with patch.object(app, "get_table", side_effect=RuntimeError("denied")):
            status, body = self.call()
        self.assertEqual(status, 200)
        self.assertFalse(body["logSaved"])
        self.assertEqual(self.last_log["applicationError"], 1)
        self.assertEqual(self.last_log["errorStage"], "dynamodb")

    def test_direct_old_event_is_rejected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = app.lambda_handler({"question": "test"}, None)
        self.assertEqual(result["statusCode"], 404)

    def test_faq_validation(self):
        for bad in ([], {}, [None], [{"id": "x"}], [FAQS[0], FAQS[0]]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                app.validate_faqs(bad)

    def test_invalid_threshold_and_wrong_key(self):
        for threshold in ("nan", "0", "1.5", "oops"):
            with patch.dict(os.environ, {"SIMILARITY_THRESHOLD": threshold}):
                self.assertEqual(self.call()[0], 500)
        def read_key(**kw):
            self.assertEqual(kw["Key"], "faq/faq.json")
            return {"Body": io.BytesIO(json.dumps(FAQS).encode())}
        with patch.dict(os.environ, {"FAQ_KEY": "faq/faq.json"}):
            self.s3.get_object = read_key
            self.assertEqual(self.call()[0], 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
