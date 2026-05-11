import customtkinter as ctk
import threading
import os
from tkinter import messagebox
from PIL import Image
import logic_module

# Quản lý đường dẫn tài nguyên
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets") # Nhét toàn bộ vào folder assets

# Đổi tên file cho rõ nghĩa
PATH_BANNER = os.path.join(ASSETS_DIR, "banner.png")
PATH_REPORT = os.path.join(ASSETS_DIR, "report_logo.png")

FONT_LABEL = ("Segoe UI", 13, "bold")
FONT_V = ("Segoe UI", 15)

class MilkTeaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Dự Đoán Doanh Thu - Professional Edition")
        self.geometry("1150x800")
        
        # Khởi tạo dữ liệu ảnh
        self.img_report = None
        if os.path.exists(PATH_REPORT):
            self.img_report = ctk.CTkImage(Image.open(PATH_REPORT), size=(350, 200))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if not logic_module.init_brain():
            messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu huấn luyện!")

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        self.left_frame = ctk.CTkScrollableFrame(self, width=450, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Banner quảng cáo/logo
        if os.path.exists(PATH_BANNER):
            img_banner = ctk.CTkImage(Image.open(PATH_BANNER), size=(420, 160))
            ctk.CTkLabel(self.left_frame, text="", image=img_banner).pack(pady=(0, 20))

        ctk.CTkLabel(self.left_frame, text="THÔNG SỐ ĐẦU VÀO", font=("Segoe UI", 20, "bold"), text_color="#3a7ebf").pack(pady=10)

        # Các ô nhập liệu có nhãn bên ngoài
        self.entry_gia = self.create_labeled_entry("Giá trung bình 1 ly (VNĐ):", "Ví dụ: 35000")
        self.entry_khach = self.create_labeled_entry("Lượng khách dự kiến / ngày:", "Ví dụ: 120")
        self.entry_dt = self.create_labeled_entry("Diện tích quán (m2):", "Ví dụ: 45.5")
        self.entry_nv = self.create_labeled_entry("Số lượng nhân viên:", "Ví dụ: 3")
        self.entry_doithu = self.create_labeled_entry("Số đối thủ (bán kính 500m):", "Ví dụ: 5")

        # Khu vực chọn Vị trí
        self.create_section_label("Vị trí mặt bằng:")
        self.combo_vitri = ctk.CTkComboBox(self.left_frame, values=["Gần trường", "Văn phòng", "Khu dân cư"], 
                                           font=FONT_V, height=45, command=self.reset_button)
        self.combo_vitri.pack(fill="x", padx=30, pady=(0, 15))
        self.combo_vitri.set("Gần trường")

        # Khu vực các tùy chọn nhanh
        self.create_section_label("Tiện ích & Đặc điểm:")
        self.sw_chongoi = self.create_switch("Có chỗ ngồi tại quán")
        self.sw_chongoi.select()
        self.sw_delivery = self.create_switch("Có bán qua App/Delivery")
        self.sw_sv = self.create_switch("Cho phép ngồi học lâu (Laptop)")

        self.btn_main = ctk.CTkButton(self.left_frame, text="🚀 PHÂN TÍCH DOANH THU", 
                                      font=("Segoe UI", 16, "bold"), height=60, corner_radius=10,
                                      command=self.start_calc)
        self.btn_main.pack(fill="x", padx=30, pady=30)

    def create_labeled_entry(self, label_text, placeholder):
        # Tạo container chứa cả nhãn và ô nhập để giữ khoảng cách đều
        container = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        container.pack(fill="x", padx=30, pady=5)
        
        lbl = ctk.CTkLabel(container, text=label_text, font=FONT_LABEL)
        lbl.pack(anchor="w")
        
        ent = ctk.CTkEntry(container, placeholder_text=placeholder, font=FONT_V, height=40)
        ent.pack(fill="x", pady=(2, 10))
        ent.bind("<KeyRelease>", self.reset_button)
        return ent

    def create_section_label(self, text):
        lbl = ctk.CTkLabel(self.left_frame, text=text, font=FONT_LABEL)
        lbl.pack(anchor="w", padx=30, pady=(10, 2))

    def create_switch(self, text):
        sw = ctk.CTkSwitch(self.left_frame, text=text, font=FONT_V, command=self.reset_button)
        sw.pack(anchor="w", padx=40, pady=6)
        return sw

    def build_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1a1c1e")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure((0,1,2), weight=1)

        self.lbl_status = ctk.CTkLabel(self.right_frame, text="HỆ THỐNG SẴN SÀNG", font=("Segoe UI", 24, "bold"), text_color="#888888")
        self.lbl_status.grid(row=0, column=0, sticky="s", pady=20)

        self.lbl_result_ngay = ctk.CTkLabel(self.right_frame, text="0 VNĐ", font=("Segoe UI", 70, "bold"), text_color="#2FA572")
        self.lbl_result_ngay.grid(row=1, column=0)

        self.lbl_result_thang = ctk.CTkLabel(self.right_frame, text="Dự kiến tháng: 0 VNĐ", font=("Segoe UI", 22), text_color="#555555")
        self.lbl_result_thang.grid(row=2, column=0, sticky="n", pady=20)

    def reset_button(self, event=None):
        self.btn_main.configure(state="normal", text="🚀 PHÂN TÍCH DOANH THU", fg_color=["#3a7ebf", "#1f538d"], command=self.start_calc)
        self.lbl_status.configure(text="CHỜ PHÂN TÍCH...", text_color="#d4a373")

    def start_calc(self):
        try:
            # Logic kiểm tra ngoại suy (bổ sung từ câu hỏi trước)
            gia = float(self.entry_gia.get())
            khach = int(self.entry_khach.get())
            
            if gia > 150000 and khach > 40:
                messagebox.showwarning("Logic Error", "Giá > 150k khó duy trì lượng khách đông. AI có thể sai lệch!")

            user_input = {
                'Gia_TB_1Ly': gia,
                'Khach_Ngay': khach,
                'Vi_tri': self.combo_vitri.get(),
                'Co_Cho_Ngoi': 1 if self.sw_chongoi.get() else 0,
                'Co_Delivery': 1 if self.sw_delivery.get() else 0,
                'So_Nhan_Vien': int(self.entry_nv.get()),
                'Cho_SV_Ngoi_Lau': 1 if self.sw_sv.get() else 0,
                'Dien_Tich_m2': float(self.entry_dt.get()),
                'So_Doi_Thu_500m': int(self.entry_doithu.get())
            }
            
            self.btn_main.configure(state="disabled", text="⌛ Đang xử lý...")
            threading.Thread(target=self.work, args=(user_input,), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ các ô số liệu!")

    def work(self, user_input):
        try:
            res = logic_module.predict_revenue(user_input)
            self.after(0, self.done, res)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
            self.after(0, self.reset_button)

    def done(self, res):
        self.latest_res = res
        ngay, thang = res
        self.lbl_status.configure(text="KẾT QUẢ DỰ ĐOÁN", text_color="#ffffff")
        self.lbl_result_ngay.configure(text=f"{ngay:,.0f} VNĐ")
        self.lbl_result_thang.configure(text=f"Dự kiến tháng: {thang:,.0f} VNĐ")
        self.btn_main.configure(state="normal", text="📋 XUẤT BÁO CÁO", fg_color="#d97706", command=self.show_report)

    def show_report(self):
        if not self.latest_res: return
        ngay, thang = self.latest_res
        
        pop = ctk.CTkToplevel(self)
        pop.title("Báo cáo AI chi tiết")
        pop.geometry("480x650")
        pop.attributes("-topmost", True)
        pop.grab_set()

        if self.img_report:
            ctk.CTkLabel(pop, image=self.img_report, text="").pack(pady=20)

        ctk.CTkLabel(pop, text="PHIẾU DỰ TOÁN KINH DOANH", font=("Segoe UI", 20, "bold")).pack()
        
        box = ctk.CTkFrame(pop, fg_color="#f0f0f0")
        box.pack(fill="x", padx=40, pady=20)

        rows = [
            ("Phân khúc vị trí:", self.combo_vitri.get()),
            ("Mô hình vận hành:", "Tại chỗ + Ship" if self.sw_delivery.get() else "Chỉ tại chỗ"),
            ("Doanh thu Ngày:", f"{ngay:,.0f} VNĐ"),
            ("Doanh thu Tháng:", f"{thang:,.0f} VNĐ"),
            ("Độ tin cậy:", "Cao (Dữ liệu nội suy)")
        ]

        for l, v in rows:
            f = ctk.CTkFrame(box, fg_color="transparent")
            f.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(f, text=l, font=("Segoe UI", 13), text_color="#333").pack(side="left")
            ctk.CTkLabel(f, text=v, font=("Segoe UI", 13, "bold"), text_color="#1f6aa5").pack(side="right")
        
        ctk.CTkButton(pop, text="XÁC NHẬN", font=("Segoe UI", 14, "bold"), height=45, command=pop.destroy).pack(pady=20)

if __name__ == "__main__":
    MilkTeaApp().mainloop()