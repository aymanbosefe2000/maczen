import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "attendance.db"

class SettingsApp(tk.Toplevel):
    def __init__(self, parent=None, home_window=None):
        super().__init__(parent)
        self.title("الإعدادات")
        self.geometry("900x550")
        self.home_window = home_window  # مرجع للواجهة الرئيسية
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # حدث إغلاق النافذة
        self.init_db()
        self.create_main_buttons()
        self.customer_frame = None
        self.employee_frame = None

    def on_close(self):
        """عند إغلاق النافذة أو الضغط على زر رجوع، أظهر النافذة الرئيسية"""
        if self.home_window is not None:
            self.home_window.deiconify()
        self.destroy()

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # جدول العملاء
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                address TEXT
            )
        ''')
        # جدول الموظفين مع قيمة الخلصة
        c.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                job_title TEXT,
                salary_type TEXT,
                salary_value TEXT
            )
        ''')
        # ضمان وجود الحقول في قواعد البيانات القديمة
        c.execute("PRAGMA table_info(employees)")
        cols = [x[1] for x in c.fetchall()]
        if "phone" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN phone TEXT")
        if "job_title" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN job_title TEXT")
        if "salary_type" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN salary_type TEXT")
        if "salary_value" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN salary_value TEXT")
        conn.commit()
        conn.close()

    def create_main_buttons(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=8)
        btn_customer = tk.Button(top, text="العملاء", font=("Arial", 13, "bold"), width=15, command=self.show_customers)
        btn_customer.pack(side="right", padx=12)
        btn_employee = tk.Button(top, text="الموظفين", font=("Arial", 13, "bold"), width=15, command=self.show_employees)
        btn_employee.pack(side="right", padx=12)
        # زر الرجوع
        btn_back = tk.Button(top, text="رجوع", font=("Arial", 13, "bold"), width=10, command=self.on_close)
        btn_back.pack(side="left", padx=12)

    def hide_frames(self):
        if self.customer_frame:
            self.customer_frame.pack_forget()
        if self.employee_frame:
            self.employee_frame.pack_forget()

    # ---------------------------------- العملاء ----------------------------------
    def show_customers(self):
        self.hide_frames()
        if not self.customer_frame:
            self.customer_frame = tk.Frame(self)
            # جدول العملاء
            columns = ("id", "name", "phone", "address")
            self.customer_tree = ttk.Treeview(self.customer_frame, columns=columns, show="headings", height=14)
            headers = ["الرقم", "اسم العميل", "رقم الهاتف", "العنوان"]
            for col, header in zip(columns, headers):
                self.customer_tree.heading(col, text=header)
                self.customer_tree.column(col, width=180, anchor="center")
            self.customer_tree.pack(fill="both", expand=True, padx=8, pady=8)

            # نموذج الإدخال
            form = tk.Frame(self.customer_frame)
            form.pack(pady=4)
            tk.Label(form, text="اسم العميل:", font=("Arial", 11)).grid(row=0, column=0, padx=3)
            tk.Label(form, text="رقم الهاتف:", font=("Arial", 11)).grid(row=0, column=2, padx=3)
            tk.Label(form, text="العنوان:", font=("Arial", 11)).grid(row=0, column=4, padx=3)
            self.customer_name_var = tk.StringVar()
            self.customer_phone_var = tk.StringVar()
            self.customer_address_var = tk.StringVar()
            tk.Entry(form, textvariable=self.customer_name_var, width=18).grid(row=0, column=1)
            tk.Entry(form, textvariable=self.customer_phone_var, width=18).grid(row=0, column=3)
            tk.Entry(form, textvariable=self.customer_address_var, width=18).grid(row=0, column=5)

            # الأزرار
            btns = tk.Frame(self.customer_frame)
            btns.pack(pady=6)
            tk.Button(btns, text="إضافة", font=("Arial", 11), width=12, command=self.add_customer).pack(side="right", padx=4)
            tk.Button(btns, text="تعديل", font=("Arial", 11), width=12, command=self.edit_customer).pack(side="right", padx=4)
            tk.Button(btns, text="حذف", font=("Arial", 11), width=12, command=self.delete_customer).pack(side="right", padx=4)
            tk.Button(btns, text="تحديث", font=("Arial", 11), width=10, command=self.refresh_customers).pack(side="right", padx=4)
        self.customer_frame.pack(fill="both", expand=True)
        self.refresh_customers()

    def refresh_customers(self):
        self.customer_tree.delete(*self.customer_tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name, phone, address FROM customers ORDER BY id DESC")
        rows = c.fetchall()
        for row in rows:
            self.customer_tree.insert("", "end", values=row)
        conn.close()

    def add_customer(self):
        name = self.customer_name_var.get().strip()
        phone = self.customer_phone_var.get().strip()
        address = self.customer_address_var.get().strip()
        if not name:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم العميل")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
        conn.commit()
        conn.close()
        self.customer_name_var.set("")
        self.customer_phone_var.set("")
        self.customer_address_var.set("")
        self.refresh_customers()

    def edit_customer(self):
        sel = self.customer_tree.selection()
        if not sel:
            messagebox.showwarning("تنبيه", "اختر عميلاً لتعديله")
            return
        item = self.customer_tree.item(sel[0])
        cid = item["values"][0]
        name = self.customer_name_var.get().strip()
        phone = self.customer_phone_var.get().strip()
        address = self.customer_address_var.get().strip()
        if not name:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم العميل")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE customers SET name=?, phone=?, address=? WHERE id=?", (name, phone, address, cid))
        conn.commit()
        conn.close()
        self.refresh_customers()

    def delete_customer(self):
        sel = self.customer_tree.selection()
        if not sel:
            messagebox.showwarning("تنبيه", "اختر عميلاً لحذفه")
            return
        item = self.customer_tree.item(sel[0])
        cid = item["values"][0]
        if not messagebox.askyesno("تأكيد", "هل تريد حذف العميل؟"):
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE id=?", (cid,))
        conn.commit()
        conn.close()
        self.refresh_customers()

    # ---------------------------------- الموظفين ----------------------------------
    def show_employees(self):
        self.hide_frames()
        if not self.employee_frame:
            self.employee_frame = tk.Frame(self)
            # جدول الموظفين
            columns = ("id", "name", "phone", "job_title", "salary_type", "salary_value")
            self.employee_tree = ttk.Treeview(self.employee_frame, columns=columns, show="headings", height=14)
            headers = ["الرقم", "اسم الموظف", "رقم الهاتف", "الوظيفة", "نوع الخلصة", "قيمة الخلصة"]
            for col, header in zip(columns, headers):
                self.employee_tree.heading(col, text=header)
                self.employee_tree.column(col, width=110 if col != "salary_value" else 120, anchor="center")
            self.employee_tree.pack(fill="both", expand=True, padx=8, pady=8)

            # نموذج الإدخال
            form = tk.Frame(self.employee_frame)
            form.pack(pady=4)
            tk.Label(form, text="اسم الموظف:", font=("Arial", 11)).grid(row=0, column=0, padx=3)
            tk.Label(form, text="رقم الهاتف:", font=("Arial", 11)).grid(row=0, column=2, padx=3)
            tk.Label(form, text="الوظيفة:", font=("Arial", 11)).grid(row=0, column=4, padx=3)
            tk.Label(form, text="نوع الخلصة:", font=("Arial", 11)).grid(row=0, column=6, padx=3)
            tk.Label(form, text="قيمة الخلصة:", font=("Arial", 11)).grid(row=0, column=8, padx=3)
            self.emp_name_var = tk.StringVar()
            self.emp_phone_var = tk.StringVar()
            self.emp_job_var = tk.StringVar()
            self.emp_salary_var = tk.StringVar()
            self.emp_salary_value_var = tk.StringVar()
            tk.Entry(form, textvariable=self.emp_name_var, width=12).grid(row=0, column=1)
            tk.Entry(form, textvariable=self.emp_phone_var, width=12).grid(row=0, column=3)
            tk.Entry(form, textvariable=self.emp_job_var, width=12).grid(row=0, column=5)
            self.emp_salary_combo = ttk.Combobox(form, textvariable=self.emp_salary_var, values=["يومي", "نسبة"], state="readonly", width=10)
            self.emp_salary_combo.grid(row=0, column=7)
            tk.Entry(form, textvariable=self.emp_salary_value_var, width=12).grid(row=0, column=9)

            # الأزرار
            btns = tk.Frame(self.employee_frame)
            btns.pack(pady=6)
            tk.Button(btns, text="إضافة", font=("Arial", 11), width=12, command=self.add_employee).pack(side="right", padx=4)
            tk.Button(btns, text="تعديل", font=("Arial", 11), width=12, command=self.edit_employee).pack(side="right", padx=4)
            tk.Button(btns, text="حذف", font=("Arial", 11), width=12, command=self.delete_employee).pack(side="right", padx=4)
            tk.Button(btns, text="تحديث", font=("Arial", 11), width=10, command=self.refresh_employees).pack(side="right", padx=4)
        self.employee_frame.pack(fill="both", expand=True)
        self.refresh_employees()

    def refresh_employees(self):
        self.employee_tree.delete(*self.employee_tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # يتأكد من وجود الحقول الإضافية
        c.execute("PRAGMA table_info(employees)")
        cols = [x[1] for x in c.fetchall()]
        if "phone" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN phone TEXT")
        if "job_title" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN job_title TEXT")
        if "salary_type" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN salary_type TEXT")
        if "salary_value" not in cols:
            c.execute("ALTER TABLE employees ADD COLUMN salary_value TEXT")
        conn.commit()
        c.execute("SELECT id, name, phone, job_title, salary_type, salary_value FROM employees ORDER BY id DESC")
        rows = c.fetchall()
        for row in rows:
            self.employee_tree.insert("", "end", values=row)
        conn.close()

    def add_employee(self):
        name = self.emp_name_var.get().strip()
        phone = self.emp_phone_var.get().strip()
        job = self.emp_job_var.get().strip()
        salary_type = self.emp_salary_var.get().strip()
        salary_value = self.emp_salary_value_var.get().strip()
        if not name:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم الموظف")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO employees (name, phone, job_title, salary_type, salary_value) VALUES (?, ?, ?, ?, ?)",
                  (name, phone, job, salary_type, salary_value))
        conn.commit()
        conn.close()
        self.emp_name_var.set("")
        self.emp_phone_var.set("")
        self.emp_job_var.set("")
        self.emp_salary_var.set("")
        self.emp_salary_value_var.set("")
        self.emp_salary_combo.set("")
        self.refresh_employees()

    def edit_employee(self):
        sel = self.employee_tree.selection()
        if not sel:
            messagebox.showwarning("تنبيه", "اختر موظفًا لتعديله")
            return
        item = self.employee_tree.item(sel[0])
        eid = item["values"][0]
        name = self.emp_name_var.get().strip()
        phone = self.emp_phone_var.get().strip()
        job = self.emp_job_var.get().strip()
        salary_type = self.emp_salary_var.get().strip()
        salary_value = self.emp_salary_value_var.get().strip()
        if not name:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم الموظف")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE employees SET name=?, phone=?, job_title=?, salary_type=?, salary_value=? WHERE id=?",
                  (name, phone, job, salary_type, salary_value, eid))
        conn.commit()
        conn.close()
        self.refresh_employees()

    def delete_employee(self):
        sel = self.employee_tree.selection()
        if not sel:
            messagebox.showwarning("تنبيه", "اختر موظفًا لحذفه")
            return
        item = self.employee_tree.item(sel[0])
        eid = item["values"][0]
        if not messagebox.askyesno("تأكيد", "هل تريد حذف الموظف؟"):
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE id=?", (eid,))
        conn.commit()
        conn.close()
        self.refresh_employees()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # اخفاء النافذة الرئيسية الافتراضية
    SettingsApp(root)
    root.mainloop()