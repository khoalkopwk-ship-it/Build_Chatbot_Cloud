"""Smoke test HTTP API trên URL do SV cung cấp. Không cần AWS CLI hoặc boto3."""
import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def run(base_url, origin, out):
    results = []
    cases = [
        ("health", "GET", "/health", None, 200, "health"),
        ("exact-FAQ017", "POST", "/chat", {"question": "Nhóm được sử dụng những Region nào?"}, 200, "FAQ017"),
        ("no-accents", "POST", "/chat", {"question": "nhom duoc su dung nhung region nao"}, 200, "FAQ017"),
        ("unmatched", "POST", "/chat", {"question": "Hôm nay trời mưa không?"}, 200, "unmatched"),
        ("empty", "POST", "/chat", {"question": "   "}, 400, None),
        ("missing", "POST", "/chat", {}, 400, None),
        ("number", "POST", "/chat", {"question": 123}, 400, None),
        ("array", "POST", "/chat", [], 400, None),
        ("too-long", "POST", "/chat", {"question": "a" * 501}, 400, None),
        ("bad-json", "POST", "/chat", "{", 400, None),
        ("too-large", "POST", "/chat", " " * 4097, 413, None),
        ("unknown-route", "GET", "/does-not-exist", None, 404, None),
    ]
    for name, method, path, body, expected, semantic in cases:
        raw = None if body is None else (body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)).encode("utf-8")
        req = urllib.request.Request(base_url.rstrip("/") + path, data=raw, method=method,
                                     headers={"Content-Type": "application/json", "Origin": origin})
        started = time.perf_counter()
        status = None
        payload = {}
        error = None
        try:
            try:
                response = urllib.request.urlopen(req, timeout=20)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                status = response.code
                text = response.read().decode("utf-8")
                payload = json.loads(text) if text else {}
        except Exception as exc:
            error = str(exc)
        ok = status == expected and not error
        if semantic == "health":
            ok = ok and payload.get("status") == "ok" and payload.get("build") == "week3-v1"
        elif semantic in ("FAQ017", "unmatched"):
            ok = ok and payload.get("logSaved") is True and bool(payload.get("requestId"))
            if semantic == "FAQ017":
                ok = ok and payload.get("matchedFaqId") == "FAQ017" and payload.get("matched") is True
            else:
                ok = ok and payload.get("matched") is False and payload.get("matchedFaqId") is None
        row = dict(case=name, timestamp=datetime.now(timezone.utc).isoformat(),
                   expectedStatus=expected, status=status, passed=bool(ok),
                   durationMs=round((time.perf_counter() - started) * 1000, 2),
                   requestId=payload.get("requestId"), apiRequestId=payload.get("apiRequestId"),
                   payload=payload, error=error)
        results.append(row)
        print(f"{'PASS' if ok else 'FAIL'} {name}: HTTP {status}; requestId={row['requestId']}")
        time.sleep(0.35)
    # Kiểm tra preflight bằng HTTP, sau đó vẫn phải kiểm tra trong trình duyệt.
    req = urllib.request.Request(base_url.rstrip("/") + "/chat", method="OPTIONS", headers={
        "Origin": origin, "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            allowed_methods = {v.strip().upper() for v in headers.get("access-control-allow-methods", "").split(",")}
            allowed_headers = {v.strip().lower() for v in headers.get("access-control-allow-headers", "").split(",")}
            ok = (response.code in (200, 204) and headers.get("access-control-allow-origin") == origin
                  and "POST" in allowed_methods and "content-type" in allowed_headers)
            row = dict(case="cors-preflight", status=response.code, passed=ok, headers=headers)
    except Exception as exc:
        row = dict(case="cors-preflight", passed=False, error=str(exc))
    results.append(row)
    print(f"{'PASS' if row['passed'] else 'FAIL'} cors-preflight")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"baseUrl": base_url, "origin": origin,
                              "runAt": datetime.now(timezone.utc).isoformat(), "results": results},
                             ensure_ascii=False, indent=2), encoding="utf-8")
    return all(r["passed"] for r in results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--out", type=Path, default=Path("docs/week3-api-results.json"))
    args = parser.parse_args()
    parsed = urllib.parse.urlsplit(args.base_url)
    if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in ("localhost", "127.0.0.1")):
        parser.error("Dùng HTTPS API Gateway hoặc HTTP localhost để test nội bộ")
    raise SystemExit(0 if run(args.base_url, args.origin, args.out) else 1)
