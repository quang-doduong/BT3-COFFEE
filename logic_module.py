import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import os
import time

# Biến toàn cục lưu trữ mô hình trong bộ nhớ
AI_MODEL = None
AI_SCALER = None
MODEL_COLUMNS = None

def init_brain():
    """Hàm này sẽ được gọi lúc mở App để train AI sẵn"""
    global AI_MODEL, AI_SCALER, MODEL_COLUMNS
    
    # Giả định file CSV nằm cùng thư mục
    csv_path = os.path.join(os.path.dirname(__file__), 'Data_Du_Doan_Doanh_Thu_Full.csv')
    
    try:
        data = pd.read_csv(csv_path)
        data_processed = pd.get_dummies(data, columns=['Vi_tri'])
        data_processed = data_processed.astype(float)
        
        X = data_processed.drop(['Doanh_Thu_Ngay', 'Doanh_Thu_Thang'], axis=1)
        y = data_processed['Doanh_Thu_Ngay']
        
        MODEL_COLUMNS = list(X.columns)
        
        AI_SCALER = StandardScaler()
        X_scaled = AI_SCALER.fit_transform(X)
        
        AI_MODEL = LinearRegression()
        AI_MODEL.fit(X_scaled, y)
        return True
    except Exception as e:
        print(f"Lỗi khởi tạo AI: {e}")
        return False

def predict_revenue(user_input_dict):
    """Hàm nhận data từ UI và trả về dự đoán"""
    global AI_MODEL, AI_SCALER, MODEL_COLUMNS
    
    if not AI_MODEL:
        raise ValueError("AI chưa được huấn luyện! Thiếu file dữ liệu.")
        
    # Giả lập delay một chút để UI chạy hiệu ứng "Đang phân tích..." cho chuyên nghiệp
    time.sleep(1.2) 
    
    df_new = pd.DataFrame([user_input_dict])
    df_new = pd.get_dummies(df_new, columns=['Vi_tri'])
    
    # Khớp cột tự động
    df_new = df_new.reindex(columns=MODEL_COLUMNS, fill_value=0)
    
    X_new_scaled = AI_SCALER.transform(df_new)
    
    doanh_thu_ngay = AI_MODEL.predict(X_new_scaled)[0]
    doanh_thu_thang = doanh_thu_ngay * 30
    
    return doanh_thu_ngay, doanh_thu_thang