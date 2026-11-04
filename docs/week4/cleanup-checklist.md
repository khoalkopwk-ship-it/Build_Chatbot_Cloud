# CHECKLIST CLEANUP AWS LEARNER LAB — TUẦN 4

**Nhóm:** Serverless | **Ngày hoàn thành thực tế:** 04/11/2026 (11:33:53 UTC+7)  
**Account thực tế:** `550609224402` | **Region:** `us-east-1`  
**Phụ trách kỹ thuật script/đối soát:** Đặng Nguyễn Minh Khoa (`khoalkopwk-ship-it` — 24110253)  
**Phụ trách thao tác AWS/ảnh:** Ngô Anh Bằng (`bawgitne` — 24110166)  
**Lưu ý:** Đã thực hiện thao tác xóa thật trên AWS CloudShell, có đầy đủ log CLI và 4 ảnh chụp màn hình minh chứng.

## A. Trước khi xóa — bắt buộc

- [x] Cả nhóm đã hoàn tất demo, quay video tối đa 10 phút (hỏi đáp FAQ + đối soát log DynamoDB & CloudWatch) và lưu trữ video ngoài AWS Learner Lab: [Link Google Drive Video Demo](https://drive.google.com/drive/folders/1sHl8H4BfK-NmiGBEJrDkyx8ODl4nMWLm?usp=sharing).
- [x] Đã kiểm tra FAQ mới và lưu `data/faq.json` cuối cùng (50 FAQ, 26.2 KB) vào GitHub.
- [x] Đã sao lưu `course-faq-data-24110253` và `course-faq-web-24110253` ra máy riêng và gói tar.gz trên CloudShell.
- [x] Đã xuất DynamoDB `CourseFAQQueryLogs` ra nơi lưu trữ riêng tư an toàn (không đưa câu hỏi người dùng lên GitHub public).
- [x] Đã lưu kết quả test, ảnh trước cleanup, CloudWatch metrics, usage/chi phí quan sát được.
- [x] Đã xác nhận bằng `aws sts get-caller-identity` là đúng Account `550609224402` và Region `us-east-1` (`voclabs/user5515899=24110166@student.hcmute.edu.vn`).
- [x] Đã chạy `bash scripts/week4/inventory-aws.sh` và `bash scripts/week4/cleanup-aws.sh --plan`.
- [x] Đã chạy `bash scripts/week4/backup-before-cleanup.sh` thành công lúc 10:26 UTC+7 (03:26:48Z) và lưu gói nén tại `/home/cloudshell-user/coursefaq-backup-20261104T032652Z.tar.gz`.

## B. Các tài nguyên cần dọn theo thứ tự chuẩn

**Thứ tự tháo dỡ bắt buộc:** **API Gateway → Lambda → DynamoDB → S3 (Data & Web) → CloudWatch**

| STT | Thứ tự | Dịch vụ | Tài nguyên chính xác | Trước | Sau | Minh chứng sau |
|:---:|:---:|---|---|---|---|---|
| 1 | 1 | API Gateway | HTTP API `course-faq-api` / ID `tijvqgrltk` | 2 routes (`POST /chat`, `$default`) | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 2 | 2 | Lambda | `course-faq-lambda` | Python 3.13, RAM 128 MB | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 3 | 3 | DynamoDB | `CourseFAQQueryLogs` | Pay-per-request table | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 4 | 4 | S3 dữ liệu | `course-faq-data-24110253` | Chứa `faq.json` (50 FAQ) | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 5 | 5 | S3 website | `course-faq-web-24110253` | Chứa 4 file frontend | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 6 | 6 | CloudWatch Alarm | `CourseFAQ-ApplicationErrors` | Metric Alarm lỗi app | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 7 | 7 | CloudWatch Dashboard | `CourseFAQ-Week3-Dashboard` | Dashboard theo dõi | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 8 | 8 | CloudWatch Logs | `/aws/lambda/course-faq-lambda` | Log stream Lambda | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |
| 9 | 9 | CloudWatch Logs | `/aws/apigateway/course-faq-api` | Log stream API Gateway | **ĐÃ XÓA (ABSENT)** | [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png), [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) |

**Quan trọng:** Chỉ xóa đúng 9 tài nguyên của dự án; không xóa IAM `LabRole` hoặc tài nguyên AWS Lab do giảng viên cấp.

## C. Sau khi xóa — yêu cầu bằng chứng

- [x] Chạy `bash scripts/week4/verify-cleanup.sh` và đạt kết quả `absent=9/9, present=0, failed=0`, **không có AccessDenied**.
- [x] Chụp ảnh pre-cleanup và sao lưu: [`Week4_Cleanup_Before.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Before.png) hiển thị rõ Account ID `550609224402`, Region `us-east-1` và thời gian UTC.
- [x] Chụp ảnh chi tiết sao lưu dữ liệu: [`Week4_Cleanup_Backup_Detail.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Backup_Detail.png) xác nhận 50 FAQ và marker `.coursefaq-backup-ok`.
- [x] Chụp ảnh lệnh thực thi tháo dỡ tuần tự: [`Week4_Cleanup_Execution_Order.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_Execution_Order.png) minh chứng xóa đúng thứ tự: API Gateway → Lambda → DynamoDB → S3 → CloudWatch.
- [x] Chụp ảnh kiểm chứng độc lập sau xóa: [`Week4_Cleanup_After.png`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week4/Week4_Cleanup_After.png) xác nhận toàn bộ 9/9 tài nguyên đã bị xóa sạch hoàn toàn.
- [x] Lưu output log thật đã rà soát vào [`docs/week4/cleanup-verification.txt`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-verification.txt).
- [x] Điền biên bản nghiệm thu [`docs/week4/cleanup-evidence-template.md`](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week4/cleanup-evidence-template.md) với thời điểm và chữ ký xác nhận của cả 2 thành viên.
- [x] Commit script, checklist và minh chứng thật vào repo; cập nhật worklog đúng số giờ thực tế.

## Quy tắc kết luận

**ĐÃ CLEANUP HOÀN TẤT (ABSENT 9/9)**: 100% tài nguyên đã được giải phóng thành công, không còn dịch vụ nào chạy ngầm làm phát sinh chi phí trên AWS Academy Learner Lab.
