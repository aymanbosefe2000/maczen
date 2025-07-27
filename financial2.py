import tkinter as tk
from tkinter import ttk, messagebox

# ------------------------- قسم الأرباح -------------------------
class PrintPreviewProfit(tk.Toplevel):
    def __init__(self, parent, paid, remain, net_profit, table_data):
        super().__init__(parent)
        self.title("معاينة الطباعة")
        self.geometry("700x500")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        top = tk.Frame(self, bg="white")
        top.pack(fill="x", pady=10)
        tk.Label(top, text="المدفوع", font=("Arial", 11)).grid(row=0, column=0, padx=8)
        tk.Entry(top, width=10, font=("Arial", 11), justify="center", state="readonly", 
                 textvariable=tk.StringVar(value=paid)).grid(row=1, column=0)
        tk.Label(top, text="الباقي", font=("Arial", 11)).grid(row=0, column=1, padx=8)
        tk.Entry(top, width=10, font=("Arial", 11), justify="center", state="readonly", 
                 textvariable=tk.StringVar(value=remain)).grid(row=1, column=1)
        tk.Label(top, text="صافي الربح", font=("Arial", 11)).grid(row=0, column=2, padx=8)
        tk.Entry(top, width=10, font=("Arial", 11), justify="center", state="readonly", 
                 textvariable=tk.StringVar(value=net_profit)).grid(row=1, column=2)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, pady=10)
        columns = ("sales", "manufacturing", "expenses", "employees")
        headers = ["المبيعات", "تكلفة التصنيع", "المصروفات", "الموظفين"]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        for col, head in zip(columns, headers):
            tree.heading(col, text=head)
            tree.column(col, anchor="center", width=140)
        tree.pack(fill="both", expand=True)
        for row in table_data:
            tree.insert('', 'end', values=row)
        options = tk.Frame(self, pady=10)
        options.pack()
        tk.Label(options, text="عدد النسخ:", font=("Arial", 11)).grid(row=0, column=0, padx=8)
        self.copies_var = tk.IntVar(value=1)
        tk.Spinbox(options, from_=1, to=20, width=5, font=("Arial", 11), textvariable=self.copies_var).grid(row=0, column=1)
        tk.Label(options, text="حجم الصفحة:", font=("Arial", 11)).grid(row=0, column=2, padx=8)
        self.size_var = tk.StringVar(value="A4")
        tk.OptionMenu(options, self.size_var, "A4", "A5", "Letter", "Legal").grid(row=0, column=3)
        btns = tk.Frame(self)
        btns.pack(pady=12)
        tk.Button(btns, text="تأكيد الطباعة", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=self.confirm_print).pack(side="right", padx=10)
        tk.Button(btns, text="إلغاء", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=self.destroy).pack(side="right", padx=10)
    def confirm_print(self):
        copies = self.copies_var.get()
        page_size = self.size_var.get()
        messagebox.showinfo("طباعة", f"تم إرسال البيانات للطباعة.\nعدد النسخ: {copies}\nحجم الصفحة: {page_size}")
        self.destroy()

class ProfitSection(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("قسم الأرباح")
        self.geometry("900x450")
        self.configure(bg='white')

        main = tk.Frame(self, bg="white")
        main.pack(fill="both", expand=True, padx=8, pady=8)
        top = tk.Frame(main, bg="white")
        top.pack(fill="x", pady=4, anchor="n")
        tk.Label(top, text="التاريخ من", font=("Arial", 11), bg="white").pack(side="right", padx=2)
        self.from_entry = tk.Entry(top, width=12, font=("Arial", 11), justify="center")
        self.from_entry.pack(side="right")
        tk.Label(top, text="الى", font=("Arial", 11), bg="white").pack(side="right", padx=2)
        self.to_entry = tk.Entry(top, width=12, font=("Arial", 11), justify="center")
        self.to_entry.pack(side="right")
        search_btn = tk.Button(top, text="بحث", font=("Arial", 11), width=7, command=self.search_action)
        search_btn.pack(side="right", padx=4)
        print_btn = tk.Button(top, text="طباعة", font=("Arial", 11), width=7, command=self.print_action)
        print_btn.pack(side="right", padx=4)
        box_frame = tk.Frame(top, bg="white")
        box_frame.pack(side="right", padx=18)
        tk.Label(box_frame, text="المدفوع", font=("Arial", 11), bg="white").grid(row=0, column=0)
        self.paid = tk.Entry(box_frame, width=11, font=("Arial", 11), justify="center")
        self.paid.grid(row=1, column=0, padx=3)
        tk.Label(box_frame, text="الباقي", font=("Arial", 11), bg="white").grid(row=0, column=1)
        self.remain = tk.Entry(box_frame, width=11, font=("Arial", 11), justify="center")
        self.remain.grid(row=1, column=1, padx=3)
        tk.Label(box_frame, text="صافي الربح", font=("Arial", 11), bg="white").grid(row=0, column=2)
        self.net_profit = tk.Entry(box_frame, width=11, font=("Arial", 11), justify="center")
        self.net_profit.grid(row=1, column=2, padx=3)
        table_frame = tk.Frame(main, bg="white")
        table_frame.pack(fill="both", expand=True, pady=14)
        columns = ("sales", "manufacturing", "expenses", "employees")
        headers = ["المبيعات", "تكلفة التصنيع", "المصروفات", "الموظفين"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=9)
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=210)
        self.tree.pack(fill="both", expand=True)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
        self.search_action()
    def search_action(self):
        from_date = self.from_entry.get().strip()
        to_date = self.to_entry.get().strip()
        if from_date and to_date:
            sales_val = 12000
            paid_val = 9000
        else:
            sales_val = 8000
            paid_val = 8000
        remain_val = max(sales_val - paid_val, 0)
        manufacturing = 2500
        expenses = 1200
        employees = 1500
        net_profit = sales_val - manufacturing - expenses - employees
        self.paid.delete(0, tk.END)
        self.paid.insert(0, str(paid_val))
        self.remain.delete(0, tk.END)
        self.remain.insert(0, str(remain_val))
        self.net_profit.delete(0, tk.END)
        self.net_profit.insert(0, str(net_profit))
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree.insert('', 'end', values=(str(sales_val), str(manufacturing), str(expenses), str(employees)))
        self.tree.insert('', 'end', values=("", "", "", ""))
    def print_action(self):
        paid = self.paid.get()
        remain = self.remain.get()
        net_profit = self.net_profit.get()
        table_data = []
        for row in self.tree.get_children():
            table_data.append(self.tree.item(row)['values'])
        PrintPreviewProfit(self, paid, remain, net_profit, table_data)
    def close_window(self):
        self.destroy()

# ------------------------- قسم المصروفات -------------------------
class MsrofatWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("إدارة المصروفات")
        self.geometry("700x400")
        self.configure(bg='white')
        add_frame = tk.LabelFrame(self, text="إضافة مصروف جديد", font=("Arial", 11, "bold"), bg="white")
        add_frame.pack(fill="x", padx=12, pady=8)
        tk.Label(add_frame, text="القيمة:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=6, pady=6)
        self.value_entry = tk.Entry(add_frame, width=15, font=("Arial", 11), justify="center")
        self.value_entry.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(add_frame, text="السبب:", font=("Arial", 11), bg="white").grid(row=0, column=2, padx=6, pady=6)
        self.reason_entry = tk.Entry(add_frame, width=30, font=("Arial", 11), justify="center")
        self.reason_entry.grid(row=0, column=3, padx=6, pady=6)
        add_btn = tk.Button(add_frame, text="إضافة", font=("Arial", 11), width=8, command=self.add_expense)
        add_btn.grid(row=0, column=4, padx=8, pady=6)
        search_frame = tk.LabelFrame(self, text="بحث في المصروفات", font=("Arial", 11, "bold"), bg="white")
        search_frame.pack(fill="x", padx=12, pady=6)
        tk.Label(search_frame, text="من تاريخ:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=4)
        self.from_date = tk.Entry(search_frame, width=12, font=("Arial", 10), justify="center")
        self.from_date.grid(row=0, column=1, padx=4)
        tk.Label(search_frame, text="إلى تاريخ:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=4)
        self.to_date = tk.Entry(search_frame, width=12, font=("Arial", 10), justify="center")
        self.to_date.grid(row=0, column=3, padx=4)
        tk.Label(search_frame, text="اسم المصروف:", font=("Arial", 10), bg="white").grid(row=0, column=4, padx=4)
        self.name_search = tk.Entry(search_frame, width=18, font=("Arial", 10), justify="center")
        self.name_search.grid(row=0, column=5, padx=4)
        search_btn = tk.Button(search_frame, text="بحث", font=("Arial", 10), width=8, command=self.dummy_search)
        search_btn.grid(row=0, column=6, padx=6)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=12, pady=8)
        columns = ("id", "value", "reason", "date")
        headers = ["رقم", "القيمة", "السبب", "التاريخ"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
    def add_expense(self):
        value = self.value_entry.get().strip()
        reason = self.reason_entry.get().strip()
        if not value or not reason:
            messagebox.showwarning("تحذير", "يجب إدخال كل من القيمة والسبب.")
            return
        idx = len(self.tree.get_children()) + 1
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.tree.insert('', 'end', values=(idx, value, reason, today))
        messagebox.showinfo("تم", "تمت إضافة المصروف بنجاح.")
        self.value_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
    def dummy_search(self):
        messagebox.showinfo("بحث", "تم تنفيذ عملية البحث (تجريبي).")
    def close_window(self):
        self.destroy()

# ------------------------- قسم المواد الخام -------------------------
class MwadKhamWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("إدارة المواد الخام")
        self.geometry("750x450")
        self.configure(bg='white')
        self.products = ["سكر", "طحين", "زيت", "ملح"]
        self.entries = []
        add_frame = tk.LabelFrame(self, text="إضافة مادة خام", font=("Arial", 11, "bold"), bg="white")
        add_frame.pack(fill="x", padx=12, pady=8)
        tk.Label(add_frame, text="اسم الصنف:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=6, pady=6)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var, values=self.products, width=20, font=("Arial", 11))
        self.product_combo.set("")
        self.product_combo.grid(row=0, column=1, padx=6, pady=6)
        self.product_combo.bind("<KeyRelease>", self.on_product_typing)
        tk.Label(add_frame, text="الكمية:", font=("Arial", 11), bg="white").grid(row=0, column=2, padx=6, pady=6)
        self.qty_entry = tk.Entry(add_frame, width=10, font=("Arial", 11), justify="center")
        self.qty_entry.grid(row=0, column=3, padx=6, pady=6)
        tk.Label(add_frame, text="السعر:", font=("Arial", 11), bg="white").grid(row=0, column=4, padx=6, pady=6)
        self.price_entry = tk.Entry(add_frame, width=10, font=("Arial", 11), justify="center")
        self.price_entry.grid(row=0, column=5, padx=6, pady=6)
        add_btn = tk.Button(add_frame, text="إضافة", font=("Arial", 11), width=9, command=self.add_product)
        add_btn.grid(row=0, column=6, padx=8, pady=6)
        search_frame = tk.LabelFrame(self, text="بحث عن صنف", font=("Arial", 11, "bold"), bg="white")
        search_frame.pack(fill="x", padx=12, pady=6)
        tk.Label(search_frame, text="اسم الصنف:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=4)
        self.search_entry = tk.Entry(search_frame, width=18, font=("Arial", 10), justify="center")
        self.search_entry.grid(row=0, column=1, padx=4)
        search_btn = tk.Button(search_frame, text="بحث", font=("Arial", 10), width=8, command=self.search_product)
        search_btn.grid(row=0, column=2, padx=6)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=12, pady=8)
        columns = ("name", "qty", "price", "date")
        headers = ["اسم الصنف", "الكمية", "السعر", "تاريخ الإضافة"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=130)
        self.tree.pack(fill="both", expand=True)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
        self.refresh_table()
    def on_product_typing(self, event):
        value = self.product_combo.get()
        if value == "":
            self.product_combo['values'] = self.products
        else:
            filtered = [item for item in self.products if value in item]
            self.product_combo['values'] = filtered
    def add_product(self):
        name = self.product_var.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        from datetime import datetime
        if not name or not qty or not price:
            messagebox.showwarning("تحذير", "يرجى إدخال جميع الحقول.")
            return
        try:
            qty = float(qty)
            price = float(price)
        except ValueError:
            messagebox.showwarning("تحذير", "الكمية والسعر يجب أن تكون أرقام.")
            return
        if name not in self.products:
            self.products.append(name)
            self.product_combo['values'] = self.products
        self.entries.insert(0, (name, qty, price, datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.refresh_table()
        messagebox.showinfo("تم", "تمت إضافة المادة الخام بنجاح.")
        self.product_var.set("")
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
    def refresh_table(self, filter_name=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for entry in self.entries:
            if filter_name is None or filter_name in entry[0]:
                self.tree.insert('', 'end', values=entry)
    def search_product(self):
        name = self.search_entry.get().strip()
        if name:
            self.refresh_table(filter_name=name)
        else:
            self.refresh_table()
    def close_window(self):
        self.destroy()

# ------------------------- قسم تكلفة التصنيع -------------------------
class TklefaWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("تكلفة التصنيع")
        self.geometry("750x450")
        self.configure(bg='white')
        self.products = ["منتج 1", "منتج 2", "منتج 3", "منتج 4"]
        self.entries = []
        add_frame = tk.LabelFrame(self, text="إضافة تكلفة تصنيع", font=("Arial", 11, "bold"), bg="white")
        add_frame.pack(fill="x", padx=12, pady=8)
        tk.Label(add_frame, text="اسم المنتج:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=6, pady=6)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var, values=self.products, width=20, font=("Arial", 11))
        self.product_combo.grid(row=0, column=1, padx=6, pady=6)
        self.product_combo.set("")
        tk.Label(add_frame, text="سعر اليد العاملة:", font=("Arial", 11), bg="white").grid(row=0, column=2, padx=6, pady=6)
        self.labor_entry = tk.Entry(add_frame, width=10, font=("Arial", 11), justify="center")
        self.labor_entry.grid(row=0, column=3, padx=6, pady=6)
        self.labor_entry.bind("<KeyRelease>", self.update_total)
        tk.Label(add_frame, text="سعر المواد الخام:", font=("Arial", 11), bg="white").grid(row=0, column=4, padx=6, pady=6)
        self.raw_entry = tk.Entry(add_frame, width=10, font=("Arial", 11), justify="center")
        self.raw_entry.grid(row=0, column=5, padx=6, pady=6)
        self.raw_entry.bind("<KeyRelease>", self.update_total)
        tk.Label(add_frame, text="تكلفة التصنيع:", font=("Arial", 11), bg="white").grid(row=0, column=6, padx=6, pady=6)
        self.total_var = tk.StringVar(value="0")
        self.total_entry = tk.Entry(add_frame, width=12, font=("Arial", 11), justify="center", state="readonly", textvariable=self.total_var)
        self.total_entry.grid(row=0, column=7, padx=6, pady=6)
        add_btn = tk.Button(add_frame, text="إضافة", font=("Arial", 11), width=9, command=self.add_cost)
        add_btn.grid(row=0, column=8, padx=8, pady=6)
        search_frame = tk.LabelFrame(self, text="بحث باسم المنتج", font=("Arial", 11, "bold"), bg="white")
        search_frame.pack(fill="x", padx=12, pady=6)
        tk.Label(search_frame, text="اسم المنتج:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=4)
        self.search_entry = tk.Entry(search_frame, width=18, font=("Arial", 10), justify="center")
        self.search_entry.grid(row=0, column=1, padx=4)
        search_btn = tk.Button(search_frame, text="بحث", font=("Arial", 10), width=8, command=self.search_product)
        search_btn.grid(row=0, column=2, padx=6)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=12, pady=8)
        columns = ("product", "labor", "raw", "total", "date")
        headers = ["اسم المنتج", "سعر اليد العاملة", "سعر المواد الخام", "تكلفة التصنيع", "تاريخ الإضافة"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=110)
        self.tree.pack(fill="both", expand=True)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
        self.refresh_table()
    def update_total(self, event=None):
        try:
            labor = float(self.labor_entry.get())
        except:
            labor = 0
        try:
            raw = float(self.raw_entry.get())
        except:
            raw = 0
        self.total_var.set(str(labor + raw))
    def add_cost(self):
        product = self.product_var.get().strip()
        labor = self.labor_entry.get().strip()
        raw = self.raw_entry.get().strip()
        total = self.total_var.get()
        from datetime import datetime
        if not product or not labor or not raw:
            messagebox.showwarning("تحذير", "يرجى إدخال جميع الحقول.")
            return
        try:
            labor_v = float(labor)
            raw_v = float(raw)
            total_v = float(total)
        except ValueError:
            messagebox.showwarning("تحذير", "سعر اليد العاملة والمواد الخام أرقام فقط.")
            return
        self.entries.insert(0, (product, labor, raw, total, datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.refresh_table()
        messagebox.showinfo("تم", "تمت إضافة تكلفة التصنيع بنجاح.")
        self.product_var.set("")
        self.labor_entry.delete(0, tk.END)
        self.raw_entry.delete(0, tk.END)
        self.total_var.set("0")
    def refresh_table(self, filter_name=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for entry in self.entries:
            if filter_name is None or filter_name in entry[0]:
                self.tree.insert('', 'end', values=entry)
    def search_product(self):
        name = self.search_entry.get().strip()
        if name:
            self.refresh_table(filter_name=name)
        else:
            self.refresh_table()
    def close_window(self):
        self.destroy()

# ------------------------- قسم العملاء والفواتير -------------------------
class PrintPreviewInvoice(tk.Toplevel):
    def __init__(self, parent, customer_name, table_data, total, paid, remain):
        super().__init__(parent)
        self.title("معاينة الطباعة")
        self.geometry("850x500")
        self.focus_set()
        self.grab_set()
        tk.Label(self, text=f"اسم العميل: {customer_name}", font=("Arial", 14, "bold"), fg="#1a237e").pack(pady=5)
        tk.Label(self, text="معاينة الفواتير", font=("Arial", 13, "bold")).pack(pady=2)
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("product", "qty", "price", "value", "paid", "remain", "date")
        headers = ["اسم المنتج", "الكمية", "السعر", "القيمة", "المدفوع", "الباقي", "تاريخ الفاتورة"]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for col, head in zip(columns, headers):
            tree.heading(col, text=head)
            tree.column(col, anchor="center", width=110)
        tree.pack(fill="both", expand=True)
        for row in table_data:
            tree.insert('', 'end', values=row)
        sums = tk.Frame(self)
        sums.pack(pady=5)
        tk.Label(sums, text=f"الإجمالي الكلي: {total}", font=("Arial", 11)).grid(row=0, column=0, padx=10)
        tk.Label(sums, text=f"إجمالي المدفوع: {paid}", font=("Arial", 11)).grid(row=0, column=1, padx=10)
        tk.Label(sums, text=f"إجمالي الباقي: {remain}", font=("Arial", 11)).grid(row=0, column=2, padx=10)
        options = tk.Frame(self)
        options.pack(pady=10)
        tk.Label(options, text="عدد النسخ:", font=("Arial", 11)).grid(row=0, column=0, padx=8)
        self.copies_var = tk.IntVar(value=1)
        tk.Spinbox(options, from_=1, to=20, width=5, font=("Arial", 11), textvariable=self.copies_var).grid(row=0, column=1)
        tk.Label(options, text="حجم الصفحة:", font=("Arial", 11)).grid(row=0, column=2, padx=8)
        self.size_var = tk.StringVar(value="A4")
        tk.OptionMenu(options, self.size_var, "A4", "A5", "Letter", "Legal").grid(row=0, column=3)
        btns = tk.Frame(self)
        btns.pack(pady=12)
        tk.Button(btns, text="تأكيد الطباعة", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=self.confirm_print).pack(side="right", padx=10)
        tk.Button(btns, text="إلغاء", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=self.destroy).pack(side="right", padx=10)
    def confirm_print(self):
        copies = self.copies_var.get()
        page_size = self.size_var.get()
        messagebox.showinfo("طباعة", f"تم إرسال البيانات للطباعة.\nعدد النسخ: {copies}\nحجم الصفحة: {page_size}")
        self.destroy()

class CustomersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("إدارة العملاء والفواتير")
        self.geometry("1050x600")
        self.configure(bg='white')
        self.customers = ["أحمد", "منى", "سعيد"]
        self.invoices = [
            ("أحمد", "سكر", 5, 50, 250, 250, 0, "2025-07-15"),
            ("أحمد", "طحين", 2, 100, 200, 150, 50, "2025-07-16"),
            ("منى", "ملح", 3, 30, 90, 60, 30, "2025-07-16"),
            ("سعيد", "زيت", 1, 200, 200, 100, 100, "2025-07-17"),
            ("أحمد", "زيت", 2, 180, 360, 360, 0, "2025-07-19"),
            ("منى", "سكر", 4, 55, 220, 120, 100, "2025-07-20")
        ]
        self.filtered_invoices = self.invoices.copy()
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=10, pady=8)
        tk.Label(top, text="اختر العميل:", font=("Arial", 12), bg="white").pack(side="right", padx=6)
        self.cust_var = tk.StringVar()
        self.cust_combo = ttk.Combobox(top, textvariable=self.cust_var, values=self.customers, width=14, font=("Arial", 12))
        self.cust_combo.pack(side="right", padx=6)
        self.cust_combo.bind("<<ComboboxSelected>>", self.on_customer_select)
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(fill="x", padx=10)
        tk.Label(search_frame, text="بحث باسم الزبون:", font=("Arial", 10), bg="white").pack(side="right", padx=2)
        self.name_search_entry = tk.Entry(search_frame, width=12, font=("Arial", 10))
        self.name_search_entry.pack(side="right", padx=2)
        tk.Label(search_frame, text="بحث باسم المنتج:", font=("Arial", 10), bg="white").pack(side="right", padx=2)
        self.prod_search_entry = tk.Entry(search_frame, width=12, font=("Arial", 10))
        self.prod_search_entry.pack(side="right", padx=2)
        tk.Label(search_frame, text="من تاريخ:", font=("Arial", 10), bg="white").pack(side="right", padx=2)
        self.from_date_entry = tk.Entry(search_frame, width=10, font=("Arial", 10))
        self.from_date_entry.pack(side="right", padx=2)
        tk.Label(search_frame, text="إلى تاريخ:", font=("Arial", 10), bg="white").pack(side="right", padx=2)
        self.to_date_entry = tk.Entry(search_frame, width=10, font=("Arial", 10))
        self.to_date_entry.pack(side="right", padx=2)
        search_btn = tk.Button(search_frame, text="بحث", font=("Arial", 10), width=8, command=self.search_invoices)
        search_btn.pack(side="right", padx=6)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=8)
        columns = ("product", "qty", "price", "value", "paid", "remain", "date")
        headers = ["اسم المنتج", "الكمية", "السعر", "القيمة", "المدفوع", "الباقي", "تاريخ الفاتورة"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, selectmode="extended")
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)
        sums_frame = tk.Frame(self, bg="white")
        sums_frame.pack(fill="x", padx=10, pady=5)
        self.total_var = tk.StringVar(value="0")
        self.paid_var = tk.StringVar(value="0")
        self.remain_var = tk.StringVar(value="0")
        tk.Label(sums_frame, text="الإجمالي الكلي:", font=("Arial", 11), bg="white").pack(side="right", padx=12)
        tk.Entry(sums_frame, textvariable=self.total_var, width=10, font=("Arial", 11), state="readonly", justify="center").pack(side="right")
        tk.Label(sums_frame, text="إجمالي المدفوع:", font=("Arial", 11), bg="white").pack(side="right", padx=12)
        tk.Entry(sums_frame, textvariable=self.paid_var, width=10, font=("Arial", 11), state="readonly", justify="center").pack(side="right")
        tk.Label(sums_frame, text="إجمالي الباقي:", font=("Arial", 11), bg="white").pack(side="right", padx=12)
        tk.Entry(sums_frame, textvariable=self.remain_var, width=10, font=("Arial", 11), state="readonly", justify="center").pack(side="right")
        print_btn = tk.Button(self, text="طباعة", font=("Arial", 13), bg="#2196F3", fg="white", width=10, command=self.print_preview)
        print_btn.pack(pady=10)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
        self.refresh_table()
    def on_customer_select(self, event=None):
        name = self.cust_var.get().strip()
        self.filtered_invoices = [row for row in self.invoices if row[0] == name]
        self.refresh_table()
    def search_invoices(self):
        name = self.name_search_entry.get().strip()
        prod = self.prod_search_entry.get().strip()
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()
        results = self.invoices
        if name:
            results = [row for row in results if name in row[0]]
        if prod:
            results = [row for row in results if prod in row[1]]
        if from_date:
            results = [row for row in results if row[7] >= from_date]
        if to_date:
            results = [row for row in results if row[7] <= to_date]
        self.filtered_invoices = results
        self.refresh_table()
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        total = paid = remain = 0
        for row in self.filtered_invoices:
            self.tree.insert('', 'end', values=row[1:])
            total += row[4]
            paid += row[5]
            remain += row[6]
        self.total_var.set(str(total))
        self.paid_var.set(str(paid))
        self.remain_var.set(str(remain))
    def print_preview(self):
        selected = self.tree.selection()
        if selected:
            table_data = [self.tree.item(item)["values"] for item in selected]
        else:
            table_data = [self.tree.item(item)["values"] for item in self.tree.get_children()]
        customer_name = self.cust_var.get().strip() or "-"
        PrintPreviewInvoice(self, customer_name, table_data, self.total_var.get(), self.paid_var.get(), self.remain_var.get())
    def close_window(self):
        self.destroy()

# ------------------------- قسم الموظفين والمرتبات -------------------------
class PrintPreviewSalary(tk.Toplevel):
    def __init__(self, parent, table_data, filter_title):
        super().__init__(parent)
        self.title("معاينة الطباعة")
        self.geometry("900x500")
        self.focus_set()
        self.grab_set()
        tk.Label(self, text=f"تقرير المرتبات: {filter_title}", font=("Arial", 14, "bold"), fg="#1a237e").pack(pady=5)
        columns = ("name", "days", "salary", "type", "line")
        headers = ["اسم الموظف", "أيام الحضور", "المرتب", "نوع الخلاص", "الخط"]
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col, head in zip(columns, headers):
            tree.heading(col, text=head)
            tree.column(col, anchor="center", width=140)
        tree.pack(fill="both", expand=True)
        for row in table_data:
            tree.insert('', 'end', values=row)
        options = tk.Frame(self)
        options.pack(pady=10)
        tk.Label(options, text="عدد النسخ:", font=("Arial", 11)).grid(row=0, column=0, padx=8)
        self.copies_var = tk.IntVar(value=1)
        tk.Spinbox(options, from_=1, to=20, width=5, font=("Arial", 11), textvariable=self.copies_var).grid(row=0, column=1)
        tk.Label(options, text="حجم الصفحة:", font=("Arial", 11)).grid(row=0, column=2, padx=8)
        self.size_var = tk.StringVar(value="A4")
        tk.OptionMenu(options, self.size_var, "A4", "A5", "Letter", "Legal").grid(row=0, column=3)
        btns = tk.Frame(self)
        btns.pack(pady=12)
        tk.Button(btns, text="تأكيد الطباعة", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=self.confirm_print).pack(side="right", padx=10)
        tk.Button(btns, text="إلغاء", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=self.destroy).pack(side="right", padx=10)
    def confirm_print(self):
        copies = self.copies_var.get()
        page_size = self.size_var.get()
        messagebox.showinfo("طباعة", f"تم إرسال البيانات للطباعة.\nعدد النسخ: {copies}\nحجم الصفحة: {page_size}")
        self.destroy()

class EmployeesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("إدارة الموظفين والحضور والمرتبات")
        self.geometry("1200x600")
        self.configure(bg='white')
        self.employees_settings = {
            "محمد": {"type": "يومي", "daily_wage": 150, "line": "الخيط", "ratio": None},
            "أحمد": {"type": "نسبة", "daily_wage": None, "line": "التعبئة", "ratio": 2},
            "سعاد": {"type": "يومي", "daily_wage": 120, "line": "المعالجة", "ratio": None},
            "منى": {"type": "نسبة", "daily_wage": None, "line": "الفرز", "ratio": 1.5}
        }
        self.employees = list(self.employees_settings.keys())
        self.attendance = [
            ("محمد", "2025-07-01"),
            ("محمد", "2025-07-02"),
            ("أحمد", "2025-07-01"),
            ("أحمد", "2025-07-02"),
            ("أحمد", "2025-07-03"),
            ("منى", "2025-07-01"),
            ("منى", "2025-07-03"),
            ("سعاد", "2025-07-01"),
            ("سعاد", "2025-07-03"),
            ("منى", "2025-06-01"),
        ]
        self.line_production = [
            ("الخيط", "2025-07-01", 100),
            ("الخيط", "2025-07-02", 80),
            ("التعبئة", "2025-07-01", 40),
            ("التعبئة", "2025-07-02", 50),
            ("التعبئة", "2025-07-03", 60),
            ("الفرز", "2025-07-01", 30),
            ("الفرز", "2025-07-03", 20),
            ("المعالجة", "2025-07-01", 70),
            ("المعالجة", "2025-07-03", 90),
            ("الفرز", "2025-06-01", 40),
        ]
        self.filtered_data = []
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=10, pady=8)
        tk.Label(top, text="اسم الموظف:", font=("Arial", 12), bg="white").pack(side="right", padx=6)
        self.emp_var = tk.StringVar()
        self.emp_combo = ttk.Combobox(top, textvariable=self.emp_var, values=["الكل"] + self.employees, width=14, font=("Arial", 12))
        self.emp_combo.set("الكل")
        self.emp_combo.pack(side="right", padx=6)
        tk.Label(top, text="من تاريخ:", font=("Arial", 11), bg="white").pack(side="right", padx=2)
        self.from_entry = tk.Entry(top, width=12, font=("Arial", 11), justify="center")
        self.from_entry.pack(side="right", padx=2)
        tk.Label(top, text="إلى تاريخ:", font=("Arial", 11), bg="white").pack(side="right", padx=2)
        self.to_entry = tk.Entry(top, width=12, font=("Arial", 11), justify="center")
        self.to_entry.pack(side="right", padx=2)
        search_btn = tk.Button(top, text="بحث", font=("Arial", 11), width=8, command=self.filter_data)
        search_btn.pack(side="right", padx=8)
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("name", "days", "salary", "type", "line")
        headers = ["اسم الموظف", "أيام الحضور", "المرتب", "نوع الخلاص", "الخط"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16, selectmode="extended")
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center", width=150 if col == "name" else 110)
        self.tree.pack(fill="both", expand=True)
        print_btn = tk.Button(self, text="طباعة", font=("Arial", 13), bg="#2196F3", fg="white", width=10, command=self.print_preview)
        print_btn.pack(pady=10)
        # زر رجوع
        back_btn = tk.Button(self, text="رجوع", font=("Arial", 11), bg="#eee", width=8, command=self.close_window)
        back_btn.pack(side="bottom", pady=8)
        self.filter_data()
    def filter_data(self):
        emp = self.emp_var.get().strip()
        if emp == "الكل":
            emp = None
        from_date = self.from_entry.get().strip()
        to_date = self.to_entry.get().strip()
        filtered_attendance = []
        for name, date in self.attendance:
            if emp and name != emp:
                continue
            if from_date and date < from_date:
                continue
            if to_date and date > to_date:
                continue
            filtered_attendance.append((name, date))
        summary = {}
        for name, date in filtered_attendance:
            if name not in summary:
                summary[name] = {"days": 0, "dates": []}
            summary[name]["days"] += 1
            summary[name]["dates"].append(date)
        self.filtered_data = []
        for name in summary:
            settings = self.employees_settings.get(name, {})
            emp_type = settings.get("type", "-")
            line = settings.get("line", "-")
            ratio = settings.get("ratio")
            daily_wage = settings.get("daily_wage")
            salary = 0
            if emp_type == "يومي":
                salary = summary[name]["days"] * (daily_wage or 0)
            elif emp_type == "نسبة":
                for day in summary[name]["dates"]:
                    produced = self.get_line_production(line, day)
                    salary += (ratio or 0) * produced
            self.filtered_data.append((name, summary[name]["days"], salary, emp_type, line))
        self.refresh_table()
    def get_line_production(self, line, day):
        for l, d, produced in self.line_production:
            if l == line and d == day:
                return produced
        return 0
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.filtered_data:
            self.tree.insert('', 'end', values=row)
    def print_preview(self):
        selected = self.tree.selection()
        if selected:
            table_data = [self.tree.item(item)["values"] for item in selected]
            if len(selected) == 1:
                filter_title = f"الموظف: {table_data[0][0]}"
            else:
                filter_title = "الموظفين المحددين"
        else:
            table_data = [self.tree.item(item)["values"] for item in self.tree.get_children()]
            filter_title = "جميع الموظفين" if self.emp_var.get() == "الكل" else f"الموظف: {self.emp_var.get()}"
        if not table_data:
            messagebox.showwarning("تنبيه", "لا توجد بيانات للمعاينة والطباعة.")
            return
        PrintPreviewSalary(self, table_data, filter_title)
    def close_window(self):
        self.destroy()
         # زر الرجوع
        btn_back = tk.Button(top, text="رجوع", font=("Arial", 13, "bold"), width=10, command=self.on_close)
        btn_back.pack(side="left", padx=12)

# ------------------------- النافذة الرئيسية -------------------------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("برنامج إدارة المالية")
        self.geometry("340x420")
        self.configure(bg='white')
        tk.Label(self, text="النظام المالي الشامل", font=("Arial", 15, "bold"), fg="#1565c0", bg='white').pack(pady=18)
        sections = [
            ("قسم الأرباح", self.open_profits),
            ("قسم المصروفات", self.open_msrofat),
            ("قسم المواد الخام", self.open_mwadkham),
            ("قسم تكلفة التصنيع", self.open_tklefa),
            ("قسم العملاء والفواتير", self.open_customers),
            ("قسم الموظفين والمرتبات", self.open_employees),
        ]
        self.windows = {}
        for i, (label, cmd) in enumerate(sections):
            btn = tk.Button(self, text=label, font=("Arial", 13), width=22, height=2, bg="#e3f2fd", command=cmd)
            btn.pack(pady=7)
        tk.Label(self, text="by alamera9894", font=("Arial", 9), fg="#aaa", bg='white').pack(side="bottom", pady=8)
    def _safe_open(self, key, cls):
        if key in self.windows and self.windows[key].winfo_exists():
            self.windows[key].focus_set()
            return
        self.windows[key] = cls(self)
    def open_profits(self):
        self._safe_open("profits", ProfitSection)
    def open_msrofat(self):
        self._safe_open("msrofat", MsrofatWindow)
    def open_mwadkham(self):
        self._safe_open("mwadkham", MwadKhamWindow)
    def open_tklefa(self):
        self._safe_open("tklefa", TklefaWindow)
    def open_customers(self):
        self._safe_open("customers", CustomersWindow)
    def open_employees(self):
        self._safe_open("employees", EmployeesWindow)

if __name__ == "__main__":
    MainApp().mainloop()