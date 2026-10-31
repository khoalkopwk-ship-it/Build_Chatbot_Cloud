#!/usr/bin/env bash
# READ ONLY, không xóa gì cả.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_aws_common.sh
source "$DIR/_aws_common.sh"
verify_context
print_inventory
echo 'Kết quả chỉ phản ánh trạng thái tại thời điểm truy vấn; chụp màn hình kèm Account/Region/time.'
