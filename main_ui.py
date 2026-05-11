import customtkinter as ctk
import threading
import os
from tkinter import messagebox
from PIL import Image
import logic_module

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PATH_BANNER = os.path.join(ASSETS_DIR, "banner.png")
PATH_REPORT = os.path.join(ASSETS_DIR, "report_logo.png")

FONT_LABEL = ("Segoe UI", 13, "bold")
FONT_V = ("Segoe UI", 15)

class MilkTeaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Dự Đoán Doanh Thu - Real-world Logic")
        self.geometry("1150x850")
        
        self.img_report = None
        if os.path.exists(PATH_REPORT):
            self.img_report = ctk.CTkImage(Image.open(PATH_REPORT), size=(350, 200))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        logic_module.init_brain()
        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        self.left_frame = ctk.CTkScrollableFrame(self, width=450, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        if os.path.exists(PATH_BANNER):
            img_banner = ctk.CTkImage(Image.open(PATH_BANNER), size=(420, 160))
            ctk.CTkLabel(self.left_frame, text="", image=img_banner).pack(pady=(0, 20))

        ctk.CTkLabel(self.left_frame, text="THÔNG SỐ ĐẦU VÀO", font=("Segoe UI", 20, "bold"), text_color="#3a7ebf").pack(pady=10)

        self.entry_gia = self.create_labeled_entry("Giá trung bình 1 ly (VNĐ):", "Ví dụ: 35000")
        self.entry_khach = self.create_labeled_entry("Lượng khách dự kiến (Ngày thường):", "Ví dụ: 120")
        self.entry_dt = self.create_labeled_entry("Diện tích quán (m2):", "Ví dụ: 45.5")
        self.entry_nv = self.create_labeled_entry("Số lượng nhân viên:", "Ví dụ: 3")
        self.entry_doithu = self.create_labeled_entry("Số đối thủ (bán kính 500m):", "Ví dụ: 5")

        self.create_section_label("Vị trí mặt bằng:")
        self.combo_vitri = ctk.CTkComboBox(self.left_frame, values=["Gần trường", "Văn phòng", "Khu dân cư"], font=FONT_V, height=45, command=self.reset_button)
        self.combo_vitri.pack(fill="x", padx=30, pady=(0, 15))
        self.combo_vitri.set("Gần trường")

        self.create_section_label("Tiện ích & Đặc điểm:")
        self.sw_chongoi = self.create_switch("Có chỗ ngồi tại quán")
        self.sw_chongoi.select()
        self.sw_delivery = self.create_switch("Có bán qua App/Delivery")
        self.sw_sv = self.create_switch("Cho phép ngồi học lâu (Laptop)")

        self.btn_main = ctk.CTkButton(self.left_frame, text="🚀 PHÂN TÍCH DOANH THU", font=("Segoe UI", 16, "bold"), height=60, command=self.start_calc)
        self.btn_main.pack(fill="x", padx=30, pady=30)

    def create_labeled_entry(self, label_text, placeholder):
        container = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        container.pack(fill="x", padx=30, pady=5)
        ctk.CTkLabel(container, text=label_text, font=FONT_LABEL).pack(anchor="w")
        ent = ctk.CTkEntry(container, placeholder_text=placeholder, font=FONT_V, height=40)
        ent.pack(fill="x", pady=(2, 10))
        ent.bind("<KeyRelease>", self.reset_button)
        return ent

    def create_section_label(self, text):
        ctk.CTkLabel(self.left_frame, text=text, font=FONT_LABEL).pack(anchor="w", padx=30, pady=(10, 2))

    def create_switch(self, text):
        sw = ctk.CTkSwitch(self.left_frame, text=text, font=FONT_V, command=self.reset_button)
        sw.pack(anchor="w", padx=40, pady=6)
        return sw

    def build_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1a1c1e")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Tiêu đề
        self.lbl_status = ctk.CTkLabel(self.right_frame, text="DỰ TOÁN THỰC TẾ", font=("Segoe UI", 24, "bold"), text_color="#888888")
        self.lbl_status.pack(pady=(40, 20))

        # Khung kết quả chi tiết
        self.res_box = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.res_box.pack(fill="both", expand=True, padx=20)

        self.lbl_rev_weekday = self.create_result_label("NGÀY THƯỜNG", "#2FA572", 50)
        self.lbl_rev_weekend = self.create_result_label("CUỐI TUẦN (x1.4)", "#d97706", 50)
        
        ctk.CTkLabel(self.res_box, text="________________________________", text_color="#333333").pack(pady=10)
        
        self.lbl_total = self.create_result_label("TỔNG DOANH THU THÁNG", "#3a7ebf", 65)

    def create_result_label(self, title, color, size):
        ctk.CTkLabel(self.res_box, text=title, font=("Segoe UI", 14, "bold"), text_color="#888888").pack(pady=(15, 0))
        lbl = ctk.CTkLabel(self.res_box, text="0 VNĐ", font=("Segoe UI", size, "bold"), text_color=color)
        lbl.pack()
        return lbl

    def reset_button(self, event=None):
        self.btn_main.configure(state="normal", text="🚀 PHÂN TÍCH DOANH THU", fg_color=["#3a7ebf", "#1f538d"], command=self.start_calc)

    def start_calc(self):
        try:
            user_input = {
                'Gia_TB_1Ly': float(self.entry_gia.get()),
                'Khach_Ngay': int(self.entry_khach.get()),
                'Vi_tri': self.combo_vitri.get(),
                'Co_Cho_Ngoi': 1 if self.sw_chongoi.get() else 0,
                'Co_Delivery': 1 if self.sw_delivery.get() else 0,
                'So_Nhan_Vien': int(self.entry_nv.get()),
                'Cho_SV_Ngoi_Lau': 1 if self.sw_sv.get() else 0,
                'Dien_Tich_m2': float(self.entry_dt.get()),
                'So_Doi_Thu_500m': int(self.entry_doithu.get())
            }
            self.btn_main.configure(state="disabled", text="⌛ AI đang tính toán...")
            threading.Thread(target=self.work, args=(user_input,), daemon=True).start()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ số liệu!")

    def work(self, user_input):
        try:
            res = logic_module.predict_revenue_advanced(user_input)
            self.after(0, self.done, res)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
            self.after(0, self.reset_button)

    def done(self, res):
        self.latest_res = res
        self.lbl_rev_weekday.configure(text=f"{res['weekday_single']:,.0f} VNĐ")
        self.lbl_rev_weekend.configure(text=f"{res['weekend_single']:,.0f} VNĐ")
        self.lbl_total.configure(text=f"{res['total_month']:,.0f} VNĐ")
        
        self.btn_main.configure(state="normal", text="📋 CHI TIẾT BÁO CÁO", fg_color="#d97706", command=self.show_report)

    def show_report(self):
        if not self.latest_res: return
        res = self.latest_res
        
        pop = ctk.CTkToplevel(self)
        pop.title("Báo cáo AI chi tiết")
        pop.geometry("500x650")
        pop.attributes("-topmost", True)
        pop.grab_set()

        if self.img_report:
            ctk.CTkLabel(pop, image=self.img_report, text="").pack(pady=20)

        box = ctk.CTkFrame(pop, fg_color="#f0f0f0")
        box.pack(fill="x", padx=40, pady=10)

        rows = [
            ("Trung bình ngày thường:", f"{res['weekday_single']:,.0f} đ"),
            ("Trung bình cuối tuần:", f"{res['weekend_single']:,.0f} đ"),
            ("Tổng 22 ngày thường:", f"{res['weekday_single']*22:,.0f} đ"),
            ("Tổng 8 ngày cuối tuần:", f"{res['weekend_single']*8:,.0f} đ"),
            ("TỔNG DOANH THU THÁNG:", f"{res['total_month']:,.0f} đ")
        ]

        for l, v in rows:
            f = ctk.CTkFrame(box, fg_color="transparent")
            f.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(f, text=l, font=("Segoe UI", 13)).pack(side="left")
            ctk.CTkLabel(f, text=v, font=("Segoe UI", 13, "bold"), text_color="#1f6aa5").pack(side="right")
        
        ctk.CTkButton(pop, text="HOÀN TẤT", font=("Segoe UI", 14, "bold"), height=45, command=pop.destroy).pack(pady=20)

if __name__ == "__main__":
    MilkTeaApp().mainloop()