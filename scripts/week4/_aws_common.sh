#!/usr/bin/env bash
# Shared constants and read-only inventory helpers. AWS CLI v2 / CloudShell Bash.
set -euo pipefail
export AWS_DEFAULT_REGION=us-east-1
export AWS_PAGER=""
ACCOUNT=550609224402
REGION=us-east-1
API_ID=tijvqgrltk
API_NAME=course-faq-api
LAMBDA=course-faq-lambda
TABLE=CourseFAQQueryLogs
DATA_BUCKET=course-faq-data-24110253
WEB_BUCKET=course-faq-web-24110253
LAMBDA_LOG=/aws/lambda/course-faq-lambda
API_LOG=/aws/apigateway/course-faq-api
ALARM=CourseFAQ-ApplicationErrors
DASHBOARD=CourseFAQ-Week3-Dashboard

# Explicitly stop on CLI errors, even inside `if resource_present` conditions.
aws_read() {
  local result
  if ! result="$(aws "$@")"; then
    echo "STOP: Không truy vấn được AWS CLI: $1 $2 (quyền, token, kết nối)." >&2
    exit 4
  fi
  printf '%s' "$result"
}

verify_context() {
  command -v aws >/dev/null || { echo 'ERROR: Chưa có AWS CLI.' >&2; exit 1; }
  local actual
  actual="$(aws_read sts get-caller-identity --query Account --output text --region "$REGION")" || exit 4
  [[ "$actual" == "$ACCOUNT" ]] || {
    echo "STOP: AWS Account $actual khác account nhóm $ACCOUNT" >&2; exit 2;
  }
  echo "AWS Account=$actual Region=$REGION UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

# Trả 0 nếu tồn tại và đúng tên, 1 nếu không tồn tại.
resource_present() {
  local kind="$1" actual expected
  case "$kind" in
    api)
      actual="$(aws_read apigatewayv2 get-apis --region "$REGION" --query "Items[?ApiId=='$API_ID'].Name" --output text)" || exit 4
      expected="$API_NAME" ;;
    lambda)
      actual="$(aws_read lambda list-functions --region "$REGION" --query "Functions[?FunctionName=='$LAMBDA'].FunctionName" --output text)" || exit 4
      expected="$LAMBDA" ;;
    dynamodb)
      actual="$(aws_read dynamodb list-tables --region "$REGION" --query "TableNames[?@=='$TABLE']" --output text)" || exit 4
      expected="$TABLE" ;;
    data_bucket | web_bucket)
      if [[ "$kind" == data_bucket ]]; then expected="$DATA_BUCKET"; else expected="$WEB_BUCKET"; fi
      actual="$(aws_read s3api list-buckets --query "Buckets[?Name=='$expected'].Name" --output text)" || exit 4 ;;
    lambda_log | api_log)
      if [[ "$kind" == lambda_log ]]; then expected="$LAMBDA_LOG"; else expected="$API_LOG"; fi
      actual="$(aws_read logs describe-log-groups --region "$REGION" --log-group-name-prefix "$expected" --query "logGroups[?logGroupName=='$expected'].logGroupName" --output text)" || exit 4 ;;
    alarm)
      expected="$ALARM"
      actual="$(aws_read cloudwatch describe-alarms --region "$REGION" --alarm-names "$ALARM" --query "MetricAlarms[?AlarmName=='$ALARM'].AlarmName" --output text)" || exit 4 ;;
    dashboard)
      expected="$DASHBOARD"
      actual="$(aws_read cloudwatch list-dashboards --region "$REGION" --dashboard-name-prefix "$DASHBOARD" --query "DashboardEntries[?DashboardName=='$DASHBOARD'].DashboardName" --output text)" || exit 4 ;;
    *) echo "Unknown resource: $kind" >&2; exit 2 ;;
  esac
  if [[ "$actual" == "$expected" ]]; then return 0; fi
  if [[ -z "$actual" || "$actual" == None ]]; then return 1; fi
  echo "STOP: Kết quả tên tài nguyên bất thường cho $kind: $actual" >&2
  exit 3
}

print_inventory() {
  local kind
  for kind in api lambda dynamodb data_bucket web_bucket alarm dashboard lambda_log api_log; do
    if resource_present "$kind"; then
      printf '%-16s %s\n' "$kind" 'PRESENT'
    else
      printf '%-16s %s\n' "$kind" 'ABSENT'
    fi
  done
}
