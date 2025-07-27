import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import platform

DB_NAME = "store.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            customer TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

class SalesWindow(tk.Toplevel):
    def __init__(self, parent, home_window):
        super().__init__(parent)
        self.title("إدارة المبيعات")
        self.geometry("1200x650")
        self.home_window = home_window
        self.selected_items = {}
        self.create_widgets()
        self.load_products()
        self.load_customers()
        self.refresh_invoice()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # المنتجات (يمين)
        right_frame = tk.Frame(paned)
        paned.add(right_frame, weight=1)

        # الفاتورة (يسار)
        left_frame = tk.Frame(paned)
        paned.add(left_frame, weight=3)

        # --- البحث عن صنف ---
        search_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        search_paned.pack(fill="x", padx=10, pady=8)
        search_label = tk.Label(search_paned, text="بحث عن صنف:", font=("Arial", 12))
        search_entry = tk.Entry(search_paned, font=("Arial", 12))
        search_entry.bind("<KeyRelease>", self.search_products)
        self.search_var = search_entry
        search_paned.add(search_label, weight=0)
        search_paned.add(search_entry, weight=1)

        # --- جدول المنتجات ---
        products_tree = ttk.Treeview(right_frame, columns=("الاسم", "السعر", "المتوفر"), show="headings", height=22)
        for col in products_tree["columns"]:
            products_tree.heading(col, text=col)
            products_tree.column(col, width=170 if col == "الاسم" else 110, anchor="center", stretch=True)
        products_tree.pack(fill="both", expand=True, padx=10, pady=5)
        products_tree.bind("<Double-1>", self.add_item_to_invoice)
        products_tree.bind('<ButtonRelease-1>', self.adjust_column_widths)
        self.products_tree = products_tree

        # --- أعلى الفاتورة: اسم العميل ---
        top_left = tk.Frame(left_frame)
        top_left.pack(fill="x", pady=5)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_label = tk.Label(top_left, text=f"التاريخ: {now}", font=("Arial", 12))
        self.date_label.pack(side="left", padx=8)
        tk.Label(top_left, text="اسم العميل:", font=("Arial", 12)).pack(side="left")
        client_paned = ttk.PanedWindow(top_left, orient=tk.HORIZONTAL)
        client_paned.pack(side="left", fill="x", expand=True)
        self.customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(client_paned, textvariable=self.customer_var, width=25)
        customer_combo.bind("<KeyRelease>", self.customer_combo_autocomplete)
        client_paned.add(customer_combo, weight=1)
        self.customer_combo = customer_combo

        # --- جدول الفاتورة ---
        invoice_columns = ("الاسم", "الكمية", "السعر", "الإجمالي")
        invoice_tree = ttk.Treeview(left_frame, columns=invoice_columns, show="headings", height=17)
        for col in invoice_columns:
            invoice_tree.heading(col, text=col)
            invoice_tree.column(col, width=120, anchor="center", stretch=True)
        invoice_tree.pack(fill="both", expand=True, padx=8, pady=5)
        invoice_tree.bind("<Double-1>", self.increase_quantity)
        invoice_tree.bind('<ButtonRelease-1>', self.adjust_invoice_column_widths)
        self.invoice_tree = invoice_tree

        # --- أزرار ---
        tk.Button(left_frame, text="حفظ الفاتورة", font=("Arial", 14, "bold"), command=self.save_invoice_popup).pack(pady=5)
        tk.Button(left_frame, text="عرض الفواتير", font=("Arial", 12), command=self.show_sales_list).pack(pady=5)
        tk.Button(left_frame, text="رجوع", font=("Arial", 12), command=self.close_window).pack(pady=5)
        tk.Button(self, text="رجوع", font=("Arial", 12), command=self.close_window).pack(pady=8)

    def adjust_column_widths(self, event=None):
        for col in self.products_tree["columns"]:
            self.products_tree.column(col, width=max(120, max([len(str(self.products_tree.set(item, col)))*12 for item in self.products_tree.get_children()] + [120])))

    def adjust_invoice_column_widths(self, event=None):
        for col in self.invoice_tree["columns"]:
            self.invoice_tree.column(col, width=max(120, max([len(str(self.invoice_tree.set(item, col)))*12 for item in self.invoice_tree.get_children()] + [120])))

    def load_products(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, product_name, price, quantity FROM products")
        self.products = c.fetchall()
        conn.close()
        self.show_products(self.products)

    def load_customers(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name FROM customers")
        customers = [row[0] for row in c.fetchall()]
        conn.close()
        self.customer_combo["values"] = customers

    def show_products(self, products):
        self.products_tree.delete(*self.products_tree.get_children())
        for row in products:
            self.products_tree.insert("", "end", values=(row[1], row[2], row[3]), iid=row[0])
        self.adjust_column_widths()

    def search_products(self, event=None):
        keyword = self.search_var.get().lower()
        filtered = [row for row in self.products if keyword in row[1].lower()]
        self.show_products(filtered)

    def add_item_to_invoice(self, event):
        selected = self.products_tree.selection()
        if not selected:
            return
        pid = int(selected[0])
        name, price, available = self.products_tree.item(selected[0])["values"]
        try:
            price = float(price)
            available = int(available)
        except Exception:
            price = 0
            available = 0

        qty_in_invoice = self.selected_items[pid][1] if pid in self.selected_items else 0
        if available == 0:
            messagebox.showwarning("نفاذ الكمية", f"الكمية لهذا الصنف انتهت من المخزون.")
            return
        if qty_in_invoice + 1 > available:
            messagebox.showwarning("كمية غير كافية", f"الكمية المطلوبة أكبر من الكمية المتوفرة ({available}).")
            return

        if pid in self.selected_items:
            self.selected_items[pid][1] += 1
        else:
            self.selected_items[pid] = [name, 1, price]
        self.refresh_invoice()

    def increase_quantity(self, event):
        selected = self.invoice_tree.selection()
        if not selected:
            return
        pid = int(selected[0])
        try:
            current_qty = int(self.selected_items[pid][1])
        except Exception:
            current_qty = 1

        available = 0
        for row in self.products:
            if row[0] == pid:
                available = int(row[3])
                break

        qty = simpledialog.askinteger("تعديل الكمية", f"أدخل الكمية الجديدة (المتوفر {available}):", minvalue=1, initialvalue=current_qty)
        if qty:
            if qty > available:
                messagebox.showwarning("كمية غير كافية", f"الكمية المطلوبة أكبر من الكمية المتوفرة ({available}).")
                return
            self.selected_items[pid][1] = qty
            self.refresh_invoice()

    def refresh_invoice(self):
        self.invoice_tree.delete(*self.invoice_tree.get_children())
        for pid, (name, qty, price) in self.selected_items.items():
            try:
                qty_num = int(qty)
            except Exception:
                qty_num = 0
            try:
                price_num = float(price)
            except Exception:
                price_num = 0
            total = qty_num * price_num
            self.invoice_tree.insert("", "end", values=(name, qty_num, price_num, total), iid=pid)
        self.adjust_invoice_column_widths()

    def customer_combo_autocomplete(self, event):
        val = self.customer_var.get().lower()
        values = [c for c in self.customer_combo["values"] if val in c.lower()]
        self.customer_combo["values"] = values

    def save_invoice_popup(self):
        if not self.customer_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
            return
        if not self.selected_items:
            messagebox.showerror("خطأ", "لا توجد أصناف في الفاتورة")
            return

        popup = tk.Toplevel(self)
        popup.title("حفظ الفاتورة")
        popup.geometry("300x120")
        tk.Label(popup, text="ماذا تريد أن تفعل؟", font=("Arial", 13)).pack(pady=10)
        def do_save_and_print():
            invoice_id = self._save_invoice_to_db()
            popup.destroy()
            self.selected_items = {}
            self.refresh_invoice()
            self.load_products()
            self.print_invoice_popup(invoice_id)
        def do_save_only():
            self._save_invoice_to_db()
            popup.destroy()
            self.selected_items = {}
            self.refresh_invoice()
            self.load_products()
        tk.Button(popup, text="حفظ وطباعة", font=("Arial", 12), width=12, command=do_save_and_print).pack(pady=5)
        tk.Button(popup, text="حفظ فقط", font=("Arial", 12), width=12, command=do_save_only).pack(pady=5)

    def _save_invoice_to_db(self):
        customer = self.customer_var.get().strip()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO customers (name) VALUES (?)", (customer,))
        conn.commit()
        invoice_ids = []
        for pid, (name, qty, price) in self.selected_items.items():
            c.execute("INSERT INTO sales (product_id, product_name, quantity, price, customer, date) VALUES (?, ?, ?, ?, ?, ?)",
                      (pid, name, qty, price, customer, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            invoice_ids.append(c.lastrowid)
            c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (qty, pid))
        conn.commit()
        conn.close()
        if invoice_ids:
            return invoice_ids[-1] # آخر فاتورة
        return None

    def print_invoice_popup(self, sales_id=None):
        # جلب بيانات الفاتورة
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if sales_id is None:
            c.execute("SELECT id FROM sales ORDER BY id DESC LIMIT 1")
            row = c.fetchone()
            if not row:
                messagebox.showerror("خطأ", "لا توجد فاتورة للطباعة")
                return
            sales_id = row[0]

        c.execute("SELECT customer, date FROM sales WHERE id = ?", (sales_id,))
        sale_info = c.fetchone()
        if not sale_info:
            messagebox.showerror("خطأ", "لا يمكن إيجاد بيانات الفاتورة")
            return

        customer, date_val = sale_info
        c.execute("SELECT product_name, quantity, price FROM sales WHERE customer = ? AND date = ?", (customer, date_val))
        sales_rows = c.fetchall()
        conn.close()

        # بناء نص الفاتورة
        invoice_text = ""
        invoice_text += f"{'='*18} فاتورة مبيعات {'='*18}\n"
        invoice_text += f"التاريخ: {date_val}\n"
        invoice_text += f"اسم العميل: {customer}\n"
        invoice_text += "-"*55 + "\n"
        invoice_text += f"{'الصنف':<25}{'الكمية':<12}{'السعر':<10}{'الإجمالي':<10}\n"
        invoice_text += "-"*55 + "\n"
        total = 0
        for prod, qty, price in sales_rows:
            subtotal = qty * price
            total += subtotal
            invoice_text += f"{prod:<25}{qty:<12}{price:<10.2f}{subtotal:<10.2f}\n"
        invoice_text += "-"*55 + "\n"
        invoice_text += f"{'الإجمالي الكلي:':<25}{'':<12}{'':<10}{total:<10.2f}\n"

        win = tk.Toplevel(self)
        win.title("معاينة الفاتورة")
        text_area = tk.Text(win, font=("Arial", 13), width=60, height=22)
        text_area.pack(padx=10, pady=10)
        text_area.insert("1.0", invoice_text)
        text_area.config(state="disabled")

        def do_print():
            if WIN32_AVAILABLE:
                temp_file = "temp_invoice.txt"
                with open(temp_file, "w", encoding="utf-8") as f:
                    f.write(invoice_text)
                try:
                    win32api.ShellExecute(
                        0,
                        "print",
                        temp_file,
                        None,
                        ".",
                        0
                    )
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ أثناء الطباعة:\n{e}")
                    win.destroy()
            else:
                messagebox.showinfo("تنبيه", "الطباعة التلقائية مدعومة فقط في ويندوز مع توفر مكتبة pywin32")
                win.destroy()

        def do_copy():
            self.clipboard_clear()
            self.clipboard_append(invoice_text)
            messagebox.showinfo("تم", "تم نسخ الفاتورة للحافظة.")
            win.destroy()

        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="طباعة", font=("Arial", 12), width=12, command=do_print).pack(side="right", padx=5)
        tk.Button(button_frame, text="نسخ", font=("Arial", 12), width=12, command=do_copy).pack(side="right", padx=5)

    def print_text(self, text_widget):
        self.clipboard_clear()
        self.clipboard_append(text_widget.get("1.0", "end"))
        messagebox.showinfo("تم", "تم نسخ الفاتورة للحافظة. يمكنك لصقها في أي برنامج طباعة.")

    def close_window(self):
        self.destroy()
        if self.home_window:
            self.home_window.deiconify()

    def show_sales_list(self):
        win = tk.Toplevel(self)
        win.title("قائمة الفواتير (المبيعات)")
        win.geometry("950x550")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT DISTINCT customer FROM sales")
        customer_names = [row[0] for row in c.fetchall()]
        c.execute("SELECT DISTINCT product_name FROM sales")
        product_names = [row[0] for row in c.fetchall()]
        conn.close()

        filter_frame = tk.Frame(win)
        filter_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(filter_frame, text="اسم العميل:", font=("Arial", 11)).grid(row=0, column=0, padx=5, sticky="e")
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(filter_frame, textvariable=customer_var, width=15, values=customer_names)
        customer_combo.grid(row=0, column=1, padx=5, sticky="ew")

        tk.Label(filter_frame, text="اسم الصنف:", font=("Arial", 11)).grid(row=0, column=2, padx=5, sticky="e")
        prod_var = tk.StringVar()
        prod_combo = ttk.Combobox(filter_frame, textvariable=prod_var, width=15, values=product_names)
        prod_combo.grid(row=0, column=3, padx=5, sticky="ew")

        today = datetime.now().strftime("%Y-%m-%d")
        tk.Label(filter_frame, text="من تاريخ (yyyy-mm-dd):", font=("Arial", 11)).grid(row=0, column=4, padx=5)
        date_from_var = tk.StringVar(value=today)
        tk.Entry(filter_frame, textvariable=date_from_var, width=12).grid(row=0, column=5, padx=5)
        tk.Label(filter_frame, text="إلى تاريخ (yyyy-mm-dd):", font=("Arial", 11)).grid(row=0, column=6, padx=5)
        date_to_var = tk.StringVar(value=today)
        tk.Entry(filter_frame, textvariable=date_to_var, width=12).grid(row=0, column=7, padx=5)

        def do_filter():
            customer = customer_var.get().strip()
            prod = prod_var.get().strip()
            date_from = date_from_var.get().strip()
            date_to = date_to_var.get().strip()

            sql = "SELECT id, product_name, quantity, price, customer, date FROM sales WHERE 1=1"
            params = []
            if customer:
                sql += " AND customer LIKE ?"
                params.append(f"%{customer}%")
            if prod:
                sql += " AND product_name LIKE ?"
                params.append(f"%{prod}%")
            if date_from:
                sql += " AND date(date) >= date(?)"
                params.append(date_from)
            if date_to:
                sql += " AND date(date) <= date(?)"
                params.append(date_to)
            sql += " ORDER BY date DESC"

            for row in sales_tree.get_children():
                sales_tree.delete(row)
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute(sql, params)
            rows = c.fetchall()
            conn.close()
            for row in rows:
                sales_tree.insert("", "end", values=row)

        tk.Button(filter_frame, text="بحث", font=("Arial", 11, "bold"), command=do_filter).grid(row=0, column=8, padx=10)

        columns = ("id", "product_name", "quantity", "price", "customer", "date")
        headers = ["الرقم", "المنتج", "الكمية", "السعر", "العميل", "التاريخ"]
        sales_tree = ttk.Treeview(win, columns=columns, show="headings", height=20)
        for col, header in zip(columns, headers):
            sales_tree.heading(col, text=header)
            sales_tree.column(col, anchor="center", width=120, stretch=True)
        sales_tree.pack(fill="both", expand=True, padx=5, pady=5)

        def load_all_sales():
            for row in sales_tree.get_children():
                sales_tree.delete(row)
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT id, product_name, quantity, price, customer, date FROM sales ORDER BY date DESC")
            rows = c.fetchall()
            conn.close()
            for row in rows:
                sales_tree.insert("", "end", values=row)
        load_all_sales()

        def print_selected_invoice():
            selected = sales_tree.selection()
            if not selected:
                messagebox.showwarning("تنبيه", "اختر فاتورة للطباعة")
                return
            sales_id = int(sales_tree.item(selected[0])["values"][0])
            self.print_invoice_popup(sales_id=sales_id)

        tk.Button(win, text="طباعة الفاتورة", font=("Arial", 12), command=print_selected_invoice).pack(pady=5)
        tk.Button(win, text="رجوع", font=("Arial", 12), command=win.destroy).pack(pady=5)

def open_sales_window(home_window):
    SalesWindow(home_window, home_window)

def close_window(self):
        self.destroy()
        if self.home_window:
            self.home_window.deiconify()

if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    root.withdraw()
    SalesWindow(root, None)
    root.mainloop()