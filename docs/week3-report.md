# BÁO CÁO TIẾN ĐỘ TUẦN 3

**Nhóm:** Serverless  
**Môn học:** Điện toán đám mây  
**Mã môn học:** CLCO332779_05UTExMC  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Đề tài:** Xây dựng chatbot hỏi đáp FAQ môn học dựa trên tìm kiếm từ khóa/TF-IDF chạy trên AWS Lambda.  
**Repository:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud  
**Link báo cáo tuần 3:** https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week3-report.md 
**Ngày tổng hợp minh chứng:** 25/10/2026.

## 1. Thông tin thành viên

| MSSV | Họ và tên | Vai trò |
| --- | --- | --- |
| 24110253 | Đặng Nguyễn Minh Khoa | Nhóm trưởng |
| 24110166 | Ngô Anh Bằng | Thành viên |

## 2. Mục tiêu tuần 3

Tiếp tục hệ thống tuần 2, nhóm tập trung tích hợp, bảo mật, giám sát và tự động hóa kiểm thử: đánh giá ngưỡng TF-IDF; bổ sung nguồn trả lời và mã tra cứu; theo dõi yêu cầu qua API Gateway, Lambda và DynamoDB; giới hạn truy cập S3; cấu hình CORS, throttling, CloudWatch Logs, metric và alarm. Hệ thống tiếp tục tự cài đặt thuật toán tìm kiếm, không gọi API LLM bên ngoài.

Các tài nguyên trong ảnh minh chứng thuộc Account `550609224402`, Region `us-east-1`.

| Thành phần | Tài nguyên/cấu hình |
| --- | --- |
| S3 dữ liệu | `course-faq-data-24110253`, object `faq.json`, 24 FAQ |
| S3 website | `course-faq-web-24110253` |
| Lambda | `course-faq-lambda`, build `week3-v1` |
| HTTP API | `course-faq-api`, ID `tijvqgrltk`, stage `$default` |
| API endpoint | `https://tijvqgrltk.execute-api.us-east-1.amazonaws.com` |
| DynamoDB | `CourseFAQQueryLogs`, partition key `requestId` |
| Lambda log group | `/aws/lambda/course-faq-lambda` |
| API access log group | `/aws/apigateway/course-faq-api`, lưu log 7 ngày |
| Metric và alarm | `CourseFAQChatbot/ApplicationErrors`; `CourseFAQ-ApplicationErrors` |

## 3. Kết quả thực hiện và phân công công việc

### 3.1. Đặng Nguyễn Minh Khoa (24110253)

**Công việc 1: Hoàn thiện Lambda và đánh giá ngưỡng tìm kiếm**

- **Thời gian:** 4 giờ.
- Giữ thuật toán TF-IDF và Cosine Similarity tự cài đặt; tăng kiểm tra đầu vào, giới hạn câu hỏi 500 ký tự và body 4096 byte.
- Bổ sung `source`, `category`, `requestId`, `apiRequestId`, `build`, `threshold`, `faqCount`, `faqETag` và `logSaved` trong phản hồi theo từng trường hợp.
- Dùng tập dev 10 câu để so sánh các ngưỡng; chọn `SIMILARITY_THRESHOLD=0.60` nhằm giảm trả nhầm câu ngoài phạm vi. Tập test riêng đạt 9/10, còn một câu có đáp án bị bỏ sót.
- AWS phản hồi xác nhận ngưỡng `0.6`, 24 FAQ và build `week3-v1`; ngưỡng mặc định trong mã vẫn là `0.30` khi không có biến môi trường.

Minh chứng:

- Mã nguồn Lambda: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/backend/lambda_function.py
- Kết quả test ở ngưỡng 0.60: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/TFIDF_Week3_Test_Selected_Threshold.png
- So sánh các ngưỡng trên tập dev: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/TFIDF_Week3_Dev_Threshold_Comparison.png
- Kết quả đánh giá trên tập dev: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week3/search-eval-dev-results.json
- Kết quả đánh giá trên tập test: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week3/search-eval-test-results.json
git ls-remote origin refs/heads/main
**Công việc 2: Thiết lập log có cấu trúc và cảnh báo lỗi ứng dụng**

- **Thời gian:** 2 giờ.
- Lambda phát log JSON `request_complete`, có `applicationError`, trạng thái HTTP, thời gian xử lý và mã tra cứu; không đưa câu hỏi vào dòng CloudWatch này.
- Bật API access logging tới `/aws/apigateway/course-faq-api` và cấu hình metric filter trên log group Lambda:

  ```text
  { $.event = "request_complete" && $.applicationError = 1 }
  ```

- Metric `ApplicationErrors`: giá trị lỗi `1`, mặc định `0`, không có dimension. Alarm dùng `Sum`, chu kỳ 1 phút, ngưỡng `>=1`, 1/1 datapoint, missing data là `notBreaching`, không cấu hình gửi email.
- Kiểm thử lỗi ghi DynamoDB cho thấy Lambda vẫn trả câu trả lời nhưng `logSaved=false`, `applicationError=1`, `errorStage=dynamodb`. Sau khôi phục, `logSaved=true` và `applicationError=0`.
- Lịch sử ghi nhận **OK → ALARM lúc 17:09:37 UTC ngày 24/10/2026**, rồi **ALARM → OK lúc 17:11:37 UTC**; tương ứng **00:09:37 và 00:11:37 ngày 25/10/2026 (UTC+7)**.

Minh chứng:

- Lịch sử ALARM và phục hồi OK: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_Application_Alarm_History.png
- Cấu hình filter, alarm, access log và hai lần thử lỗi/phục hồi: 
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_Application_Error_Filter.png
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_Application_Alarm_Config.png
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/API_Gateway_Week3_Access_Logging_Settings.png
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_API_Access_Log.png
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/Lambda_Week3_DynamoDB_Error_Test.png
    - https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/Lambda_Week3_DynamoDB_Recovered.png

**Công việc 3: Cấu hình Dashboard giám sát hệ thống**

- **Thời gian:** 1 giờ.
- Tạo `CourseFAQ-Week3-Dashboard` gồm sáu biểu đồ: Lambda Invocations, Duration, Errors/Throttles; API Gateway Count, Latency; ApplicationErrors.
- Quan sát được dữ liệu thực trên Dashboard, tách lỗi ứng dụng đã xử lý khỏi lỗi thực thi Lambda.
- Giám sát được cấu hình và kiểm tra trên AWS Console. Tự động hóa kiểm thử đã có minh chứng chạy từ máy tính; chưa có minh chứng triển khai toàn bộ hệ thống bằng IaC.

Minh chứng:

- Dashboard CloudWatch: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_Dashboard.png
- Định dạng API access log: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/config/api-access-log-format.txt

**Công việc 4: Giới hạn truy cập S3 và cấu hình API**

- **Thời gian:** 1 giờ.
- Đặt default route throttling của stage `$default`: rate `5` yêu cầu/giây, burst `10`. Ảnh xác nhận cấu hình; chưa có phép thử tải chứng minh HTTP 429.
- Thu hẹp bucket policy website chỉ cấp public `s3:GetObject` cho `index.html`, `style.css`, `script.js`, `config.js`.
- Bucket dữ liệu bật Block Public Access; yêu cầu anonymous tới `faq.json` nhận HTTP 403 trong khi luồng hỏi đáp vẫn đọc được FAQ qua Lambda.
- CORS cho phép đúng origin website S3 và header `content-type`; preflight từ `https://example.invalid` không được cấp header cho phép origin. Danh sách method quan sát còn rộng hơn mục tiêu GET/POST/OPTIONS, được ghi nhận trong mục 5.4.

Minh chứng:

- Throttling rate 5, burst 10: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/API_Gateway_Week3_Throttling_Settings.png
- Policy website chỉ đọc bốn file: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/S3_Week3_Web_Restricted_Policy.png
- FAQ từ chối truy cập anonymous: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/S3_Week3_FAQ_Anonymous_Access_Denied.png

### 3.2. Ngô Anh Bằng (24110166)

**Công việc 1: Cập nhật frontend hiển thị nguồn và mã tra cứu**

- **Thời gian:** 3 giờ.
- Kế thừa giao diện tuần 2, cập nhật câu hỏi gợi ý theo bộ FAQ đang dùng; hiển thị nguồn câu trả lời và mã tra cứu từ backend.
- Triển khai frontend lên S3; kiểm thử câu hỏi `Nhóm được sử dụng những Region nào?` nhận `FAQ017`, similarity `1.0`.
- Kiểm tra trên trình duyệt thấy POST `/chat` trả HTTP 200 và `Access-Control-Allow-Origin` đúng origin website sau cấu hình bảo mật.

Minh chứng:

- Website trả lời và CORS đúng origin: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/Frontend_Week3_CORS_Allowed.png
- Mã frontend mới: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/tree/main/frontend

**Lưu ý đồng bộ mã nguồn:** ảnh website S3 chứng minh đã hiển thị nguồn và mã tra cứu. Tuy nhiên, `frontend/script.js` trên GitHub hiện chưa có xử lý `source` và `requestId`; cần cập nhật bản frontend đã triển khai lên repo. Liên kết thư mục trên dùng để đối chiếu trạng thái mã, chưa chứng minh bản Git đã khớp đầy đủ giao diện trong ảnh.

**Công việc 2: Đối soát yêu cầu giữa API, Lambda và DynamoDB**

- **Thời gian:** 2 giờ.
- Dùng `requestId` của Lambda làm khóa truy vấn DynamoDB và lọc log `request_complete`; lưu `apiRequestId` riêng để liên hệ với API access log.
- Ca `exact-FAQ017` trong kết quả API có `requestId=5a4aa5a8-f815-4f0e-88a7-b0acb02ac62e`, `apiRequestId=FwtHViCpIAMEPpg=`.
- Ảnh DynamoDB trả về một item đúng mã; ảnh CloudWatch Lambda thể hiện cùng hai mã, `matchedFaqId=FAQ017`, `logSaved=true`, `applicationError=0`.

Minh chứng:

- Bản ghi DynamoDB theo requestId: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/DynamoDB_Week3_API_Test_Record.png
- Log Lambda tương ứng: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/CloudWatch_Week3_API_Test_Trace.png

**Công việc 3: Chạy bộ kiểm thử API trên AWS**

- **Thời gian:** 1 giờ.
- Chạy `scripts/test-api.py` từ thư mục kit trên máy tính, gọi HTTPS endpoint thật của API Gateway; lưu kết quả vào `docs/week3-api-results.json` của kit. Ảnh terminal thể hiện lệnh chạy, mã thoát `0` và bảng PASS; hai file này chưa có trên repository hiện tại.
- Kết quả **13/13 ca đạt**, gồm hỏi đáp, câu không dấu, không khớp, đầu vào lỗi, giới hạn kích thước, route không tồn tại và CORS preflight.
- Ảnh terminal ghi thời gian đối soát sau khi chạy là **01:14:59 ngày 25/10/2026 (UTC+7)**.

Minh chứng:

- Kết quả kiểm thử API 13/13: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/screenshots/week3/API_Week3_Automated_Test_Results.png
- Test event HTTP có đáp án: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/config/lambda-test-http.json
- Test event câu không khớp: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/config/lambda-test-unmatched.json

Hai test event hỗ trợ kiểm thử thủ công; kết quả 13/13 được minh chứng bằng ảnh chạy script ở trên.

**Công việc 4: Tổng hợp minh chứng và chuẩn bị hồ sơ tuần 3**

- **Thời gian:** 2 giờ.
- Tổng hợp 24 ảnh trong `screenshots/week3/`; báo cáo liên kết trực tiếp 11 ảnh chính, các ảnh hỗ trợ còn lại nằm trong cùng thư mục.
- Đưa mã Lambda, test event, S3 policy, định dạng API access log và báo cáo tuần 3 lên GitHub. Script/JSON đánh giá và bản frontend mới trên S3 còn cần đồng bộ để hoàn thiện hồ sơ mã nguồn.
- Tổng hợp phân công và số giờ của từng thành viên; cần bổ sung nhật ký chi tiết theo buổi và minh chứng tag tài nguyên giám sát mới trước khi nộp.

Minh chứng:

- Thư mục bộ ảnh tuần 3: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/tree/main/screenshots/week3
- Báo cáo tuần 3: https://github.com/khoalkopwk-ship-it/Build_Chatbot_Cloud/blob/main/docs/week3-report.md

## 4. Tổng hợp thời gian thực hiện

| MSSV | Thành viên | Nhóm công việc | Thời gian thực tế (giờ) |
| --- | --- | ---: | --- |
| 24110253 | Đặng Nguyễn Minh Khoa | 4 | 8 |
| 24110166 | Ngô Anh Bằng | 4 | 8 |
| **Tổng cộng** | | **8** | **16 giờ** |

> Ghi chú: Số giờ do nhóm ghi nhận trong báo cáo là 8 giờ/người, đáp ứng mức tối thiểu 8 giờ/sinh viên/tuần.

## 5. Kết quả đạt được

### 5.1. Đánh giá chất lượng tìm kiếm

| Tập | Ngưỡng | Đúng/tổng | Trả nhầm câu ngoài kho | Bỏ sót câu có đáp án |
| --- | ---: | ---: | ---: | ---: |
| Dev | 0.30 | 8/10 | 1 | 1 |
| Dev | 0.45 | 8/10 | 1 | 1 |
| Dev | 0.60 | 8/10 | 0 | 2 |
| Dev | 0.70 | 6/10 | 0 | 4 |
| Test riêng | 0.60 | 9/10 | 0 | 1 |

Ở ngưỡng 0.60, câu ngoài kho `Thời gian nghỉ tết là bao lâu?` có điểm 0.5485 được từ chối. Đánh đổi là bỏ sót một số câu có đáp án; tập test còn câu `Tài nguyên cần chạy ở đâu?` có nhãn FAQ023 nhưng điểm 0.5644 nên chưa đạt ngưỡng.

### 5.2. Kết quả kiểm thử API thực tế

| Ca kiểm thử | HTTP thực tế | Kết quả |
| --- | ---: | --- |
| `health` | 200 | PASS |
| `exact-FAQ017` | 200 | PASS, đúng FAQ017, lưu log thành công |
| `no-accents` | 200 | PASS, đúng FAQ017 |
| `unmatched` | 200 | PASS, không khớp và vẫn lưu log |
| `empty`, `missing`, `number`, `array` | 400 | PASS từng ca |
| `too-long`, `bad-json` | 400 | PASS từng ca |
| `too-large` | 413 | PASS |
| `unknown-route` | 404 | PASS |
| `cors-preflight` | 204 | PASS theo các điều kiện script đang kiểm tra |

Tổng cộng 13 ca đạt. HTTP 400/404/413 là kết quả mong đợi trong các ca đầu vào lỗi. Script CORS hiện xác nhận có POST và content-type, không kiểm tra danh sách method chỉ gồm GET/POST/OPTIONS. `/health` kiểm tra khả năng phản hồi của Lambda; ca hỏi đáp và đối soát mới kiểm tra thêm S3/DynamoDB.

### 5.3. Kết quả tích hợp và giám sát

Luồng đã có minh chứng: `Website S3 → HTTP API → Lambda TF-IDF → S3 FAQ → DynamoDB → phản hồi website`; log Lambda và API hỗ trợ tra cứu bằng hai mã tương ứng. CloudWatch phát hiện được lỗi ghi DynamoDB và lịch sử cảnh báo thể hiện chuyển ALARM rồi phục hồi OK.

Dòng log Lambda của ca `exact-FAQ017` ghi `durationMs=7964.59`, có thể đối chiếu trực tiếp trong ảnh log ở mục 3.2, Công việc 2. Đây là thời gian ứng dụng ghi nhận của một yêu cầu, không phải thời gian phía trình duyệt hoặc benchmark toàn hệ thống; cần phân tích độ trễ trong tuần 4.

### 5.4. Hạn chế và phần cần hoàn thiện

- API access log có retention 7 ngày; ảnh log group Lambda tại thời điểm tạo filter vẫn là **Never expire**.
- Kho 24 FAQ chủ yếu phản ánh yêu cầu đề tài, chưa chứng minh bao phủ nội dung giáo trình/slide môn học. Cần bổ sung tài liệu được phép và ghi nguồn chương/trang/slide đúng thực tế.
- Website S3 hiện dùng HTTP; CORS không phải cơ chế xác thực. Chưa có minh chứng đã thu hẹp quyền LabRole, triển khai IaC toàn hệ thống, đo chi phí hoặc dọn dẹp sau phiên này.

## 6. Kế hoạch tuần 4

- Bổ sung FAQ từ tài liệu môn học được giảng viên cho phép; chuẩn bị câu đánh giá độc lập và phân tích các ca bỏ sót.
- Kiểm thử tổng thể, phân tích thời gian đọc S3/ghi DynamoDB và tối ưu theo số liệu đo được.
- Tổng hợp chi phí, sơ đồ kiến trúc, nhật ký thực tế; quay video demo tối đa 10 phút.

## 7. Kết luận

Tuần 3 đã có minh chứng cho tích hợp frontend–API–Lambda–S3–DynamoDB, kiểm thử API đạt 13/13, chọn ngưỡng TF-IDF 0.60 trên tập dev và kiểm tra tập test đạt 9/10. Nhóm đã bổ sung truy vết yêu cầu, bảo vệ kho FAQ, giới hạn policy website, thiết lập throttling, Dashboard và kiểm thử cảnh báo lỗi ứng dụng có phục hồi.

## 8. Ghi nhận việc sử dụng AI hỗ trợ

ChatGPT hỗ trợ tham khảo mã Python/JavaScript, script đánh giá và kiểm thử, hướng dẫn cấu hình AWS, đối chiếu minh chứng. Việc tạo tài nguyên AWS, triển khai và thử nghiệm hệ thống được thực hiện trên AWS Academy Learner Lab của nhóm. Các thành viên cần kiểm tra mã nguồn, nắm rõ cấu hình và có khả năng giải thích khi vấn đáp.