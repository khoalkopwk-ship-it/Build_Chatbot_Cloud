# BIÊN BẢN CLEANUP AWS — CHỜ DỮ LIỆU THỰC TẾ

> **TRẠNG THÁI: CHƯA THỰC HIỆN / CHƯA CÓ MINH CHỨNG XÓA.** Đây là mẫu điền sau khi chạy thật trên AWS, không phải kết quả giả lập.

- **Dự án:** CourseFAQChatbot — nhóm Serverless.
- **Account xác minh:** `550609224402` (kiểm tra lại khi chạy).
- **Region:** `us-east-1`.
- **Ngày và giờ chạy (UTC+7):** ...
- **Người chạy cleanup và tài khoản GitHub:** ...
- **Người kiểm tra độc lập:** ...
- **Video demo đã hoàn tất và sao lưu:** Có/Chưa + vị trí/lộ trình lưu (không chứa token).
- **Backup:** đường dẫn cục bộ hoặc bằng chứng đã lưu riêng tư, **không đính kèm dữ liệu DynamoDB cá nhân**.
- **Lệnh chuẩn bị:** `bash scripts/week4/inventory-aws.sh`; `bash scripts/week4/backup-before-cleanup.sh`.
- **Lệnh cleanup:** `bash scripts/week4/cleanup-aws.sh --execute "<thư mục backup>"`.
- **Lệnh kiểm chứng:** `bash scripts/week4/verify-cleanup.sh`.
- **Kết quả kiểm chứng:** `absent=.../9; present=...` (ghi từ CLI thật, tuyệt đối không tự điền 9/9 nếu chưa chạy).
- **Nếu lỗi:** tên tài nguyên, tên lỗi, thời gian, biện pháp xử lý và trạng thái còn tồn tại.

| Dịch vụ | Tên resource | Ảnh trước | Ảnh sau | CLI/Console status | Người xác nhận |
| --- | --- | --- | --- | --- | --- |
| API Gateway | `tijvqgrltk` | ... | ... | ... | ... |
| Lambda | `course-faq-lambda` | ... | ... | ... | ... |
| DynamoDB | `CourseFAQQueryLogs` | ... | ... | ... | ... |
| S3 FAQ | `course-faq-data-24110253` | ... | ... | ... | ... |
| S3 web | `course-faq-web-24110253` | ... | ... | ... | ... |
| CloudWatch Alarm | `CourseFAQ-ApplicationErrors` | ... | ... | ... | ... |
| Dashboard | `CourseFAQ-Week3-Dashboard` | ... | ... | ... | ... |
| Lambda log group | `/aws/lambda/course-faq-lambda` | ... | ... | ... | ... |
| API log group | `/aws/apigateway/course-faq-api` | ... | ... | ... | ... |

## Kết luận cleanup

**Chưa thể kết luận.** Sau khi thực hiện, cập nhật bằng số liệu/ảnh thật và dẫn link commit GitHub thực tế. Đừng để chữ “đã dọn dẹp” nếu không có CLI output và ảnh kiểm chứng.

## Ghi nhận AI

ChatGPT hỗ trợ soạn script, checklist và cấu trúc biên bản. Sinh viên phải đọc hiểu, chạy và kiểm tra trên AWS Learner Lab thực tế.
