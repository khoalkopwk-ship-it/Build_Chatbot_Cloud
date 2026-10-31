#!/usr/bin/env bash
# Xuất backup lên máy đang chạy AWS CLI. KHÔNG commit DynamoDB logs hoặc backup private lên GitHub.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_aws_common.sh
source "$DIR/_aws_common.sh"
verify_context
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="${1:-$HOME/coursefaq-backup-$STAMP}"
[[ ! -e "$BACKUP_DIR" ]] || { echo "STOP: Đường dẫn đã tồn tại: $BACKUP_DIR" >&2; exit 2; }
umask 077
mkdir -p "$BACKUP_DIR/s3-data" "$BACKUP_DIR/s3-web" "$BACKUP_DIR/config" "$BACKUP_DIR/dynamodb"
# Chỉ backup nếu resource tồn tại; không dùng dữ liệu giả.
resource_present data_bucket || { echo 'Data bucket không tồn tại; không thể backup.' >&2; exit 2; }
resource_present web_bucket || { echo 'Web bucket không tồn tại; không thể backup.' >&2; exit 2; }
resource_present dynamodb || { echo 'DynamoDB table không tồn tại; không thể backup.' >&2; exit 2; }
resource_present api || { echo 'API không tồn tại; không thể backup.' >&2; exit 2; }
resource_present lambda || { echo 'Lambda không tồn tại; không thể backup.' >&2; exit 2; }
aws s3 sync "s3://$DATA_BUCKET" "$BACKUP_DIR/s3-data" --region "$REGION" --only-show-errors
aws s3 sync "s3://$WEB_BUCKET" "$BACKUP_DIR/s3-web" --region "$REGION" --only-show-errors
aws dynamodb scan --table-name "$TABLE" --region "$REGION" --output json > "$BACKUP_DIR/dynamodb/items.json"
aws dynamodb describe-table --table-name "$TABLE" --region "$REGION" > "$BACKUP_DIR/config/dynamodb-table.json"
aws lambda get-function-configuration --function-name "$LAMBDA" --region "$REGION" > "$BACKUP_DIR/config/lambda-config.json"
aws apigatewayv2 get-api --api-id "$API_ID" --region "$REGION" > "$BACKUP_DIR/config/api-config.json"
aws apigatewayv2 get-stage --api-id "$API_ID" --stage-name '$default' --region "$REGION" > "$BACKUP_DIR/config/api-stage.json"
if resource_present alarm; then aws cloudwatch describe-alarms --alarm-names "$ALARM" --region "$REGION" > "$BACKUP_DIR/config/alarm.json"; fi
if resource_present dashboard; then aws cloudwatch get-dashboard --dashboard-name "$DASHBOARD" --region "$REGION" > "$BACKUP_DIR/config/dashboard.json"; fi
[[ -s "$BACKUP_DIR/s3-data/faq.json" ]] || { echo 'STOP: FAQ backup rỗng hoặc thiếu.' >&2; exit 4; }
[[ -s "$BACKUP_DIR/s3-web/index.html" ]] || { echo 'STOP: Website index.html backup thiếu.' >&2; exit 4; }
[[ -s "$BACKUP_DIR/dynamodb/items.json" ]] || { echo 'STOP: DynamoDB backup thiếu.' >&2; exit 4; }
printf '%s\n' "account=$ACCOUNT" "region=$REGION" "UTC=$STAMP" > "$BACKUP_DIR/.coursefaq-backup-ok"
echo "BACKUP COMPLETE: $BACKUP_DIR"
echo 'DynamoDB items.json có thể có câu hỏi người dùng; lưu riêng tư, KHÔNG commit công khai.'
echo 'Backup S3 sync chỉ chứa phiên bản hiện hành; nếu S3 có object version cũ, phải xử lý riêng.'
