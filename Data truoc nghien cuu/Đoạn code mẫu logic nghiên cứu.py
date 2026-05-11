# Lập trình hồi quy tuyến tính 2026.05.
# 1. Khai báo thư viện
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Hỗ trợ hiển thị tiếng Việt trên biểu đồ (nếu cần)
plt.rcParams['axes.unicode_minus'] = False 

# 2. Đọc dữ liệu
data = pd.read_csv('Data_Du_Doan_Doanh_Thu_Full.csv')

# 3. Tiền xử lý dữ liệu
# Chuyển đổi cột 'Vi_tri' thành số (One-Hot Encoding)
data_processed = pd.get_dummies(data, columns=['Vi_tri'])
data_processed = data_processed.astype(float) # Đảm bảo mọi thứ đều là số thực

# 4. Xác định Input (X) và Output (y)
X = data_processed.drop(['Doanh_Thu_Ngay', 'Doanh_Thu_Thang'], axis=1)
y = data_processed['Doanh_Thu_Ngay']

# Lấy danh sách tên các yếu tố để vẽ biểu đồ sau này
feature_names = X.columns

# 5. Chia tập Train / Test (80% học - 20% thi)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 6. CHUẨN HÓA DỮ LIỆU (FEATURE SCALING) - BƯỚC ĂN ĐIỂM
# ==========================================
scaler = StandardScaler()
# Chỉ "học" (fit) tỷ lệ trên tập Train để tránh rò rỉ dữ liệu, sau đó áp dụng (transform) cho cả Train và Test
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Huấn luyện mô hình
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 8. Đánh giá mô hình
print(f"Độ chính xác (R2) trên tập Train: {model.score(X_train_scaled, y_train):.4f}")
print(f"Độ chính xác (R2) trên tập Test: {model.score(X_test_scaled, y_test):.4f}")
print("-" * 50)

# ==========================================
# 9. TRÍCH XUẤT VÀ SẮP XẾP MỨC ĐỘ QUAN TRỌNG
# ==========================================
# Lấy trọng số (coefficients) từ mô hình
importance = pd.DataFrame({
    'Yeu_To': feature_names,
    'Trong_So': model.coef_
})

# Lấy trị tuyệt đối để biết sức ảnh hưởng thực sự (bất kể là tác động tăng hay giảm doanh thu)
importance['Muc_Do_Anh_Huong'] = importance['Trong_So'].abs()
# Sắp xếp từ cao xuống thấp
importance = importance.sort_values(by='Muc_Do_Anh_Huong', ascending=False)

print("BẢNG XẾP HẠNG MỨC ĐỘ ẢNH HƯỞNG CỦA CÁC YẾU TỐ:")
print(importance[['Yeu_To', 'Trong_So', 'Muc_Do_Anh_Huong']])

# ==========================================
# 10. VẼ BIỂU ĐỒ BÁO CÁO (DÀNH CHO SLIDE)
# ==========================================
plt.figure(figsize=(14, 6))

# ---- Biểu đồ 1: Thực tế vs Dự đoán (Đánh giá độ chuẩn của AI) ----
plt.subplot(1, 2, 1)
y_pred = model.predict(X_test_scaled)
plt.scatter(y_test, y_pred, color='dodgerblue', alpha=0.7, edgecolors='k')
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
plt.title('Độ Khớp: Thực Tế vs Dự Đoán', fontsize=14)
plt.xlabel('Doanh Thu Thực Tế (VNĐ)', fontsize=12)
plt.ylabel('Doanh Thu Dự Đoán (VNĐ)', fontsize=12)

# ---- Biểu đồ 2: Mức độ ảnh hưởng của các yếu tố (Feature Importance) ----
plt.subplot(1, 2, 2)
sns.barplot(x='Muc_Do_Anh_Huong', y='Yeu_To', data=importance, palette='viridis')
plt.title('Mức Độ Ảnh Hưởng Của Từng Yếu Tố', fontsize=14)
plt.xlabel('Trọng số đã chuẩn hóa (Càng dài càng quan trọng)', fontsize=12)
plt.ylabel('Các biến đầu vào', fontsize=12)

plt.tight_layout()
plt.show()