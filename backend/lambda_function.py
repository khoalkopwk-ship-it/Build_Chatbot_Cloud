import json
import os
import uuid
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")
table = boto3.resource("dynamodb").Table(os.environ["LOG_TABLE"])


def lambda_handler(event, context):
    obj = s3.get_object(
        Bucket=os.environ["FAQ_BUCKET"],
        Key=os.environ["FAQ_KEY"]
    )
    faqs = json.loads(obj["Body"].read().decode("utf-8"))

    if not isinstance(faqs, list) or not faqs:
        raise ValueError("Kho FAQ phải là danh sách không rỗng")

    request_id = str(uuid.uuid4())

    table.put_item(Item={
        "request_id": request_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "record_type": "infrastructure_test",
        "faq_count": len(faqs),
        "status": "success"
    })

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "phase": "week1",
            "faq_count": len(faqs),
            "request_id": request_id,
            "message": "Đọc S3 và ghi DynamoDB thành công"
        }, ensure_ascii=False)
    }