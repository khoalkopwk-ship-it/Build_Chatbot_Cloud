#!/usr/bin/env bash
# READ ONLY: kiểm chứng các resource dự án không còn; exit 0 chỉ khi cả 9 đều ABSENT.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_aws_common.sh
source "$DIR/_aws_common.sh"
verify_context
missing=0
present=0
for kind in api lambda dynamodb data_bucket web_bucket alarm dashboard lambda_log api_log; do
  if resource_present "$kind"; then
    echo "FAIL  $kind PRESENT"
    ((present+=1))
  else
    echo "PASS  $kind ABSENT"
    ((missing+=1))
  fi
done
echo "VERIFY SUMMARY: absent=$missing/9, present=$present; UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if (( present > 0 )); then
  echo 'Chưa thể xác nhận cleanup hoàn tất.' >&2
  exit 1
fi
echo 'Đã kiểm chứng KHÔNG còn 9 tài nguyên được định danh bằng script này.'
echo 'Vẫn cần rà soát các tài nguyên khác có thể đã tạo riêng trong Lab.'
