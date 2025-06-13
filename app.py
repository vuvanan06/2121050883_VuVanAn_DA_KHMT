from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Tải mô hình học máy đã lưu (Logistic Regression)
model = joblib.load('best_logreg_model.pkl')

# Tải bộ scaler đã lưu (dùng để chuẩn hóa dữ liệu đầu vào)
try:
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    scaler = None

# Danh sách các cột đầu vào của mô hình
cols = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
    'MonthlyCharges', 'TotalCharges'
]

# Giá trị hợp lệ cho từng cột (dùng để kiểm tra đầu vào)
valid_ranges = {
    'gender': [0, 1],
    'SeniorCitizen': [0, 1],
    'Partner': [0, 1],
    'Dependents': [0, 1],
    'tenure': [0, None],  # tenure >= 0
    'PhoneService': [0, 1],
    'MultipleLines': [0, 1],
    'InternetService': [0, 1, 2],
    'OnlineSecurity': [0, 1],
    'OnlineBackup': [0, 1],
    'DeviceProtection': [0, 1],
    'TechSupport': [0, 1],
    'StreamingTV': [0, 1],
    'StreamingMovies': [0, 1],
    'Contract': [0, 1, 2],
    'PaperlessBilling': [0, 1],
    'PaymentMethod': [0, 1, 2, 3],
    'MonthlyCharges': [0, None],  # >= 0
    'TotalCharges': [0, None]     # >= 0
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    input_values = None
    excel_results = None
    error = None

    if request.method == 'POST':
        # Trường hợp người dùng upload file Excel
        if 'excel_file' in request.files and request.files['excel_file'].filename != '':
            file = request.files['excel_file']
            if file.filename.endswith(('.xlsx', '.xls')):
                try:
                    # Đọc file Excel
                    df = pd.read_excel(file)

                    # Kiểm tra thiếu hoặc dư cột
                    missing_cols = [col for col in cols if col not in df.columns]
                    extra_cols = [col for col in df.columns if col not in cols and col != 'Prediction']
                    if missing_cols or extra_cols:
                        error = f"File Excel không khớp với danh sách cột. Thiếu: {', '.join(missing_cols) if missing_cols else 'Không'}. Thừa: {', '.join(extra_cols) if extra_cols else 'Không'}."
                    else:
                        # Kiểm tra giá trị thiếu
                        if df[cols].isna().any().any():
                            error = "File Excel chứa ô trống hoặc giá trị không hợp lệ"
                        else:
                            # Lọc dòng hợp lệ
                            invalid_rows = []
                            valid_df = pd.DataFrame(columns=cols)
                            for index, row in df.iterrows():
                                is_valid = True
                                invalid_values = {}
                                for col in cols:
                                    value = row[col]
                                    valid_range = valid_ranges[col]
                                    if valid_range[1] is None:  # Không giới hạn trên
                                        if pd.notna(value) and value < valid_range[0]:
                                            is_valid = False
                                            invalid_values[col] = value
                                    else:
                                        if pd.notna(value) and value not in valid_range:
                                            is_valid = False
                                            invalid_values[col] = value
                                if is_valid:
                                    valid_df = pd.concat([valid_df, pd.DataFrame([row])], ignore_index=True)
                                else:
                                    # Lưu thông tin dòng không hợp lệ (thêm +2 để trùng Excel)
                                    invalid_rows.append((index + 2, invalid_values))

                            if not valid_df.empty:
                                df_original = valid_df.copy()

                                # Chuẩn hóa các cột nếu có scaler
                                if scaler:
                                    cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
                                    valid_df[cols_to_scale] = scaler.transform(valid_df[cols_to_scale])

                                # Dự đoán
                                predictions = model.predict(valid_df[cols])
                                df_original['Prediction'] = ['Rời bỏ' if pred == 1 else 'Ở lại' for pred in predictions]

                                # Chuẩn bị kết quả hiển thị
                                excel_results = df_original.to_dict(orient='records')
                            else:
                                error = "Không có dòng nào trong file Excel hợp lệ để dự đoán."

                            # Hiển thị chi tiết các dòng không hợp lệ
                            if invalid_rows:
                                error_msg = "Các dòng không hợp lệ trong file Excel (dòng số, giá trị không hợp lệ): "
                                error_msg += "; ".join([
                                    f"Dòng {row[0]}: {', '.join([f'{k}: {v}' for k, v in row[1].items()])}"
                                    for row in invalid_rows
                                ])
                                error = (error + " " + error_msg) if error else error_msg

                except Exception as e:
                    error = f"Lỗi khi đọc file Excel: {str(e)}"
            else:
                error = "Vui lòng tải lên file Excel (.xlsx hoặc .xls)"

        # Trường hợp người dùng nhập tay
        else:
            values = []
            input_values = {}
            try:
                # Kiểm tra xem người dùng đã nhập ít nhất một trường chưa
                form_filled = False
                for col in cols:
                    value = request.form.get(col)
                    if value and value.strip() != '':
                        form_filled = True
                        break
                
                if form_filled:
                    
                    for col in cols:
                        value = request.form.get(col)
                        if value is None or value.strip() == '':
                            error = f"Thiếu giá trị cho {col}"
                            return render_template('index.html', cols=cols, error=error)

                        value = float(value)
                        valid_range = valid_ranges[col]
                        if valid_range[1] is None:
                            if value < valid_range[0]:
                                error = f"Giá trị cho {col} phải lớn hơn hoặc bằng {valid_range[0]}"
                                return render_template('index.html', cols=cols, error=error)
                        else:
                            if value not in valid_range:
                                error = f"Giá trị cho {col} phải là {valid_range}"
                                return render_template('index.html', cols=cols, error=error)
                        input_values[col] = str(value)
                        values.append(value)

                    # Dự đoán từ dữ liệu nhập tay
                    sample = pd.DataFrame([values], columns=cols)
                    if scaler:
                        cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
                        sample[cols_to_scale] = scaler.transform(sample[cols_to_scale])
                    pred = model.predict(sample)
                    prediction = "Rời bỏ" if pred[0] == 1 else "Ở lại"
            except ValueError:
                error = "Vui lòng nhập đúng định dạng số cho tất cả các trường"

    # Hiển thị trang web với kết quả (nếu có)
    return render_template('index.html', cols=cols, prediction=prediction, input_values=input_values, excel_results=excel_results, error=error)

if __name__ == '__main__':
    # Chạy ứng dụng Flask ở chế độ debug
    app.run(debug=True)
