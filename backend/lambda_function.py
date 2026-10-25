import base64
import binascii
import json
import math
import os
import re
import time
import unicodedata
import uuid
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal

BUILD = "week3-v1"
MAX_BODY_BYTES = 4096
STOPWORDS = {
    "la", "gi", "co", "cua", "va", "cho", "toi", "minh", "ban", "ve",
    "nhung", "cac", "trong", "mot", "nhu", "the", "nao", "duoc",
    "khong", "hay", "biet", "giup", "xin", "hoi"
}
_s3 = None
_dynamodb = None


def get_s3():
    global _s3
    if _s3 is None:
        import boto3
        from botocore.config import Config
        _s3 = boto3.client("s3", config=Config(
            connect_timeout=1, read_timeout=2,
            retries={"total_max_attempts": 1}))
    return _s3


def get_table(name):
    global _dynamodb
    if _dynamodb is None:
        import boto3
        from botocore.config import Config
        _dynamodb = boto3.resource("dynamodb", config=Config(
            connect_timeout=1, read_timeout=2,
            retries={"total_max_attempts": 1}))
    return _dynamodb.Table(name)


def tokenize(text):
    text = unicodedata.normalize("NFD", str(text).lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d")
    return [w for w in re.findall(r"[a-z0-9]+", text) if w not in STOPWORDS]


def validate_faqs(faqs):
    if not isinstance(faqs, list) or not faqs:
        raise ValueError("FAQ phải là mảng không rỗng")
    seen = set()
    for faq in faqs:
        if not isinstance(faq, dict):
            raise ValueError("FAQ item phải là object")
        for field in ("id", "question", "answer"):
            if not isinstance(faq.get(field), str) or not faq[field].strip():
                raise ValueError("FAQ thiếu trường bắt buộc")
        if faq["id"] in seen:
            raise ValueError("FAQ trùng id")
        seen.add(faq["id"])
        for field in ("source", "category"):
            if field in faq and not isinstance(faq[field], str):
                raise ValueError("Sai kiểu metadata")
        if "keywords" in faq and (
            not isinstance(faq["keywords"], list)
            or any(not isinstance(w, str) for w in faq["keywords"])
        ):
            raise ValueError("keywords phải là mảng chuỗi")
    return faqs


def search_faq(question, faqs):
    if not faqs:
        return None, 0.0
    documents = [tokenize(f["question"]) for f in faqs]
    n = len(documents)
    df = Counter()
    for tokens in documents:
        df.update(set(tokens))

    def vector(tokens):
        if not tokens:
            return {}
        return {w: c / len(tokens) * (math.log((n + 1) / (df[w] + 1)) + 1)
                for w, c in Counter(tokens).items()}

    def cosine(a, b):
        dot = sum(v * b.get(w, 0.0) for w, v in a.items())
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    query = vector(tokenize(question))
    scores = [cosine(query, vector(tokens)) for tokens in documents]
    i = max(range(n), key=lambda j: scores[j])
    return faqs[i], scores[i]


def lambda_handler(event, context):
    start = time.perf_counter()
    event = event if isinstance(event, dict) else {}
    rc = event.get("requestContext") or {}
    http = rc.get("http") or {}
    request_id = getattr(context, "aws_request_id", None) or str(uuid.uuid4())
    api_request_id = rc.get("requestId") or ""
    method = str(http.get("method") or event.get("httpMethod") or "").upper()
    path = str(event.get("rawPath") or event.get("path") or "").rstrip("/")

    def finish(status, payload, app_error=0, **fields):
        payload.update(requestId=request_id, apiRequestId=api_request_id, build=BUILD)
        entry = dict(event="request_complete", requestId=request_id,
                     apiRequestId=api_request_id, method=method, path=path,
                     status=status, applicationError=app_error,
                     durationMs=round((time.perf_counter() - start) * 1000, 2),
                     build=BUILD, **fields)
        # Text logging: mỗi message là một JSON object, metric filter đọc được.
        # Không ghi request body/câu hỏi/token/credential vào CloudWatch.
        print(json.dumps(entry, ensure_ascii=False))
        return {"statusCode": status,
                "headers": {"Content-Type": "application/json; charset=utf-8",
                            "Cache-Control": "no-store", "X-Request-Id": request_id},
                "body": json.dumps(payload, ensure_ascii=False)}

    if method == "GET" and path == "/health":
        return finish(200, {"status": "ok", "message": "Course FAQ Chatbot API"})
    if method != "POST" or path != "/chat":
        return finish(404, {"error": "Endpoint không tồn tại"})
    headers = {str(k).lower(): str(v) for k, v in (event.get("headers") or {}).items()}
    content_type = headers.get("content-type", "application/json").split(";")[0].strip().lower()
    if content_type != "application/json":
        return finish(415, {"error": "Cần gửi Content-Type: application/json"})

    try:
        raw = event.get("body") or "{}"
        if not isinstance(raw, str):
            raise TypeError("body phải là chuỗi")
        # Giới hạn trước decode để tránh giải mã body tùy ý quá lớn.
        if len(raw.encode("utf-8")) > MAX_BODY_BYTES * 2:
            return finish(413, {"error": "Request body quá lớn"})
        if event.get("isBase64Encoded"):
            raw = base64.b64decode(raw, validate=True).decode("utf-8")
        if len(raw.encode("utf-8")) > MAX_BODY_BYTES:
            return finish(413, {"error": "Request body quá lớn"})
        data = json.loads(raw)
        question = data.get("question") if isinstance(data, dict) else None
    except (ValueError, TypeError, UnicodeDecodeError, binascii.Error):
        return finish(400, {"error": "JSON không hợp lệ"})
    if not isinstance(question, str) or not question.strip():
        return finish(400, {"error": "Cần nhập câu hỏi"})
    question = question.strip()
    if len(question) > 500:
        return finish(400, {"error": "Câu hỏi tối đa 500 ký tự"})

    try:
        bucket = os.environ["FAQ_BUCKET"]
        key = os.environ.get("FAQ_KEY", "faq.json")
        threshold = float(os.environ.get("SIMILARITY_THRESHOLD", "0.30"))
        if not math.isfinite(threshold) or not 0 < threshold <= 1:
            raise ValueError("threshold ngoài khoảng (0, 1]")
        obj = get_s3().get_object(Bucket=bucket, Key=key)
        stream = obj["Body"]
        try:
            faqs = validate_faqs(json.loads(stream.read().decode("utf-8-sig")))
        finally:
            stream.close()
        best, score = search_faq(question, faqs)
    except Exception as exc:
        return finish(500, {"error": "Không thể tải hoặc tìm kiếm dữ liệu FAQ"},
                      app_error=1, errorType=type(exc).__name__, errorStage="faq")

    matched = best is not None and score >= threshold
    result = {"question": question, "matched": matched,
              "answer": best["answer"] if matched else
              "Mình chưa tìm thấy câu trả lời phù hợp trong tài liệu môn học.",
              "matchedFaqId": best["id"] if matched else None,
              "similarity": round(score, 4), "threshold": threshold,
              "source": best.get("source", "") if matched else None,
              "category": best.get("category", "") if matched else None,
              "faqCount": len(faqs), "faqETag": obj.get("ETag", "")}
    log_saved = False
    error_type = ""
    try:
        get_table(os.environ["LOG_TABLE"]).put_item(Item={
            "requestId": request_id, "apiRequestId": api_request_id,
            "question": question, "matchedFaqId": result["matchedFaqId"] or "NONE",
            "similarity": Decimal(str(result["similarity"])), "matched": matched,
            "threshold": Decimal(str(threshold)), "build": BUILD,
            "faqETag": result["faqETag"],
            "timestamp": datetime.now(timezone.utc).isoformat()})
        log_saved = True
    except Exception as exc:
        error_type = type(exc).__name__
    result["logSaved"] = log_saved
    return finish(200, result, app_error=int(not log_saved), matched=matched,
                  matchedFaqId=result["matchedFaqId"], similarity=result["similarity"],
                  threshold=threshold, faqCount=len(faqs), logSaved=log_saved,
                  errorStage="" if log_saved else "dynamodb", errorType=error_type)
