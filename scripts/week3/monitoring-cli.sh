#!/usr/bin/env bash
# TÙY CHỌN: chạy trong AWS CloudShell nếu Learner Lab cho phép.
# Thay tài nguyên rồi review. Script chỉ cấu hình log/metric/alarm cho API hiện có.
# Không tạo IAM role, không tạo Lambda, không tạo lại bucket/table/API.
set -euo pipefail
: "${FAQ_API_ID:?Điền FAQ_API_ID của HTTP API hiện tại}"
: "${FAQ_WEB_ORIGIN:?Điền FAQ_WEB_ORIGIN lấy từ S3 Properties, không có / cuối}"
FAQ_REGION="${FAQ_REGION:-us-east-1}"
FAQ_FUNCTION="${FAQ_FUNCTION:-course-faq-lambda}"
if [[ "$FAQ_REGION" != us-east-1 && "$FAQ_REGION" != us-west-2 ]]; then
  echo 'Region không thuộc danh sách cho phép' >&2
  exit 1
fi
FAQ_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
FAQ_API_LOG_GROUP='/aws/apigateway/course-faq-api'
FAQ_LAMBDA_LOG_GROUP="/aws/lambda/$FAQ_FUNCTION"
export AWS_DEFAULT_REGION="$FAQ_REGION"

aws apigatewayv2 get-api --api-id "$FAQ_API_ID" --query '{Name:Name,Type:ProtocolType,Endpoint:ApiEndpoint}'
FAQ_PROTOCOL="$(aws apigatewayv2 get-api --api-id "$FAQ_API_ID" --query ProtocolType --output text)"
[[ "$FAQ_PROTOCOL" == HTTP ]] || { echo 'Cần HTTP API'; exit 1; }

# Không nuốt lỗi AccessDenied. Log group có rồi thì bỏ qua bước tạo.
FAQ_EXISTING_GROUP="$(aws logs describe-log-groups --log-group-name-prefix "$FAQ_API_LOG_GROUP" --query "logGroups[?logGroupName=='$FAQ_API_LOG_GROUP'].logGroupName" --output text)"
if [[ -z "$FAQ_EXISTING_GROUP" ]]; then
  aws logs create-log-group --log-group-name "$FAQ_API_LOG_GROUP" --tags Project=CourseFAQChatbot,Owner=24110253-24110166
fi
aws logs put-retention-policy --log-group-name "$FAQ_API_LOG_GROUP" --retention-in-days 7
aws logs put-retention-policy --log-group-name "$FAQ_LAMBDA_LOG_GROUP" --retention-in-days 7

FAQ_TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$FAQ_TMP_DIR"' EXIT
export FAQ_ACCOUNT_ID FAQ_API_ID FAQ_API_LOG_GROUP FAQ_REGION FAQ_WEB_ORIGIN FAQ_TMP_DIR
python3 - <<'PY'
import json,os
from pathlib import Path
p=Path(os.environ['FAQ_TMP_DIR'])
arn=f"arn:aws:logs:{os.environ['FAQ_REGION']}:{os.environ['FAQ_ACCOUNT_ID']}:log-group:{os.environ['FAQ_API_LOG_GROUP']}"
fmt=json.dumps({'requestId':'$context.requestId','requestTime':'$context.requestTime','httpMethod':'$context.httpMethod','routeKey':'$context.routeKey','status':'$context.status','responseLength':'$context.responseLength','integrationError':'$context.integrationErrorMessage'},separators=(',',':'))
(p/'access.json').write_text(json.dumps({'DestinationArn':arn,'Format':fmt}))
(p/'cors.json').write_text(json.dumps({'AllowOrigins':[os.environ['FAQ_WEB_ORIGIN']],'AllowMethods':['GET','POST','OPTIONS'],'AllowHeaders':['content-type'],'MaxAge':300,'AllowCredentials':False}))
PY
aws apigatewayv2 update-api --api-id "$FAQ_API_ID" --cors-configuration "file://$FAQ_TMP_DIR/cors.json"
aws apigatewayv2 update-stage --api-id "$FAQ_API_ID" --stage-name '$default' --access-log-settings "file://$FAQ_TMP_DIR/access.json" --default-route-settings ThrottlingBurstLimit=10,ThrottlingRateLimit=5

# Lambda Configuration > Monitoring and operations tools > Logging: Text.
# print(JSON) trong backend đã phát request_complete vào log group Lambda.
aws logs put-metric-filter --log-group-name "$FAQ_LAMBDA_LOG_GROUP" --filter-name CourseFAQApplicationErrors --filter-pattern '{ $.event = "request_complete" && $.applicationError = 1 }' --metric-transformations metricName=ApplicationErrors,metricNamespace=CourseFAQChatbot,metricValue=1,defaultValue=0
aws cloudwatch put-metric-alarm --alarm-name CourseFAQ-ApplicationErrors --namespace CourseFAQChatbot --metric-name ApplicationErrors --statistic Sum --period 60 --evaluation-periods 1 --datapoints-to-alarm 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --tags Key=Project,Value=CourseFAQChatbot Key=Owner,Value=24110253-24110166
date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
printf 'Account=%s Region=%s API=%s\n' "$FAQ_ACCOUNT_ID" "$FAQ_REGION" "$FAQ_API_ID"
echo 'Đã cấu hình; tiếp tục gửi request thật rồi kiểm tra log/metric/alarm. Không có SNS/email action.'
