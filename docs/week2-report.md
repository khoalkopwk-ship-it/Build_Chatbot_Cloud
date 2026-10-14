# BÁO CÁO TIẾN ĐỘ TUẦN 2

**Nhóm:** Serverless  
**Môn học:** Điện toán đám mây  
**Mã môn học:** CLCO332779_05UTExMC  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Đề tài:** Xây dựng chatbot hỏi đáp FAQ môn học dựa trên tìm kiếm từ khóa/TF-IDF chạy trên AWS Lambda.  
**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud  
**Link báo cáo tuần 2:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week2-report.md  
**Ngày tổng hợp minh chứng:** 14/10/2026  

## 1. Thông tin thành viên

| MSSV | Họ và tên | Vai trò |
| --- | --- | --- |
| 24110253 | Đặng Nguyễn Minh Khoa | Nhóm trưởng |
| 24110166 | Ngô Anh Bằng | Thành viên |

## 2. Mục tiêu tuần 2

Dựa trên các tài nguyên đã xây dựng ở tuần 1, nhóm triển khai chức năng hỏi đáp FAQ thực tế: tự cài đặt thuật toán **TF-IDF kết hợp Cosine Similarity** trên AWS Lambda (Python); đọc kho câu hỏi từ Amazon S3; nhận câu hỏi qua API Gateway; hiển thị kết quả trên website tĩnh S3; và ghi lịch sử truy vấn vào Amazon DynamoDB. Hệ thống **không gọi API LLM bên ngoài**.

Các tài nguyên sử dụng ở Region `us-east-1`:

| Dịch vụ | Tài nguyên | Vai trò |
| --- | --- | --- |
| Amazon S3 | `course-faq-data-24110253` | Lưu `faq.json` |
| Amazon S3 | `course-faq-web-24110253` | Host giao diện chatbot |
| AWS Lambda | `course-faq-lambda` | Tìm kiếm và xử lý câu hỏi |
| API Gateway (HTTP API) | `course-faq-api` | Cung cấp `GET /health` và `POST /chat` |
| Amazon DynamoDB | `CourseFAQQueryLogs` | Lưu lịch sử truy vấn, khóa `requestId` |

## 3. Kết quả thực hiện và phân công công việc

### 3.1. Đặng Nguyễn Minh Khoa (24110253)

**Công việc 1: Phát triển thuật toán tìm kiếm FAQ bằng TF-IDF**

- **Thời gian:** 4 giờ.
- Hoàn thiện mã Python gồm các hàm `tokenize()`, `search_faq()` và phép tính Cosine Similarity.
- Chuẩn hóa chữ thường, bỏ dấu tiếng Việt, lọc một số từ dừng; tự tính trọng số TF-IDF từ tập câu hỏi FAQ.
- So sánh vector câu hỏi với các câu FAQ, lấy kết quả có độ tương đồng lớn nhất; dùng ngưỡng tìm kiếm `0.30` theo mã nguồn hiện tại.
- Không sử dụng dịch vụ AI/LLM hoặc thư viện học máy bên ngoài để suy luận câu trả lời.

Minh chứng:
- Mã TF-IDF trong Lambda: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_TFIDF_Source_Code.png  
- Mã nguồn dự án: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/backend/lambda_function.py

**Công việc 2: Tích hợp Lambda đọc kho dữ liệu FAQ trên S3**

- **Thời gian:** 2 giờ.
- Cập nhật `course-faq-lambda` để nhận nội dung câu hỏi từ JSON request `POST /chat`.
- Sử dụng Boto3 `s3.get_object()` đọc object `faq.json` trong bucket dữ liệu.
- Kiểm tra đầu vào rỗng, JSON không hợp lệ, câu hỏi quá 500 ký tự và xử lý lỗi khi không đọc được FAQ.
- Cấu hình hai biến môi trường `FAQ_BUCKET=course-faq-data-24110253` và `LOG_TABLE=CourseFAQQueryLogs`.

Minh chứng:
- Biến môi trường Lambda: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Environment_Variables.png  
- Trang Lambda Test: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Function_Test_Tab.png

**Công việc 3: Phát triển chức năng ghi lịch sử truy vấn vào DynamoDB**

- **Thời gian:** 1 giờ.
- Tích hợp Boto3 `put_item()` để ghi `requestId`, `question`, `matchedFaqId`, `similarity`, `matched`, `timestamp`.
- Tạo `requestId` bằng UUID và `timestamp` theo giờ UTC.
- Thiết lập trường `logSaved` giúp xác định việc ghi log thành công hay thất bại.
- Ghi cả câu hỏi không khớp FAQ theo xử lý của mã; tính đúng đắn của trường hợp không khớp cần được kiểm thử riêng.

Minh chứng:
- Lambda trả `logSaved: true`: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Test_Chat_Success.png  
- Bản ghi DynamoDB: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/DynamoDB_Lambda_Test_Log_Detail.png

**Công việc 4: Cấu hình API Gateway và kiểm thử Lambda**

- **Thời gian:** 2 giờ.
- Cấu hình route `POST /chat` kết nối tới Lambda `course-faq-lambda`; xác nhận route `GET /health` cũng được gắn Lambda.
- Sử dụng Lambda Test để kiểm tra đầu vào `AWS Lambda là gì?` và dữ liệu trả về.
- Kết quả minh chứng: `statusCode: 200`, `matchedFaqId: "FAQ001"`, `similarity: 1.0`, `matched: true`, `logSaved: true`.
- Kết nối HTTP API dùng payload format version `2.0`.

Minh chứng:
- Route API Gateway: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/API_Gateway_Chat_Health_Integrations.png  
- Lambda Test thành công: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Test_Chat_Success.png

**Tổng thời gian: 9 giờ.**

### 3.2. Ngô Anh Bằng (24110166)

**Công việc 1: Hoàn thiện giao diện chatbot và tích hợp API vào frontend**

- **Thời gian:** 4 giờ.
- Tiếp tục phát triển giao diện chủ đề tối, gồm thanh bên, danh sách đoạn chat, ô nhập câu hỏi, khung hiển thị trả lời.
- Cập nhật JavaScript để gửi request thật tới API Gateway qua `POST /chat`, thay cho phản hồi mô phỏng.
- Hiển thị nội dung trả lời, mã FAQ và điểm tương đồng do backend trả về.
- Tách Invoke URL vào file `config.js`; không nhúng AWS access key/secret key trong frontend.

Minh chứng:
- Chatbot trả lời trên website S3: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/S3_Website_Chatbot_Answer.png  
- Mã nguồn giao diện và cấu hình:
  - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/frontend/index.html
  - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/frontend/style.css
  - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/frontend/script.js
  - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/frontend/config.js

**Công việc 2: Cấu hình CORS và triển khai frontend lên S3**

- **Thời gian:** 2 giờ.
- Triển khai các file giao diện lên bucket website `course-faq-web-24110253`.
- Rà soát cấu hình CORS trong HTTP API để website S3 có thể gửi request đến API Gateway từ origin khác.
- Trong quá trình tích hợp, phát hiện cấu hình CORS chưa khai báo `Access-Control-Allow-Headers`, làm request có `Content-Type: application/json` bị chặn.
- Sau khi xử lý kết nối, website hiển thị được câu trả lời thực tế từ hệ thống.

Minh chứng:
- CORS trước khi sửa (hiển thị `No headers are allowed`): https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/CORS_Before_Fix_Missing_Headers.png  
- Kết quả website hoạt động: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/S3_Website_Chatbot_Answer.png

**Công việc 3: Kiểm thử liên thông website, Lambda và DynamoDB**

- **Thời gian:** 2 giờ.
- Gửi câu hỏi `AWS Lambda là gì?` từ website và kiểm tra câu trả lời: `FAQ001`, độ tương đồng `100.0%`.
- Vào DynamoDB `CourseFAQQueryLogs` → Explore items, xác nhận bảng có bản ghi mới của câu hỏi.
- Rà soát kiểu dữ liệu `requestId` (String), `matched` (Boolean), `similarity` (Number), `timestamp` (String).
- Bản ghi có dấu thời gian `2026-10-14T09:30:34.634489+00:00`, tương ứng với phiên kiểm thử ngày 14/10/2026.

Minh chứng:
- Website trả lời: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/S3_Website_Chatbot_Answer.png  
- Danh sách log DynamoDB: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/DynamoDB_Log_Items.png  
- Chi tiết log sau phiên kiểm thử website: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/DynamoDB_Website_Query_Log.png

**Công việc 4: Tổng hợp ảnh minh chứng và chuẩn bị báo cáo tuần 2**

- **Thời gian:** 1 giờ.
- Đặt tên và sắp xếp ảnh kiểm thử Lambda, API Gateway, DynamoDB và website theo thư mục `screenshots/week2/`.
- Đối chiếu ảnh với yêu cầu tuần 2 và mô tả kết quả của từng thành phần.
- Chuẩn bị nội dung báo cáo, phân chia công việc và worklog để cập nhật vào repository.

Minh chứng:
- Thư mục bộ ảnh tuần 2: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/tree/main/screenshots/week2  
- Báo cáo tuần 2: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week2-report.md

**Tổng thời gian: 9 giờ.**

## 4. Tổng hợp thời gian thực hiện

| MSSV | Thành viên | Số công việc | Thời gian (giờ) |
| --- | --- | --- | ---: |
| 24110253 | Đặng Nguyễn Minh Khoa | 4 | 9 |
| 24110166 | Ngô Anh Bằng | 4 | 9 |
| **Tổng cộng** | | **8** | **18** |

**Ghi chú:** Toàn bộ công việc đã được hoàn thành đúng tiến độ với thời gian thực tế 9 giờ/thành viên (đáp ứng yêu cầu tối thiểu 8 giờ/sinh viên/tuần).

## 5. Kết quả đạt được

### 5.1. Kết quả kỹ thuật có minh chứng

| Nội dung kiểm thử | Kết quả quan sát | Minh chứng |
| --- | --- | --- |
| Lambda xử lý câu hỏi | `statusCode: 200`, `FAQ001`, `similarity: 1.0`, `matched: true` | [Lambda Test](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Test_Chat_Success.png) |
| Ghi log trong Lambda | `logSaved: true` | [Lambda Test](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/Lambda_Test_Chat_Success.png) |
| Kết nối API Gateway–Lambda | `POST /chat` và `GET /health` đều gắn Lambda | [API Integration](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/API_Gateway_Chat_Health_Integrations.png) |
| Chatbot website S3 | Hiển thị câu hỏi và câu trả lời thật, mã `FAQ001`, 100% | [Website S3](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/S3_Website_Chatbot_Answer.png) |
| DynamoDB lưu truy vấn | Có bản ghi câu hỏi `AWS Lambda là gì?`, `matchedFaqId=FAQ001`, `similarity=1` | [DynamoDB Log](https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week2/DynamoDB_Website_Query_Log.png) |

Luồng xử lý đã được kiểm thử thành công đối với câu hỏi có trong kho FAQ:

`Người dùng → Website S3 → API Gateway POST /chat → Lambda (TF-IDF) → S3 faq.json → DynamoDB (ghi log) → Website (hiển thị đáp án)`.

### 5.2. Cơ chế xử lý câu hỏi

1. Website gửi `POST /chat` với JSON có khóa `question`.
2. Lambda đọc dữ liệu `faq.json` riêng tư từ S3.
3. Thuật toán chuẩn hóa văn bản, tính trọng số TF-IDF và Cosine Similarity với từng câu hỏi FAQ.
4. Nếu điểm lớn nhất đạt ngưỡng `0.30`, Lambda trả về câu trả lời cùng mã FAQ; nếu không đạt, trả lời chưa tìm được nội dung phù hợp.
5. Lambda ghi lịch sử vào bảng DynamoDB và trả JSON để frontend hiển thị.

Dữ liệu FAQ ban đầu được báo cáo ở tuần 1 là **24 câu**. Bộ ảnh tuần 2 không thể hiện tổng số FAQ hiện có, vì vậy báo cáo không khẳng định đã tăng lên 30–50 câu.

## 6. Kế hoạch tuần 3

- Kiểm thử mở rộng chất lượng tìm kiếm, các trường hợp không khớp và đầu vào không hợp lệ; điều chỉnh ngưỡng nếu cần.
- Bổ sung và chuẩn hóa bộ dữ liệu FAQ để phục vụ môn học thực tế.
- Kiểm tra CORS, cấu hình bảo mật S3/IAM theo quyền `LabRole` sẵn có, hạn chế quyền public đối với dữ liệu FAQ.
- Theo dõi CloudWatch Logs/Metrics, độ trễ Lambda và lỗi truy vấn; kiểm tra khả năng giám sát.
- Hoàn thiện việc quản lý mã nguồn, ảnh minh chứng, worklog và xem xét cách tự động hóa triển khai nếu Lab cho phép.
- Theo dõi chi phí thực tế, gắn tag `Project`/`Owner`, tuân thủ yêu cầu dọn dẹp tài nguyên sau thực hành.

## 7. Kết luận

Trong tuần 2, nhóm Serverless đã phát triển bước chính của đề tài: triển khai thuật toán TF-IDF và Cosine Similarity bằng Python trên AWS Lambda, sử dụng Amazon S3 làm kho FAQ, tích hợp API Gateway với website chatbot, và lưu nhật ký hỏi đáp trên DynamoDB. Minh chứng chụp từ AWS Learner Lab cho thấy câu hỏi mẫu được trả lời đúng qua giao diện và có bản ghi truy vấn tương ứng trong cơ sở dữ liệu.

Các đầu việc đã được hoàn thành với thời gian thực tế **9 giờ cho mỗi thành viên**. Trong tuần 3, nhóm tập trung kiểm thử thêm các trường hợp biên, giám sát bằng CloudWatch, rà soát bảo mật và chuẩn hóa hồ sơ minh chứng.

## 8. Ghi nhận việc sử dụng AI hỗ trợ

Nhóm có sử dụng ChatGPT để **tham khảo cấu trúc mã Python/JavaScript, giải thích TF-IDF, gợi ý xử lý CORS và hỗ trợ soạn nội dung báo cáo**. Việc tạo tài nguyên AWS, triển khai và thử nghiệm hệ thống được thực hiện trên AWS Academy Learner Lab của nhóm. Các thành viên cần kiểm tra mã nguồn, nắm rõ cấu hình và có khả năng giải thích khi vấn đáp.
