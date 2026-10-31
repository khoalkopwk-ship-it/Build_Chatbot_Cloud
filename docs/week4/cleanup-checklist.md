# CHECKLIST CLEANUP AWS LEARNER LAB — TUẦN 4

**Nhóm:** Serverless | **Ngày hoàn thành thực tế:** `CHƯA THỰC HIỆN / CẬP NHẬT SAU`  
**Account dự kiến:** `550609224402` | **Region:** `us-east-1`  
**Phụ trách kỹ thuật script/đối soát:** Khoa (đề xuất) | **Phụ trách thao tác AWS/ảnh:** Bằng (đề xuất)  
**Lưu ý:** Tạo và commit checklist/script **không** chứng minh đã xóa. Phải có kết quả CLI/Console thực tế.

## A. Trước khi xóa — bắt buộc

- [ ] Cả nhóm đã demo, quay video tối đa 10 phút và lưu video ngoài AWS Learner Lab.
- [ ] Đã kiểm tra FAQ mới và lưu `data/faq.json` cuối cùng vào GitHub.
- [ ] Đã sao lưu `course-faq-data-24110253` và `course-faq-web-24110253` ra máy riêng.
- [ ] Đã xuất DynamoDB `CourseFAQQueryLogs` ra nơi lưu trữ riêng tư (không đưa câu hỏi người dùng lên GitHub public).
- [ ] Đã lưu kết quả test, ảnh trước cleanup, CloudWatch metrics, usage/chi phí quan sát được.
- [ ] Đã xác nhận bằng `aws sts get-caller-identity` là đúng Account `550609224402` và Region `us-east-1`.
- [ ] Đã chạy `bash scripts/week4/inventory-aws.sh` và `bash scripts/week4/cleanup-aws.sh --plan`.
- [ ] Đã chạy `bash scripts/week4/backup-before-cleanup.sh` thành công và ghi đường dẫn backup.

## B. Các tài nguyên cần dọn

| STT | Dịch vụ | Tài nguyên chính xác | Trước | Sau | Minh chứng sau |
| --- | --- | --- | --- | --- | --- |
| 1 | API Gateway | HTTP API `course-faq-api` / ID `tijvqgrltk` | Chưa cập nhật | Chưa xác minh | Ảnh API list + log CLI |
| 2 | Lambda | `course-faq-lambda` | Chưa cập nhật | Chưa xác minh | Ảnh Functions list |
| 3 | DynamoDB | `CourseFAQQueryLogs` | Chưa cập nhật | Chưa xác minh | Ảnh Tables list |
| 4 | S3 dữ liệu | `course-faq-data-24110253` | Chưa cập nhật | Chưa xác minh | Ảnh Buckets list |
| 5 | S3 website | `course-faq-web-24110253` | Chưa cập nhật | Chưa xác minh | Ảnh Buckets list |
| 6 | CloudWatch Alarm | `CourseFAQ-ApplicationErrors` | Chưa cập nhật | Chưa xác minh | Ảnh Alarms list |
| 7 | CloudWatch Dashboard | `CourseFAQ-Week3-Dashboard` | Chưa cập nhật | Chưa xác minh | Ảnh Dashboards list |
| 8 | CloudWatch Logs | `/aws/lambda/course-faq-lambda` | Chưa cập nhật | Chưa xác minh | Ảnh Log groups list |
| 9 | CloudWatch Logs | `/aws/apigateway/course-faq-api` | Chưa cập nhật | Chưa xác minh | Ảnh Log groups list |

**Quan trọng:** Chỉ xóa đúng tài nguyên của dự án; kiểm tra thêm tài nguyên phát sinh ngoài danh sách nếu có. Không xóa IAM `LabRole` hoặc tài nguyên AWS Lab do giảng viên cấp.

## C. Sau khi xóa — yêu cầu bằng chứng

- [ ] Chạy `bash scripts/week4/verify-cleanup.sh` và được `absent=9/9, present=0`, **không có AccessDenied**.
- [ ] Chụp `screenshots/week4/Week4_Cleanup_Before.png` và `Week4_Cleanup_After.png` có Account, Region, thời gian.
- [ ] Chụp các service list nếu cần: `Week4_Cleanup_API_Lambda.png`, `Week4_Cleanup_DynamoDB_S3.png`, `Week4_Cleanup_CloudWatch.png`.
- [ ] Lưu output `docs/week4/cleanup-verification.txt` bằng cách lọc dữ liệu nhạy cảm; **không bịa output**.
- [ ] Điền biên bản `docs/week4/cleanup-evidence-template.md` bằng thời điểm, người thực hiện, tên tài nguyên và kết quả thật.
- [ ] Rà soát tags `Project=CourseFAQChatbot`, `Owner` trong tài nguyên còn lại nếu có.
- [ ] Commit file script, checklist và minh chứng thật vào repo bằng tài khoản người thực hiện; ghi giờ công việc thực tế.

## Quy tắc kết luận

Chỉ ghi **"Đã cleanup hoàn tất"** khi có bằng chứng xóa và verify tất cả tài nguyên liên quan. Nếu thiếu quyền xóa, ghi **"Chưa hoàn tất — AccessDenied trên [tài nguyên]"**, không che lỗi. Nếu tạm giữ tài nguyên để demo/vấn đáp, ghi rõ **"Đang giữ lại vì ...; chưa cleanup"**.
