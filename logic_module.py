import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import os
import time

AI_MODEL = None
AI_SCALER = None
MODEL_COLUMNS = None

# Hệ số tăng trưởng cuối tuần (Bạn có thể điều chỉnh con số 1.4 này)
WEEKEND_FACTOR = 1.4 

def init_brain():
    global AI_MODEL, AI_SCALER, MODEL_COLUMNS
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

def predict_revenue_advanced(user_input_dict):
    global AI_MODEL, AI_SCALER, MODEL_COLUMNS
    
    if not AI_MODEL:
        raise ValueError("AI chưa được huấn luyện!")
        
    time.sleep(1) 
    
    # 1. Dự đoán doanh thu cơ sở (Ngày thường)
    df_new = pd.DataFrame([user_input_dict])
    df_new = pd.get_dummies(df_new, columns=['Vi_tri'])
    df_new = df_new.reindex(columns=MODEL_COLUMNS, fill_value=0)
    X_new_scaled = AI_SCALER.transform(df_new)
    
    rev_weekday = AI_MODEL.predict(X_new_scaled)[0]
    
    # 2. Tính toán theo logic kinh doanh thực tế
    # Tổng doanh thu 22 ngày thường
    total_weekday = rev_weekday * 22
    
    # Doanh thu ngày cuối tuần (nhân hệ số)
    rev_weekend = rev_weekday * WEEKEND_FACTOR
    
    # Tổng doanh thu 8 ngày cuối tuần
    total_weekend = rev_weekend * 8
    
    # Tổng doanh thu tháng
    total_month = total_weekday + total_weekend
    
    return {
        'weekday_single': rev_weekday,
        'weekend_single': rev_weekend,
        'total_month': total_month
    }