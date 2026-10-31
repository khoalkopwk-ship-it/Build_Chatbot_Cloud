#!/usr/bin/env bash
# Kế hoạch cleanup mặc định chỉ đọc. --execute mới xóa thật, sau video & backup.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_aws_common.sh
source "$DIR/_aws_common.sh"
MODE="${1:---plan}"
BACKUP_DIR="${2:-}"
[[ "$MODE" == --plan || "$MODE" == --execute ]] || {
  echo "Usage: bash scripts/week4/cleanup-aws.sh [--plan | --execute BACKUP_DIR]" >&2; exit 2;
}
verify_context
if [[ "$MODE" == --plan ]]; then
  echo '=== PLAN ONLY: KHÔNG XÓA TÀI NGUYÊN ==='
  print_inventory
  echo 'Sau khi quay demo + backup: bash scripts/week4/cleanup-aws.sh --execute /duong-dan-backup'
  exit 0
fi
[[ -n "$BACKUP_DIR" && -f "$BACKUP_DIR/.coursefaq-backup-ok" ]] || {
  echo 'STOP: --execute yêu cầu thư mục backup có marker, tạo bằng backup-before-cleanup.sh.' >&2; exit 2;
}
grep -qx "account=$ACCOUNT" "$BACKUP_DIR/.coursefaq-backup-ok" &&
  grep -qx "region=$REGION" "$BACKUP_DIR/.coursefaq-backup-ok" || {
    echo 'STOP: Backup không đúng Account/Region.' >&2; exit 2;
  }
[[ -s "$BACKUP_DIR/s3-data/faq.json" && -s "$BACKUP_DIR/s3-web/index.html" && -s "$BACKUP_DIR/dynamodb/items.json" ]] || {
  echo 'STOP: Backup không đủ FAQ, web và DynamoDB.' >&2; exit 2;
}
# Preflight versioning: không xóa phần nào nếu bucket có versioning enabled/suspended.
for bucket in "$DATA_BUCKET" "$WEB_BUCKET"; do
  if resource_present "$([[ "$bucket" == "$DATA_BUCKET" ]] && echo data_bucket || echo web_bucket)"; then
    version_status="$(aws s3api get-bucket-versioning --bucket "$bucket" --region "$REGION" --query Status --output text)"
    if [[ "$version_status" != None && -n "$version_status" ]]; then
      echo "STOP: Bucket $bucket versioning=$version_status. Script chưa hỗ trợ xóa các object versions. Xử lý phiên bản/backup thủ công." >&2
      exit 3
    fi
  fi
done
# Chỉ nhận xác nhận từ terminal tương tác.
[[ -t 0 ]] || { echo 'STOP: Phải xác nhận trực tiếp trong terminal tương tác.' >&2; exit 3; }
echo '--- DANH SÁCH TÀI NGUYÊN SẼ XÓA KHÔNG THỂ HOÀN TÁC ---'
print_inventory
printf 'Đã quay demo, lưu minh chứng, và backup xong? Nhập chính xác DELETE-COURSEFAQ-550609224402: '
IFS= read -r approval
[[ "$approval" == DELETE-COURSEFAQ-550609224402 ]] || { echo 'Đã hủy cleanup.'; exit 1; }
LOGFILE="$BACKUP_DIR/cleanup-execute-$(date -u +%Y%m%dT%H%M%SZ).log"
exec > >(tee -a "$LOGFILE") 2>&1
echo "CLEANUP START $(date -u +%Y-%m-%dT%H:%M:%SZ) Account=$ACCOUNT Region=$REGION"
# Thứ tự: dừng API trước, Lambda, DB, dữ liệu, CloudWatch.
if resource_present api; then aws apigatewayv2 delete-api --api-id "$API_ID" --region "$REGION"; echo 'DELETED API'; fi
if resource_present lambda; then aws lambda delete-function --function-name "$LAMBDA" --region "$REGION"; echo 'DELETED Lambda'; fi
if resource_present dynamodb; then aws dynamodb delete-table --table-name "$TABLE" --region "$REGION"; aws dynamodb wait table-not-exists --table-name "$TABLE" --region "$REGION"; echo 'DELETED DynamoDB'; fi
if resource_present data_bucket; then aws s3 rb "s3://$DATA_BUCKET" --force --region "$REGION"; echo 'DELETED FAQ S3 bucket'; fi
if resource_present web_bucket; then aws s3 rb "s3://$WEB_BUCKET" --force --region "$REGION"; echo 'DELETED website S3 bucket'; fi
if resource_present alarm; then aws cloudwatch delete-alarms --alarm-names "$ALARM" --region "$REGION"; echo 'DELETED Alarm'; fi
if resource_present dashboard; then aws cloudwatch delete-dashboards --dashboard-names "$DASHBOARD" --region "$REGION"; echo 'DELETED Dashboard'; fi
if resource_present lambda_log; then aws logs delete-log-group --log-group-name "$LAMBDA_LOG" --region "$REGION"; echo 'DELETED Lambda log group'; fi
if resource_present api_log; then aws logs delete-log-group --log-group-name "$API_LOG" --region "$REGION"; echo 'DELETED API log group'; fi
echo "CLEANUP COMMANDS COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo 'BẮT BUỘC kiểm tra lại inventory-aws.sh, chụp màn hình AWS, ghi rõ lỗi hoặc tài nguyên còn tồn tại.'
echo "Log: $LOGFILE (giữ bản thô ngoài GitHub nếu có dữ liệu nhạy cảm)"
