import base64
import json
import logging
import math
import os
import re
import unicodedata
import uuid
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
FAQ_BUCKET = os.environ.get("FAQ_BUCKET", "course-faq-data-24110253")
LOG_TABLE = os.environ.get("LOG_TABLE", "CourseFAQQueryLogs")

STOPWORDS = {
    "la", "gi", "co", "cua", "va", "cho", "toi", "minh", "ban", "ve",
    "nhung", "cac", "trong", "mot", "nhu", "the", "nao", "duoc",
    "khong", "hay", "biet", "giup", "xin", "hoi"
}


def tokenize(text):
    text = unicodedata.normalize("NFD", str(text).lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d")
    return [word for word in re.findall(r"[a-z0-9]+", text)
            if word not in STOPWORDS]


def search_faq(question, faqs):
    if not faqs:
        return None, 0.0

    documents = [tokenize(faq.get("question", "")) for faq in faqs]
    n = len(documents)
    document_frequency = Counter()
    for tokens in documents:
        document_frequency.update(set(tokens))

    def make_vector(tokens):
        counts = Counter(tokens)
        if not tokens:
            return {}
        return {
            word: (count / len(tokens)) *
                  (math.log((n + 1) / (document_frequency[word] + 1)) + 1)
            for word, count in counts.items()
        }

    def cosine(a, b):
        if not a or not b:
            return 0.0
        dot = sum(weight * b.get(word, 0.0) for word, weight in a.items())
        norm_a = math.sqrt(sum(weight ** 2 for weight in a.values()))
        norm_b = math.sqrt(sum(weight ** 2 for weight in b.values()))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    query_vector = make_vector(tokenize(question))
    scores = [cosine(query_vector, make_vector(tokens)) for tokens in documents]
    best_index = max(range(n), key=lambda i: scores[i])
    return faqs[best_index], scores[best_index]


def response(status, payload):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(payload, ensure_ascii=False)
    }


def lambda_handler(event, context):
    http = (event.get("requestContext") or {}).get("http") or {}
    method = (http.get("method") or event.get("httpMethod") or "").upper()
    path = (event.get("rawPath") or event.get("path") or "").rstrip("/")

    if method == "GET" and path == "/health":
        return response(200, {"status": "ok", "message": "Course FAQ Chatbot API"})

    if method != "POST" or path != "/chat":
        return response(404, {"error": "Endpoint không tồn tại"})

    try:
        raw_body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(raw_body).decode("utf-8")
        data = json.loads(raw_body)
        question = data.get("question") if isinstance(data, dict) else None
    except (ValueError, TypeError, UnicodeDecodeError):
        return response(400, {"error": "JSON không hợp lệ"})

    if not isinstance(question, str) or not question.strip():
        return response(400, {"error": "Cần nhập câu hỏi"})
    question = question.strip()
    if len(question) > 500:
        return response(400, {"error": "Câu hỏi tối đa 500 ký tự"})

    try:
        obj = s3.get_object(Bucket=FAQ_BUCKET, Key="faq.json")
        faqs = json.loads(obj["Body"].read().decode("utf-8-sig"))
        if not isinstance(faqs, list):
            raise ValueError("faq.json phải là một mảng JSON")
        best, score = search_faq(question, faqs)
    except Exception:
        logger.exception("Không đọc hoặc xử lý được dữ liệu FAQ")
        return response(500, {"error": "Không thể tải hoặc tìm kiếm dữ liệu FAQ"})

    threshold = 0.30
    matched = best is not None and score >= threshold
    result = {
        "question": question,
        "answer": best.get("answer", "") if matched else
                  "Mình chưa tìm thấy câu trả lời phù hợp trong tài liệu môn học.",
        "matchedFaqId": best.get("id") if matched else None,
        "similarity": round(score, 4),
        "matched": matched
    }

    # Lưu log ngay cả khi không tìm được FAQ. Lỗi ghi log không làm hỏng câu trả lời.
    try:
        dynamodb.Table(LOG_TABLE).put_item(Item={
            "requestId": str(uuid.uuid4()),
            "question": question,
            "matchedFaqId": result["matchedFaqId"] or "NONE",
            "similarity": Decimal(str(result["similarity"])),
            "matched": matched,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        result["logSaved"] = True
    except Exception:
        logger.exception("Không thể lưu lịch sử vào DynamoDB")
        result["logSaved"] = False

    return response(200, result)
