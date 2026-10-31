"""Đánh giá chất lượng tìm kiếm TF-IDF độc lập trên kho dữ liệu 50 FAQ Tuần 4."""
import argparse
import importlib.util
import json
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("faq_lambda", ROOT / "backend/lambda_function.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def evaluate(data_file: Path, eval_file: Path, out_file: Path, threshold: float = 0.60):
    faqs = app.validate_faqs(json.loads(data_file.read_text(encoding="utf-8-sig")))
    cases = json.loads(eval_file.read_text(encoding="utf-8-sig"))
    
    print(f"Tổng số FAQ: {len(faqs)}")
    print(f"Tổng số ca kiểm thử: {len(cases)} (dev={sum(1 for c in cases if c.get('split')=='dev')}, test={sum(1 for c in cases if c.get('split')=='test')})")
    
    # 1. Kiểm tra tính nhất quán và exact match cho toàn bộ FAQ
    exact_count = sum(app.search_faq(f["question"], faqs)[0]["id"] == f["id"] for f in faqs)
    print(f"Exact question top-1 consistency: {exact_count}/{len(faqs)}")
    
    # 2. Chạy đánh giá từng ca
    results = []
    passed_total = 0
    fp_total = 0
    fn_total = 0
    wm_total = 0
    
    thresholds_to_test = [0.30, 0.45, threshold, 0.70]
    thresh_summaries = {}
    
    for t in thresholds_to_test:
        p = fp = fn = wm = 0
        split_cases = cases
        for case in split_cases:
            best, score = app.search_faq(case["question"], faqs)
            predicted = best["id"] if score >= t else None
            expected = case["expectedFaqId"]
            ok = (predicted == expected)
            if ok:
                p += 1
            elif expected is None and predicted is not None:
                fp += 1
            elif expected is not None and predicted is None:
                fn += 1
            else:
                wm += 1
        thresh_summaries[f"{t:.2f}"] = {
            "threshold": t,
            "total": len(split_cases),
            "passed": p,
            "accuracy": round(p / len(split_cases), 4),
            "falsePositive": fp,
            "falseNegative": fn,
            "wrongMatch": wm
        }
        print(f"Threshold {t:.2f}: {p}/{len(split_cases)} ({p/len(split_cases)*100:.1f}%) | FP: {fp} | FN: {fn} | WrongMatch: {wm}")

    # Chạy chi tiết cho threshold chính
    for case in cases:
        best, score = app.search_faq(case["question"], faqs)
        predicted = best["id"] if score >= threshold else None
        expected = case["expectedFaqId"]
        ok = (predicted == expected)
        if ok:
            passed_total += 1
        elif expected is None and predicted is not None:
            fp_total += 1
        elif expected is not None and predicted is None:
            fn_total += 1
        else:
            wm_total += 1
            
        row = {
            "split": case.get("split", "test"),
            "question": case["question"],
            "expectedFaqId": expected,
            "predictedFaqId": predicted,
            "score": round(score, 4),
            "threshold": threshold,
            "passed": ok,
            "matchedFaqQuestion": best["question"] if best else None
        }
        results.append(row)
        flag = "PASS" if ok else "FAIL"
        print(f"[{flag}] {case.get('split')}: '{case['question']}' -> Exp: {expected} | Got: {predicted} (Score: {score:.4f})")

    output_data = {
        "faqCount": len(faqs),
        "totalCases": len(cases),
        "selectedThreshold": threshold,
        "selectedSummary": {
            "passed": passed_total,
            "accuracy": round(passed_total / len(cases), 4),
            "falsePositive": fp_total,
            "falseNegative": fn_total,
            "wrongMatch": wm_total
        },
        "thresholdComparison": thresh_summaries,
        "details": results
    }
    
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nĐã lưu kết quả đánh giá tại: {out_file}")
    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data/faq.json")
    parser.add_argument("--eval", type=Path, default=ROOT / "data/search-eval-week4.json")
    parser.add_argument("--out", type=Path, default=ROOT / "docs/week4/search-eval-final-results.json")
    parser.add_argument("--threshold", type=float, default=0.60)
    args = parser.parse_args()
    
    evaluate(args.data, args.eval, args.out, args.threshold)
