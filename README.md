# Dự án: Phân tích và xây dựng mô hình dự đoán Khách hàng Rời bỏ của công ty viễn thông

## Tổng quan
Dự án này nhằm xây dựng một hệ thống dự đoán khả năng khách hàng rời bỏ (churn) của một công ty viễn thông bằng cách sử dụng các kỹ thuật học máy. Mục tiêu là phân tích dữ liệu khách hàng, xây dựng mô hình dự đoán và triển khai một ứng dụng web để cung cấp dự đoán dựa trên dữ liệu nhập tay hoặc tệp Excel. Mô hình chính được sử dụng là Hồi quy Logistic, với dữ liệu được chuẩn hóa bằng bộ StandardScaler đã được huấn luyện sẵn. Ngoài ra, dự án sử dụng Power BI để trực quan hóa dữ liệu và phân tích hành vi khách hàng, giúp công ty nhận diện khách hàng có nguy cơ rời bỏ và đưa ra các chiến lược giữ chân hiệu quả.

## Công cụ sử dụng
Dự án sử dụng các công cụ và thư viện sau:
- **Python**: Ngôn ngữ lập trình chính.
- **Pandas và NumPy**: Xử lý và phân tích dữ liệu.
- **Scikit-learn**: Xây dựng và huấn luyện mô hình học máy (Hồi quy Logistic, StandardScaler).
- **Flask**: Tạo ứng dụng web để triển khai mô hình.
- **Joblib**: Lưu và tải mô hình đã huấn luyện.
- **Openpyxl**: Xử lý tệp Excel cho chức năng dự đoán hàng loạt.
- **Matplotlib, Seaborn, Plotly**: Trực quan hóa dữ liệu (trong sổ tay Jupyter).
- **Jupyter Notebook**: Phân tích dữ liệu và huấn luyện mô hình.
- **Power BI**: Trực quan hóa dữ liệu thông qua dashboard, cung cấp các biểu đồ và phân tích chi tiết về hành vi khách hàng.

## Cấu trúc Dự án
- **app.py**: Ứng dụng Flask cung cấp giao diện web và xử lý dự đoán.
- **2121050883_VuVanAn_code.ipynb**: Sổ tay Jupyter chứa phân tích dữ liệu, tiền xử lý và huấn luyện mô hình.
- **best_logreg_model.pkl**: Mô hình Hồi quy Logistic đã được huấn luyện sẵn.
- **scaler.pkl**: Bộ chuẩn hóa StandardScaler đã được huấn luyện sẵn.
- **templates/index.html**: Mẫu HTML cho giao diện web (không được cung cấp nhưng được tham chiếu trong app.py).
- **Data/Customer-Churn.csv**: Tập dữ liệu dùng để huấn luyện (được tham chiếu trong sổ tay).
- **Power BI Dashboard**: Tệp `.pbix` chứa các biểu đồ và phân tích trực quan.

## Tính năng
- **Dự đoán Nhập tay**: Người dùng nhập dữ liệu khách hàng qua biểu mẫu web để dự đoán khả năng rời bỏ.
- **Tải lên Tệp Excel**: Hỗ trợ tải lên tệp Excel chứa dữ liệu khách hàng để dự đoán hàng loạt.
- **Kiểm tra Đầu vào**: Đảm bảo dữ liệu đầu vào khớp với các cột mong đợi và nằm trong phạm vi hợp lệ.
- **Tiền xử lý Dữ liệu**: Xử lý giá trị thiếu, mã hóa biến phân loại (sử dụng LabelEncoder) và chuẩn hóa các đặc trưng số (tenure, MonthlyCharges, TotalCharges).
- **Triển khai Mô hình**: Sử dụng mô hình Hồi quy Logistic đã huấn luyện để dự đoán khách hàng sẽ "Rời bỏ" hoặc "Ở lại".
- **Phân tích bằng Power BI**: Cung cấp các biểu đồ trực quan để phân tích hành vi khách hàng dựa trên các yếu tố như giới tính, độ tuổi, dịch vụ sử dụng, phương thức thanh toán, và hợp đồng.

## Cài đặt
1. Sao chép kho lưu trữ:
   ```bash
   git clone <url-kho-lưu-trữ>
   cd <thư-mục-dự-án>
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
   Các gói cần thiết bao gồm:
   - flask
   - pandas
   - numpy
   - scikit-learn
   - joblib
   - openpyxl
3. Đảm bảo các tệp sau nằm trong thư mục dự án:
   - `best_logreg_model.pkl`
   - `scaler.pkl`
   - `templates/index.html`
4. Chạy ứng dụng Flask:
   ```bash
   python app.py
   ```
5. Cài đặt Power BI Desktop (nếu chưa có) và mở tệp `.pbix` để xem dashboard.

## Cách sử dụng
1. **Chạy ứng dụng**: Sau khi chạy `app.py`, truy cập giao diện web tại `http://localhost:5000`.
2. **Nhập tay dữ liệu**: Điền thông tin khách hàng vào biểu mẫu web và nhấn gửi để nhận dự đoán.
3. **Tải lên Excel**: Tải lên tệp Excel chứa dữ liệu khách hàng với các cột khớp với danh sách đặc trưng (`gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`). Kết quả dự đoán sẽ được hiển thị trên giao diện.
4. **Xem phân tích Power BI**: Mở tệp dashboard Power BI để xem các biểu đồ phân tích hành vi khách hàng.

## Dữ liệu
Tập dữ liệu `Customer-Churn.csv` bao gồm 7043 bản ghi với 21 cột, trong đó:
- **customerID**: Mã khách hàng.
- **gender**: Giới tính (Nam/Nữ).
- **SeniorCitizen**: Người cao tuổi (0: Không, 1: Có).
- **Partner, Dependents**: Tình trạng bạn đời và người phụ thuộc (Yes/No).
- **tenure**: Số tháng khách hàng sử dụng dịch vụ.
- **PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies**: Các dịch vụ khách hàng sử dụng.
- **Contract**: Loại hợp đồng (Month-to-month, One year, Two year).
- **PaperlessBilling**: Thanh toán không dùng giấy (Yes/No).
- **PaymentMethod**: Phương thức thanh toán.
- **MonthlyCharges, TotalCharges**: Chi phí hàng tháng và tổng chi phí.
- **Churn**: Nhãn mục tiêu (Yes: Rời bỏ, No: Ở lại).

Dữ liệu được tiền xử lý bằng cách mã hóa các biến phân loại và chuẩn hóa các biến số, sau đó được sử dụng để huấn luyện mô hình và phân tích trong Power BI.

## Phân tích Power BI
Dashboard Power BI cung cấp các phân tích chi tiết về hành vi khách hàng, bao gồm:
- **Tổng quan về khách hàng**:
  - Tổng số khách hàng: 7043.
  - Số khách hàng rời bỏ: 1869 (26,54%).
  - Số khách hàng ở lại: 5174.
- **Phân tích theo giới tính**:
  - Phân bố: 50,48% Nữ, 49,52% Nam.
  - Tỷ lệ rời bỏ không có sự khác biệt đáng kể giữa hai giới.
- **Phân tích theo SeniorCitizen**:
  - 29,96% là người cao tuổi (Yes), 70,04% không phải (No).
  - Tỷ lệ rời bỏ cao hơn ở nhóm người cao tuổi.
- **Phân tích theo InternetService**:
  - Phân bố: 3096 (Fiber optic), 2421 (DSL), 1526 (No).
  - Tỷ lệ rời bỏ cao nhất ở khách hàng sử dụng Fiber optic (41,89%).
- **Phân tích theo Contract**:
  - Phân bố: 3875 (Month-to-month), 1695 (One year), 1473 (Two year).
  - Tỷ lệ rời bỏ cao nhất ở hợp đồng Month-to-month (42,71%).
- **Phân tích theo PaymentMethod**:
  - Phân bố: 2365 (Electronic check), 1612 (Mailed check), 1544 (Bank transfer), 1522 (Credit card).
  - Tỷ lệ rời bỏ cao nhất ở khách hàng sử dụng Electronic check (45,29%).
- **Phân tích theo StreamingTV**:
  - Phân bố: 2810 (Yes), 2707 (No), 1526 (No internet).
  - Tỷ lệ rời bỏ cao hơn ở nhóm sử dụng StreamingTV (30,07%).

## Kết quả
- Mô hình Hồi quy Logistic được chọn sau khi thử nghiệm nhiều mô hình (Logistic Regression, SVM, Decision Tree, Random Forest, XGBoost, v.v.) dựa trên độ chính xác, precision và recall.
- Ứng dụng web cung cấp giao diện thân thiện để dự đoán, với khả năng xử lý lỗi và kiểm tra dữ liệu đầu vào.
- Dashboard Power BI cung cấp cái nhìn trực quan về hành vi khách hàng, giúp xác định các yếu tố chính ảnh hưởng đến tỷ lệ rời bỏ (như loại hợp đồng và phương thức thanh toán).
