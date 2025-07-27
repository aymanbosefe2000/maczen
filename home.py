import tkinter as tk
import seting
import saleswindow
import maczen
import financial2

class HomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("الواجهة الرئيسية لمنظومة المصنع")
        self.geometry("400x400")

        # زر المبيعات
        btn_sales = tk.Button(self, text="المبيعات", font=("Arial", 13, "bold"), width=20, height=2, command=self.open_sales)
        btn_sales.pack(pady=10)

        # زر المخزن
        btn_maczen = tk.Button(self, text="المخزن", font=("Arial", 13, "bold"), width=20, height=2, command=self.open_storage)
        btn_maczen.pack(pady=10)

        # زر المالية
        btn_financial2 = tk.Button(self, text="المالية", font=("Arial", 13, "bold"), width=20, height=2, command=self.open_financial)
        btn_financial2.pack(pady=10)
        
        # زر التقارير
        btn_report = tk.Button(self, text="التقارير", font=("Arial", 13, "bold"), width=20, height=2, command=self.open_report)
        btn_report.pack(pady=10)

        # زر الإعدادات
        btn_setting = tk.Button(self, text="الإعدادات", font=("Arial", 13, "bold"), width=20, height=2, command=self.open_settings)
        btn_setting.pack(pady=10)

    def open_sales(self):
        self.withdraw()
        saleswindow.SalesWindow(self, self)

    def open_storage(self):
        self.withdraw()
        maczen.MaczenWindow(self, self)

    def open_financial(self):
        self.withdraw()
        win = financial2.MainApp()
        win.mainloop()
        self.deiconify()

    def open_report(self):
        # ضع هنا استدعاء نافذة التقارير
        # مثال:
        # import tqrer
        # self.withdraw()
        # tqrer.ReportWindow(parent=self, home_window=self)
        pass

    def open_settings(self):
        self.withdraw()  # إخفاء الصفحة الرئيسية
        seting.SettingsApp(parent=self, home_window=self)

if __name__ == "__main__":
    app = HomeWindow()
    app.mainloop()