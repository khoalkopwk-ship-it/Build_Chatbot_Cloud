"""Offline: kiểm tra dữ liệu, exact questions, dev hoặc test. Không cần boto3."""
import argparse
import importlib.util
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("faq_lambda", ROOT / "backend/lambda_function.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
parser = argparse.ArgumentParser()
parser.add_argument("--split", choices=["dev", "test"], default="dev")
parser.add_argument("--threshold", type=float)
args = parser.parse_args()
if args.split == "test" and args.threshold is None:
    parser.error("Chốt ngưỡng từ tập dev rồi truyền --threshold khi chạy test")
thresholds = [args.threshold] if args.threshold is not None else [0.30, 0.45, 0.60, 0.70]
if any(not 0 < t <= 1 for t in thresholds):
    parser.error("Ngưỡng phải thuộc (0, 1]")
faqs = app.validate_faqs(json.loads((ROOT / "data/faq.json").read_text(encoding="utf-8-sig")))
cases = json.loads((ROOT / "data/search-eval.json").read_text(encoding="utf-8-sig"))
for faq in faqs:
    assert faq.get("source", "").strip(), "Cần ghi nguồn cho từng FAQ"
    assert all(unicodedata.is_normalized("NFC", faq[field]) for field in ("question", "answer")), "Cần chuẩn hóa NFC"
exact = sum(app.search_faq(f["question"], faqs)[0]["id"] == f["id"] for f in faqs)
print(f"FAQ={len(faqs)}; exact-question top1={exact}/{len(faqs)} (chỉ kiểm tra nhất quán)")
rows = []
for threshold in thresholds:
    passed = false_positive = false_negative = wrong_match = 0
    for case in [c for c in cases if c["split"] == args.split]:
        best, score = app.search_faq(case["question"], faqs)
        predicted = best["id"] if score >= threshold else None
        expected = case["expectedFaqId"]
        ok = predicted == expected
        passed += int(ok)
        false_positive += int(expected is None and predicted is not None)
        false_negative += int(expected is not None and predicted is None)
        wrong_match += int(expected is not None and predicted is not None and predicted != expected)
        rows.append(dict(threshold=threshold, **case,
                         predictedFaqId=predicted, score=round(score, 4), passed=ok))
        print(f"{threshold:.2f} {'PASS' if ok else 'FAIL'} expected={expected} actual={predicted} score={score:.4f}: {case['question']}")
    total = sum(c["split"] == args.split for c in cases)
    print(f"SUMMARY threshold={threshold:.2f}: correct={passed}/{total}; falsePositive={false_positive}; falseNegative={false_negative}; wrongMatch={wrong_match}")
out = ROOT / "docs" / f"search-eval-{args.split}-results.json"
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved: {out}")
# Đây là phép đo chất lượng; FAIL phải được phân tích, không sửa nhãn để làm đẹp.
