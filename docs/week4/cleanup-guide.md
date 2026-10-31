# HƯỚNG DẪN THAO TÁC CLEANUP — AWS LEARNER LAB (TUẦN 4)

**Làm sau khi hoàn tất demo, báo cáo số liệu và sao lưu. Không chạy `--execute` khi website còn cần hoạt động để giảng viên chấm.**

## 1. Chạy trên CloudShell hoặc máy có AWS CLI v2 và quyền Learner Lab

Ở gốc repository, mở terminal **Bash** (`CloudShell`, Git Bash hoặc WSL). Trên PowerShell có thể dùng `bash scripts/week4/inventory-aws.sh` nếu đã cài Bash. Trong AWS Learner Lab, dùng session/credentials được cấp sẵn, không tạo IAM user/role hay cấp access key lên GitHub. Nếu CloudShell không được hỗ trợ, dùng AWS Console từng dịch vụ và điền checklist từ kết quả thật.

### Kiểm tra không xóa tài nguyên

```bash
aws sts get-caller-identity
bash scripts/week4/inventory-aws.sh
bash scripts/week4/cleanup-aws.sh --plan
```

Chụp màn hình có Account ID, Region, thời gian. Nếu `AccessDenied`, xử lý quyền theo LabRole hoặc dùng AWS Console; script chủ động dừng khi lỗi, không coi lỗi quyền là resource đã xóa.

### Tạo bản sao lưu ngoài repository

```bash
bash scripts/week4/backup-before-cleanup.sh "$HOME/coursefaq-backup-final"
```

Thư mục backup chứa cả DynamoDB query logs, là dữ liệu riêng tư; **không đưa vào repo GitHub public**. Kiểm tra file `s3-data/faq.json`, `s3-web/index.html`, `dynamodb/items.json` có nội dung; lưu bản sao độc lập và video trước khi dọn.

### Cleanup không thể hoàn tác

```bash
bash scripts/week4/cleanup-aws.sh --execute "$HOME/coursefaq-backup-final"
```

Script chỉ xóa 9 tài nguyên định danh rõ sau khi người dùng nhập xác nhận. Nó sẽ từ chối bucket S3 có Versioning Enabled/Suspended; trong trường hợp đó xử lý có kiểm soát theo tài liệu AWS rồi kiểm chứng lại. Lệnh `aws s3 rb ... --force` chỉ tự dọn đối tượng không phiên bản, không dọn các phiên bản S3 cũ.

### Kiểm chứng sau cleanup

```bash
bash scripts/week4/verify-cleanup.sh | tee "$HOME/coursefaq-cleanup-verify.txt"
```

Chụp `screenshots/week4/Week4_Cleanup_After.png` và các ảnh dịch vụ nếu cần; sao chép **output verify đã rà soát thông tin riêng tư** vào `docs/week4/cleanup-verification.txt`, thêm thời gian thực tế. Nhớ kiểm tra các dịch vụ khác trong console nếu từng tạo tài nguyên bổ sung.

## 2. Lệnh AWS CLI được dùng — biết giải thích khi vấn đáp

| Resource | Lệnh xóa (đã khóa định danh trong script) | Kiểm chứng |
| --- | --- | --- |
| API Gateway | `aws apigatewayv2 delete-api --api-id tijvqgrltk --region us-east-1` | `get-apis` / AWS Console |
| Lambda | `aws lambda delete-function --function-name course-faq-lambda --region us-east-1` | `list-functions` |
| DynamoDB | `aws dynamodb delete-table --table-name CourseFAQQueryLogs --region us-east-1` | `list-tables`, waiter |
| S3 FAQ | `aws s3 rb s3://course-faq-data-24110253 --force` | `list-buckets` |
| S3 Web | `aws s3 rb s3://course-faq-web-24110253 --force` | `list-buckets` |
| Alarm | `aws cloudwatch delete-alarms --alarm-names CourseFAQ-ApplicationErrors` | `describe-alarms` |
| Dashboard | `aws cloudwatch delete-dashboards --dashboard-names CourseFAQ-Week3-Dashboard` | `list-dashboards` |
| Log groups | `aws logs delete-log-group --log-group-name ...` | `describe-log-groups` |

**Kết quả chỉ được đưa vào báo cáo khi có ảnh và kiểm chứng thật.** Script tồn tại trong Git là sản phẩm tự động hóa; log chạy thật mới là bằng chứng cleanup.

## 3. Nếu phải làm bằng AWS Console thay vì CLI

1. Xác minh Account/Region và quay demo. Tải S3 objects và export/ghi nhận DynamoDB an toàn.
2. API Gateway → `course-faq-api` → Delete (kiểm tra ID).
3. Lambda → Functions → `course-faq-lambda` → Delete.
4. DynamoDB → Tables → `CourseFAQQueryLogs` → Delete table.
5. S3 → Buckets → Empty bucket trước rồi Delete bucket **riêng từng bucket**, kiểm tra versioning.
6. CloudWatch → Alarms / Dashboards / Log groups → xóa đúng resource của CourseFAQ; không xóa chung các nhóm khác.
7. Chụp trạng thái danh sách sau khi xóa và/hoặc chạy `verify-cleanup.sh` nếu có CLI.

Không xóa `LabRole`, các role mặc định, tài nguyên Lab khác hoặc dữ liệu các nhóm khác.
