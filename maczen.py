import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_NAME = "store.db"

# --- شاشة المخزن الرئيسية ---
class MaczenWindow(tk.Toplevel):
    def __init__(self, parent, home_window):
        super().__init__(parent)
        self.title("المخزن - إدارة الأصناف")
        self.geometry("1000x600")
        self.home_window = home_window
        self.init_db()
        self.create_widgets()
        self.load_products()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # الأصناف
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                price REAL
            )
        ''')
        # خطوط الإنتاج
        c.execute('''
            CREATE TABLE IF NOT EXISTS production_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                line_name TEXT UNIQUE
            )
        ''')
        c.execute("INSERT OR IGNORE INTO production_lines (line_name) VALUES ('خط 1')")
        c.execute("INSERT OR IGNORE INTO production_lines (line_name) VALUES ('خط 2')")
        # جدول تفاصيل إنتاج الخطوط لكل صنف
        c.execute('''
            CREATE TABLE IF NOT EXISTS product_line_quantities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                line_id INTEGER,
                quantity INTEGER,
                date TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(line_id) REFERENCES production_lines(id)
            )
        ''')
        # ضمان وجود عمود date في قاعدة بيانات قديمة
        c.execute("PRAGMA table_info(product_line_quantities)")
        cols = [r[1] for r in c.fetchall()]
        if "date" not in cols:
            c.execute("ALTER TABLE product_line_quantities ADD COLUMN date TEXT")
        conn.commit()
        conn.close()

    def create_widgets(self):
        # شريط البحث
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="بحث عن صنف:", font=("Arial", 12)).pack(side="right")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        search_entry.pack(side="right", padx=8)
        search_entry.bind("<KeyRelease>", self.search_products)

        # جدول الأصناف
        columns = ("id", "product_name", "total_quantity", "price")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        headers = ["الرقم", "اسم الصنف", "الكمية الإجمالية", "السعر"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=130 if col != "product_name" else 250)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # أزرار العمليات
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=6)
        tk.Button(btn_frame, text="إضافة صنف", width=14, font=("Arial", 12), command=self.add_product).pack(side="right", padx=7)
        tk.Button(btn_frame, text="تعديل صنف", width=14, font=("Arial", 12), command=self.edit_product).pack(side="right", padx=7)
        tk.Button(btn_frame, text="حذف صنف", width=14, font=("Arial", 12), command=self.delete_product).pack(side="right", padx=7)
        tk.Button(btn_frame, text="تحديث", width=8, font=("Arial", 12), command=self.load_products).pack(side="right", padx=7)
        tk.Button(btn_frame, text="خطوط الإنتاج", width=14, font=("Arial", 12), command=self.open_production_lines).pack(side="left", padx=7)

        # زر الرجوع للنافذة الرئيسية
        tk.Button(self, text="رجوع", font=("Arial", 12), command=self.close_window).pack(side="bottom", pady=10)

        # لا تضع self.pack هنا، لأن Toplevel لا يدعم pack أو grid

    def load_products(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # حساب الكمية الإجمالية من جدول الربط
        c.execute('''
            SELECT p.id, p.product_name, 
                   IFNULL(SUM(plq.quantity), 0) as total_quantity, 
                   p.price
            FROM products p
            LEFT JOIN product_line_quantities plq ON plq.product_id = p.id
            GROUP BY p.id, p.product_name, p.price
            ORDER BY p.id DESC
        ''')
        products = c.fetchall()
        conn.close()
        self.show_products(products)

    def show_products(self, products):
        self.tree.delete(*self.tree.get_children())
        for row in products:
            self.tree.insert("", "end", values=row)

    def search_products(self, event=None):
        keyword = self.search_var.get().lower()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            SELECT p.id, p.product_name, 
                   IFNULL(SUM(plq.quantity), 0) as total_quantity, 
                   p.price
            FROM products p
            LEFT JOIN product_line_quantities plq ON plq.product_id = p.id
            WHERE lower(p.product_name) LIKE ?
            GROUP BY p.id, p.product_name, p.price
            ORDER BY p.id DESC
        ''', (f"%{keyword}%",))
        products = c.fetchall()
        conn.close()
        self.show_products(products)

    def get_production_lines(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, line_name FROM production_lines ORDER BY id")
        lines = c.fetchall()
        conn.close()
        return lines

    def get_line_quantities(self, product_id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            SELECT line_id, quantity
            FROM product_line_quantities
            WHERE product_id = ?
        ''', (product_id,))
        data = {row[0]: row[1] for row in c.fetchall()}
        conn.close()
        return data

    def add_product(self):
        win = tk.Toplevel(self)
        win.title("إضافة صنف جديد")
        win.geometry("420x400")
        name_var = tk.StringVar()
        price_var = tk.DoubleVar(value=1.0)
        lines = self.get_production_lines()
        line_vars = {}
        # واجهة الإدخال
        tk.Label(win, text="اسم الصنف:", font=("Arial", 12)).pack(pady=4)
        tk.Entry(win, textvariable=name_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(win, text="السعر:", font=("Arial", 12)).pack(pady=4)
        tk.Entry(win, textvariable=price_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(win, text="إنتاج كل خط:", font=("Arial", 12, "bold")).pack(pady=6)
        for line_id, line_name in lines:
            f = tk.Frame(win)
            f.pack(anchor="w", padx=30, pady=2)
            var = tk.IntVar(value=0)
            line_vars[line_id] = var
            tk.Label(f, text=line_name, font=("Arial", 11)).pack(side="right")
            tk.Entry(f, textvariable=var, font=("Arial", 11), width=7).pack(side="right", padx=6)
        # التاريخ
        tk.Label(win, text="تاريخ الإنتاج (yyyy-mm-dd):", font=("Arial", 12)).pack(pady=6)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(win, textvariable=date_var, font=("Arial", 12)).pack(pady=2)

        def save():
            name = name_var.get().strip()
            price = price_var.get()
            date_val = date_var.get().strip()
            # اجمع كميات الخطوط
            total = 0
            line_data = []
            for line_id, var in line_vars.items():
                qty = var.get()
                if qty < 0:
                    messagebox.showerror("خطأ", "لا يمكن أن تكون الكمية سالبة")
                    return
                if qty > 0:
                    line_data.append((line_id, qty))
                    total += qty
            if not name or price < 0 or total == 0:
                messagebox.showerror("خطأ", "يرجى إدخال جميع البيانات بشكل صحيح، وكمية أكبر من صفر")
                return
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except:
                messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة (yyyy-mm-dd)")
                return
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO products (product_name, price) VALUES (?, ?)", (name, price))
            product_id = c.lastrowid
            for line_id, qty in line_data:
                c.execute("INSERT INTO product_line_quantities (product_id, line_id, quantity, date) VALUES (?, ?, ?, ?)", (product_id, line_id, qty, date_val))
            conn.commit()
            conn.close()
            win.destroy()
            self.load_products()
        tk.Button(win, text="حفظ", font=("Arial", 12), command=save).pack(pady=16)

    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر صنفًا لتعديله.")
            return
        item = self.tree.item(selected[0])
        pid, old_name, old_total, old_price = item["values"]

        win = tk.Toplevel(self)
        win.title("تعديل الصنف")
        win.geometry("420x400")
        name_var = tk.StringVar(value=old_name)
        price_var = tk.DoubleVar(value=old_price)
        lines = self.get_production_lines()
        old_line_quantities = self.get_line_quantities(pid)
        line_vars = {}
        tk.Label(win, text="اسم الصنف:", font=("Arial", 12)).pack(pady=4)
        tk.Entry(win, textvariable=name_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(win, text="السعر:", font=("Arial", 12)).pack(pady=4)
        tk.Entry(win, textvariable=price_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(win, text="إنتاج كل خط:", font=("Arial", 12, "bold")).pack(pady=6)
        for line_id, line_name in lines:
            f = tk.Frame(win)
            f.pack(anchor="w", padx=30, pady=2)
            var = tk.IntVar(value=old_line_quantities.get(line_id,0))
            line_vars[line_id] = var
            tk.Label(f, text=line_name, font=("Arial", 11)).pack(side="right")
            tk.Entry(f, textvariable=var, font=("Arial", 11), width=7).pack(side="right", padx=6)
        # التاريخ (لا يمكن تعديله في هذه النسخة، لكن يمكن إضافته لو أردت)
        tk.Label(win, text="تاريخ الإنتاج (yyyy-mm-dd):", font=("Arial", 12)).pack(pady=6)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(win, textvariable=date_var, font=("Arial", 12)).pack(pady=2)
        def save():
            name = name_var.get().strip()
            price = price_var.get()
            date_val = date_var.get().strip()
            total = 0
            line_data = []
            for line_id, var in line_vars.items():
                qty = var.get()
                if qty < 0:
                    messagebox.showerror("خطأ", "لا يمكن أن تكون الكمية سالبة")
                    return
                if qty > 0:
                    line_data.append((line_id, qty))
                    total += qty
            if not name or price < 0 or total == 0:
                messagebox.showerror("خطأ", "يرجى إدخال جميع البيانات بشكل صحيح، وكمية أكبر من صفر")
                return
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except:
                messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة (yyyy-mm-dd)")
                return
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("UPDATE products SET product_name=?, price=? WHERE id=?", (name, price, pid))
            # احذف تفاصيل الكميات القديمة ثم أضف الجديدة
            c.execute("DELETE FROM product_line_quantities WHERE product_id=?", (pid,))
            for line_id, qty in line_data:
                c.execute("INSERT INTO product_line_quantities (product_id, line_id, quantity, date) VALUES (?, ?, ?, ?)", (pid, line_id, qty, date_val))
            conn.commit()
            conn.close()
            win.destroy()
            self.load_products()
        tk.Button(win, text="حفظ التعديل", font=("Arial", 12), command=save).pack(pady=16)

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر صنفًا لحذفه.")
            return
        item = self.tree.item(selected[0])
        pid, name, _, _ = item["values"]
        if not messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الصنف '{name}'؟"):
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM product_line_quantities WHERE product_id=?", (pid,))
        c.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        self.load_products()

    def open_production_lines(self):
        self.withdraw()
        win = tk.Toplevel(self)
        ProductionLinesWindow(win, self.home_window if self.home_window else self)
        win.protocol("WM_DELETE_WINDOW", lambda: [win.destroy(), self.deiconify()])

    def close_window(self):
        self.destroy()
        if self.home_window:
            self.home_window.deiconify()

# --- شاشة خطوط الإنتاج (عرض فقط) ---
class ProductionLinesWindow(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent)
        self.parent = parent
        self.main_win = main_win
        self.parent.title("خطوط الإنتاج - تفاصيل الإنتاج")
        self.parent.geometry("1080x600")
        self.create_widgets()
        self.load_lines()

    def get_products_names(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT product_name FROM products ORDER BY product_name")
        names = [row[0] for row in c.fetchall()]
        conn.close()
        return names

    def create_widgets(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=6)
        tk.Label(search_frame, text="اختر اسم الصنف:", font=("Arial", 12)).pack(side="right")

        self.product_search_var = tk.StringVar()
        product_names = [""] + self.get_products_names()
        self.product_combo = ttk.Combobox(search_frame, textvariable=self.product_search_var, values=product_names, font=("Arial", 12), state="readonly", width=22)
        self.product_combo.pack(side="right", padx=5)
        self.product_combo.bind("<<ComboboxSelected>>", lambda e: self.load_lines())

        # التاريخ من إلى
        tk.Label(search_frame, text="من تاريخ (yyyy-mm-dd):", font=("Arial", 12)).pack(side="right", padx=7)
        self.from_date_var = tk.StringVar()
        from_entry = tk.Entry(search_frame, textvariable=self.from_date_var, font=("Arial", 12), width=12)
        from_entry.pack(side="right", padx=2)
        tk.Label(search_frame, text="إلى تاريخ (yyyy-mm-dd):", font=("Arial", 12)).pack(side="right", padx=7)
        self.to_date_var = tk.StringVar()
        to_entry = tk.Entry(search_frame, textvariable=self.to_date_var, font=("Arial", 12), width=12)
        to_entry.pack(side="right", padx=2)

        tk.Button(search_frame, text="تصفية", font=("Arial", 12), command=self.load_lines).pack(side="right", padx=8)
        tk.Button(search_frame, text="رجوع", font=("Arial", 12), command=self.close_window).pack(side="left", padx=10)

        columns = ("line_name", "product_name", "quantity", "date")
        headers = ["خط الإنتاج", "اسم الصنف", "الكمية المنتجة", "التاريخ"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=24)
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=180 if col=="line_name" else 180)
        self.tree.pack(fill="both", expand=True, padx=10, pady=15)
        self.pack(fill="both", expand=True)

    def load_lines(self):
        product_name = self.product_search_var.get().strip()
        from_date = self.from_date_var.get().strip()
        to_date = self.to_date_var.get().strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        sql = '''
            SELECT l.line_name, p.product_name, plq.quantity, plq.date
            FROM product_line_quantities plq
            JOIN products p ON p.id = plq.product_id
            JOIN production_lines l ON l.id = plq.line_id
            WHERE 1=1
        '''
        params = []
        if product_name:
            sql += " AND p.product_name = ?"
            params.append(product_name)
        if from_date:
            sql += " AND date(plq.date) >= date(?)"
            params.append(from_date)
        if to_date:
            sql += " AND date(plq.date) <= date(?)"
            params.append(to_date)
        sql += " ORDER BY l.line_name, p.product_name, plq.date DESC"
        c.execute(sql, params)
        rows = c.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
        conn.close()

    def close_window(self):
        self.parent.destroy()
        self.main_win.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    MaczenWindow(root, None)
    root.mainloop()