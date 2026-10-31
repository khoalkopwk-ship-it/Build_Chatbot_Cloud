# Danh mục Minh chứng Tuần 4 (Baseline Evidence Index) — Nhóm Serverless

> **Thời điểm ghi nhận:** 31/10/2026 (UTC+7)  
> **AWS Account ID:** `550609224402`  
> **Region:** `us-east-1` (US East - N. Virginia)  
> **IAM / Learner Lab Session:** `voclabs/user5515899=24110166@student.hcmute.edu.vn` (Ngô Anh Bằng)  
> **Hàm Lambda:** `course-faq-lambda` (Python 3.13, 128 MB RAM, Timeout 10s)  
> **S3 Bucket:** `course-faq-data-24110253`  
> **DynamoDB Table:** `CourseFAQQueryLogs`  
> **Trạng thái ghi nhận:** Baseline trước và ngay tại thời điểm upload kho dữ liệu 50 FAQ lên S3.

---

## 1. Danh sách 10 Minh chứng Ảnh Chụp Màn hình AWS

| STT | Tên file ảnh | Thành phần AWS | Nội dung minh chứng chi tiết |
|:---:|---|---|---|
| 01 | `Week4_S3_Backup.png` | Amazon S3 (`course-faq-data-24110253`) | Giao diện S3 Console hiển thị thao tác tải về bản sao lưu `faq (1).json` của kho 24 FAQ trước khi thực hiện cập nhật. |
| 02 | `Week4_S3_FAQ50_Upload.png` | Amazon S3 (`course-faq-data-24110253`) | Đối tượng `faq.json` bản mở rộng (50 FAQ) đã upload thành công lúc **10:17:26 (UTC+7) ngày 31/10/2026**, dung lượng **26.2 KB**, Storage class Standard. |
| 03 | `Week4_Lambda_General_Configuration.png` | AWS Lambda (`course-faq-lambda`) | Cấu hình tài nguyên thực thi: Memory **128 MB**, Ephemeral storage 512 MB, Timeout **10 giây**. |
| 04 | `Week4_Lambda_Environment_Variables.png` | AWS Lambda (`course-faq-lambda`) | Biến môi trường: `FAQ_BUCKET=course-faq-data-24110253`, `FAQ_KEY=faq.json`, `LOG_TABLE=CourseFAQQueryLogs`, `SIMILARITY_THRESHOLD=0.60`. |
| 05 | `Week4_Lambda_Test_Event.png` | AWS Lambda Console | Lưu cấu hình sự kiện kiểm thử `Week4_Test_Exact_FAQ` (Synchronous invocation, routeKey `POST /chat`). |
| 06 | `Week4_Lambda_Exact_FAQ017.png` | AWS Lambda Execution | Kết quả test câu hỏi khớp chính xác (FAQ017): `statusCode=200`, `matched=true`, `similarity=1.0`, `faqCount=24` (baseline), duration **7510.40 ms** (cold start + tải FAQ từ S3). |
| 07 | `Week4_Lambda_Unmatched.png` | AWS Lambda Execution | Kết quả test câu hỏi ngoài phạm vi môn học: `statusCode=200`, `matched=false`, `similarity=0.0`, `threshold=0.6`, duration **303.43 ms** (warm execution), `logSaved=true`. |
| 08 | `Week4_Lambda_Empty_Input.png` | AWS Lambda Execution | Kết quả test đầu vào rỗng: `statusCode=400`, thông báo `"Vui lòng nhập câu hỏi"`, duration **1.55 ms**, phản hồi lỗi validation đúng quy chuẩn. |
| 09 | `Week4_CloudWatch_Logs.png` | Amazon CloudWatch Logs | Log stream `/aws/lambda/course-faq-lambda` hiển thị chi tiết 3 lần gọi liên tiếp với các RequestId, Duration (7510.40ms, 303.43ms, 1.55ms) và Max Memory Used **97 MB**. |
| 10 | `Week4_Lambda_Metrics.png` | CloudWatch Metrics / Lambda Monitor | Đồ thị giám sát Lambda: Invocations sum=3, Errors max=0, Throttles max=0, Success rate min=100%, Concurrent executions max=1. |

---

## 2. Ghi chú Kỹ thuật về Dữ liệu Baseline

1. **Số lượng FAQ trong ảnh baseline:**  
   Các ảnh Lambda Test Event (`Week4_Lambda_Exact_FAQ017.png`, `Week4_Lambda_Unmatched.png`) chụp trước thời điểm upload S3 mới, do đó phản hồi `faqCount=24`. Đây là minh chứng baseline chuẩn xác, trung thực, không chỉnh sửa số liệu.
2. **Thời gian khởi động lạnh (Cold Start):**  
   Ở lần gọi đầu tiên sau khi khởi tạo môi trường thực thi, Lambda cần nạp runtime Python 3.13 (`Init duration: 83.24 ms`) và tải file `faq.json` từ S3 qua AWS SDK (`boto3`), tổng thời gian đo được là **7,510.40 ms**. Ở lần gọi tiếp theo (warm container), thời gian giảm xuống còn **303.43 ms**.
3. **Mức sử dụng bộ nhớ:**  
   Trong cấu hình 128 MB RAM, bộ nhớ sử dụng tối đa thực tế là **97 MB**, đảm bảo không xảy ra hiện tượng Out of Memory (OOM) trong quá trình xử lý TF-IDF cục bộ trên Lambda.
