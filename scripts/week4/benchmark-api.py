"""Benchmark script đo hiệu năng và độ trễ HTTP của API Gateway và Lambda Tuần 4."""
import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


BENCHMARK_PROMPTS = [
    {"type": "exact-lambda", "question": "AWS Lambda là gì?"},
    {"type": "exact-region", "question": "Nhóm được sử dụng những Region nào?"},
    {"type": "exact-attendance", "question": "Môn học có bắt buộc điểm danh không?"},
    {"type": "paraphrase-lambda", "question": "định nghĩa lambda serverless aws"},
    {"type": "paraphrase-region", "question": "khu vuc aws nao duoc dung cho bai lab"},
    {"type": "out-of-scope", "question": "Hôm nay thời tiết thế nào?"},
    {"type": "out-of-scope-crypto", "question": "Giá bitcoin hôm nay tăng hay giảm?"},
    {"type": "empty-input", "question": "   "},
]


def run_benchmark(base_url: str, count: int, interval: float, out_path: Path):
    print(f"Bắt đầu benchmark API Gateway -> Lambda tại: {base_url}")
    print(f"Tổng số mẫu đo: {count}, khoảng cách giữa các request: {interval}s")
    
    results = []
    latencies = []
    
    # 1. Warm-up ping /health
    health_url = base_url.rstrip("/") + "/health"
    try:
        t0 = time.perf_counter()
        req = urllib.request.Request(health_url, method="GET")
        with urllib.request.urlopen(req, timeout=15) as res:
            t_health = (time.perf_counter() - t0) * 1000
            print(f"[WARMUP] GET /health - Status {res.code} - {t_health:.2f} ms")
    except Exception as e:
        print(f"[WARMUP WARNING] GET /health thất bại: {e}")

    # 2. Benchmark loop
    chat_url = base_url.rstrip("/") + "/chat"
    for i in range(count):
        prompt_info = BENCHMARK_PROMPTS[i % len(BENCHMARK_PROMPTS)]
        body_dict = {"question": prompt_info["question"]}
        raw_body = json.dumps(body_dict, ensure_ascii=False).encode("utf-8")
        
        req = urllib.request.Request(
            chat_url,
            data=raw_body,
            method="POST",
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
        started = time.perf_counter()
        status = None
        payload = {}
        error = None
        
        try:
            try:
                response = urllib.request.urlopen(req, timeout=25)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                status = response.code
                text = response.read().decode("utf-8", errors="replace")
                payload = json.loads(text) if text else {}
        except Exception as exc:
            error = str(exc)
            
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        latencies.append(duration_ms)
        
        row = {
            "index": i + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "queryType": prompt_info["type"],
            "question": prompt_info["question"],
            "status": status,
            "durationMs": duration_ms,
            "matched": payload.get("matched"),
            "matchedFaqId": payload.get("matchedFaqId"),
            "similarity": payload.get("similarity"),
            "faqCount": payload.get("faqCount"),
            "logSaved": payload.get("logSaved"),
            "requestId": payload.get("requestId"),
            "apiRequestId": payload.get("apiRequestId"),
            "error": error
        }
        results.append(row)
        
        print(f"[{i+1}/{count}] HTTP {status} | {duration_ms:7.2f} ms | Q: {prompt_info['question'][:30]}... -> FAQ: {row['matchedFaqId']} (sim: {row['similarity']})")
        time.sleep(interval)

    # 3. Tính toán thống kê
    sorted_latencies = sorted(latencies)
    n = len(latencies)
    stats = {
        "count": n,
        "successCount": sum(1 for r in results if r["status"] in (200, 400)),
        "http200Count": sum(1 for r in results if r["status"] == 200),
        "http400Count": sum(1 for r in results if r["status"] == 400),
        "minMs": round(min(latencies), 2) if latencies else 0,
        "maxMs": round(max(latencies), 2) if latencies else 0,
        "meanMs": round(statistics.mean(latencies), 2) if latencies else 0,
        "medianMs": round(statistics.median(latencies), 2) if latencies else 0,
        "p90Ms": round(sorted_latencies[int(n * 0.90) - 1], 2) if latencies else 0,
        "p95Ms": round(sorted_latencies[int(n * 0.95) - 1], 2) if latencies else 0,
        "stdDevMs": round(statistics.stdev(latencies), 2) if len(latencies) > 1 else 0
    }
    
    summary = {
        "baseUrl": base_url,
        "executedAt": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "results": results
    }
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== KẾT QUẢ THỐNG KÊ BENCHMARK ===")
    print(f"Số mẫu: {stats['count']} | Thành công: {stats['successCount']}")
    print(f"Min: {stats['minMs']} ms | Max: {stats['maxMs']} ms | Mean: {stats['meanMs']} ms")
    print(f"p50 (Median): {stats['medianMs']} ms | p90: {stats['p90Ms']} ms | p95: {stats['p95Ms']} ms | StdDev: {stats['stdDevMs']} ms")
    print(f"Đã lưu kết quả tại: {out_path}")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://tijvqgrltk.execute-api.us-east-1.amazonaws.com")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--interval", type=float, default=0.5)
    parser.add_argument("--out", type=Path, default=Path("docs/week4/benchmark-results.json"))
    args = parser.parse_args()
    
    run_benchmark(args.base_url, args.count, args.interval, args.out)
