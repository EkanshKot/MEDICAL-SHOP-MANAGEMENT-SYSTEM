# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26  4 10:31:18 2025

@author: ekansh
"""

"""
MEDICAL SHOP MANAGEMENT SYSTEM

"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, timedelta
import os

class MedicalShopSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Shop Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#e8f4f8')
        
        
        self.conn = sqlite3.connect('medical_shop.db')
        self.create_tables()
        self.load_sample_data()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                generic_name TEXT,
                batch_no TEXT UNIQUE,
                expiry_date TEXT,
                manufacturer TEXT,
                quantity INTEGER DEFAULT 0,
                mrp REAL DEFAULT 0.0,
                selling_price REAL DEFAULT 0.0,
                category TEXT,
                added_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT,
                medicine_id INTEGER,
                qty_sold INTEGER,
                total_amount REAL,
                sale_date TEXT,
                customer_name TEXT,
                FOREIGN KEY(medicine_id) REFERENCES medicines(id)
            )
        ''')
        self.conn.commit()
    
    def load_sample_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines")
        if cursor.fetchone()[0] == 0:
            sample_medicines = [
                ("Paracetamol 500mg", "Paracetamol", "PAR001", "2026-12-31", "Cipla", 100, 2.50, 2.00, "Pain Relief"),
                ("Amoxicillin 500mg", "Amoxicillin", "AMO002", "2026-11-30", "Sun Pharma", 75, 4.50, 3.80, "Antibiotic"),
                ("Aspirin 150mg", "Aspirin", "ASP003", "2026-10-15", "GSK", 200, 1.20, 1.00, "Pain Relief"),
                ("Cetirizine 10mg", "Cetirizine", "CET004", "2026-09-30", "Mankind", 150, 1.80, 1.50, "Antihistamine"),
                ("Metformin 500mg", "Metformin", "MET005", "2026-12-15", "Lupin", 80, 3.20, 2.80, "Diabetes")
            ]
            
            cursor.executemany('''
                INSERT INTO medicines(name, generic_name, batch_no, expiry_date, manufacturer, 
                                     quantity, mrp, selling_price, category, added_date)
                VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', [(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], datetime.now().strftime("%Y-%m-%d")) 
                  for m in sample_medicines])
            self.conn.commit()
            messagebox.showinfo("Success", "Sample data loaded! Ready to use.")
    
    def create_widgets(self):
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        self.create_dashboard()
        
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="💊 Inventory")
        self.create_inventory()
        
        self.billing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.billing_frame, text="💳 Billing")
        self.create_billing()
        
        
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="📈 Reports")
        self.create_reports()
    
    def create_dashboard(self):
        
        stats_frame = ttk.LabelFrame(self.dashboard_frame, text="Quick Stats", padding=20)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        
        ttk.Label(stats_frame, text="Total Medicines:").grid(row=0, column=0, sticky=tk.W, padx=10)
        self.total_meds = ttk.Label(stats_frame, text="0", font=('Arial', 16, 'bold'), foreground='blue')
        self.total_meds.grid(row=0, column=1, padx=10)
        
        # Low stock
        ttk.Label(stats_frame, text="Low Stock:").grid(row=0, column=2, sticky=tk.W, padx=10)
        self.low_stock = ttk.Label(stats_frame, text="0", font=('Arial', 16, 'bold'), foreground='orange')
        self.low_stock.grid(row=0, column=3, padx=10)
        
        
        ttk.Label(stats_frame, text="Today's Sales:").grid(row=1, column=0, sticky=tk.W, padx=10)
        self.today_sales = ttk.Label(stats_frame, text="₹0", font=('Arial', 16, 'bold'), foreground='green')
        self.today_sales.grid(row=1, column=1, padx=10)
        
        self.update_dashboard()
        
        
        actions_frame = ttk.LabelFrame(self.dashboard_frame, text="Quick Actions", padding=20)
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(actions_frame, text="➕ Add Medicine", command=lambda: self.notebook.select(1)).pack(side=tk.LEFT, padx=10)
        ttk.Button(actions_frame, text="💳 New Bill", command=lambda: self.notebook.select(2)).pack(side=tk.LEFT, padx=10)
        ttk.Button(actions_frame, text="📊 View Reports", command=lambda: self.notebook.select(3)).pack(side=tk.LEFT, padx=10)
        ttk.Button(actions_frame, text="🔄 Refresh", command=self.update_dashboard).pack(side=tk.LEFT, padx=10)
    
    def update_dashboard(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines")
        self.total_meds.config(text=cursor.fetchone()[0])
        
        cursor.execute("SELECT COUNT(*) FROM medicines WHERE quantity < 10")
        self.low_stock.config(text=cursor.fetchone()[0])
        
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT SUM(total_amount) FROM sales WHERE sale_date=?", (today,))
        sales = cursor.fetchone()[0] or 0
        self.today_sales.config(text=f"₹{sales:.2f}")
    
    def create_inventory(self):
        # Search frame
        search_frame = ttk.Frame(self.inventory_frame)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.search_medicines)
        
        ttk.Button(search_frame, text="➕ Add New", command=self.add_medicine).pack(side=tk.RIGHT, padx=5)
        ttk.Button(search_frame, text="✏️ Edit", command=self.edit_medicine).pack(side=tk.RIGHT, padx=5)
        ttk.Button(search_frame, text="🗑️ Delete", command=self.delete_medicine).pack(side=tk.RIGHT, padx=5)
        
        
        columns = ('ID', 'Name', 'Generic', 'Batch', 'Qty', 'MRP', 'Sell', 'Expiry', 'Category')
        self.med_tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.med_tree.heading(col, text=col)
            self.med_tree.column(col, width=100)
        
        self.med_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.med_tree.bind('<<TreeviewSelect>>', self.on_med_select)
        
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, command=self.med_tree.yview)
        self.med_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_medicines()
    
    def search_medicines(self, event=None):
        search_term = self.search_var.get().lower()
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, generic_name, batch_no, quantity, mrp, selling_price, 
                   expiry_date, category 
            FROM medicines 
            WHERE name LIKE ? OR generic_name LIKE ? OR batch_no LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        for row in cursor.fetchall():
            self.med_tree.insert('', tk.END, values=row)
    
    def refresh_medicines(self):
        self.search_var.set('')
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, generic_name, batch_no, quantity, mrp, selling_price, expiry_date, category FROM medicines ORDER BY name")
        for row in cursor.fetchall():
            self.med_tree.insert('', tk.END, values=row)
    
    def on_med_select(self, event):
        selection = self.med_tree.selection()
        self.selected_med = selection[0] if selection else None
    
    def add_medicine(self):
        self.med_window('Add Medicine', 'add')
    
    def edit_medicine(self):
        if hasattr(self, 'selected_med') and self.selected_med:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM medicines WHERE id=?", (self.med_tree.item(self.selected_med)['values'][0],))
            med = cursor.fetchone()
            if med:
                self.med_window('Edit Medicine', 'edit', med)
        else:
            messagebox.showwarning("Warning", "Select a medicine to edit!")
    
    def delete_medicine(self):
        if hasattr(self, 'selected_med') and self.selected_med:
            med_id = self.med_tree.item(self.selected_med)['values'][0]
            if messagebox.askyesno("Confirm", "Delete this medicine?"):
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
                self.conn.commit()
                self.refresh_medicines()
                messagebox.showinfo("Success", "Medicine deleted!")
        else:
            messagebox.showwarning("Warning", "Select a medicine to delete!")
    
    def med_window(self, title, mode, med=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("500x600")
        win.grab_set()
        
       
        fields = ['name', 'generic_name', 'batch_no', 'expiry_date', 'manufacturer', 
                 'quantity', 'mrp', 'selling_price', 'category']
        entries = {}
        
        ttk.Label(win, text="Medicine Name:").pack(pady=5)
        entries['name'] = ttk.Entry(win, width=50)
        entries['name'].pack()
        
        ttk.Label(win, text="Generic Name:").pack(pady=5)
        entries['generic_name'] = ttk.Entry(win, width=50)
        entries['generic_name'].pack()
        
        ttk.Label(win, text="Batch No:").pack(pady=5)
        entries['batch_no'] = ttk.Entry(win, width=50)
        entries['batch_no'].pack()
        
        ttk.Label(win, text="Expiry Date (YYYY-MM-DD):").pack(pady=5)
        entries['expiry_date'] = ttk.Entry(win, width=50)
        entries['expiry_date'].pack()
        
        ttk.Label(win, text="Manufacturer:").pack(pady=5)
        entries['manufacturer'] = ttk.Entry(win, width=50)
        entries['manufacturer'].pack()
        
        ttk.Label(win, text="Quantity:").pack(pady=5)
        entries['quantity'] = ttk.Entry(win, width=50)
        entries['quantity'].pack()
        
        ttk.Label(win, text="MRP:").pack(pady=5)
        entries['mrp'] = ttk.Entry(win, width=50)
        entries['mrp'].pack()
        
        ttk.Label(win, text="Selling Price:").pack(pady=5)
        entries['selling_price'] = ttk.Entry(win, width=50)
        entries['selling_price'].pack()
        
        ttk.Label(win, text="Category:").pack(pady=5)
        entries['category'] = ttk.Entry(win, width=50)
        entries['category'].pack()
        
        if mode == 'edit' and med:
            for i, field in enumerate(fields):
                entries[field].insert(0, med[i+1])
        
        def save():
            try:
                data = [entries[f].get() for f in fields]
                if mode == 'add':
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        INSERT INTO medicines(name, generic_name, batch_no, expiry_date, manufacturer, 
                                            quantity, mrp, selling_price, category, added_date)
                        VALUES(?,?,?,?,?,?,?,?,?,?)
                    ''', tuple(data) + [datetime.now().strftime("%Y-%m-%d")])
                    self.conn.commit()
                    messagebox.showinfo("Success", "Medicine added!")
                else:  # edit
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        UPDATE medicines SET name=?, generic_name=?, batch_no=?, expiry_date=?,
                        manufacturer=?, quantity=?, mrp=?, selling_price=?, category=?
                        WHERE id=?
                    ''', tuple(data) + (med[0],))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Medicine updated!")
                
                win.destroy()
                self.refresh_medicines()
                self.update_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(win, text="Save", command=save).pack(pady=20)
    
    def create_billing(self):
        
        customer_frame = ttk.LabelFrame(self.billing_frame, text="Customer Details", padding=10)
        customer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(customer_frame, text="Customer Name:").grid(row=0, column=0)
        self.cust_name = ttk.Entry(customer_frame, width=30)
        self.cust_name.grid(row=0, column=1, padx=5)
        
        ttk.Label(customer_frame, text="Phone:").grid(row=0, column=2)
        self.cust_phone = ttk.Entry(customer_frame, width=20)
        self.cust_phone.grid(row=0, column=3, padx=5)
        
        # Medicine search
        search_frame = ttk.LabelFrame(self.billing_frame, text="Add Medicines", padding=10)
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(search_frame, text="Search Medicine:").pack(side=tk.LEFT)
        self.bill_search = tk.StringVar()
        bill_entry = ttk.Entry(search_frame, textvariable=self.bill_search, width=30)
        bill_entry.pack(side=tk.LEFT, padx=5)
        bill_entry.bind('<KeyRelease>', self.search_for_bill)
        
        ttk.Button(search_frame, text="➕ Add to Bill", command=self.add_to_bill).pack(side=tk.LEFT, padx=5)
        
        
        bill_items_frame = ttk.LabelFrame(self.billing_frame, text="Bill Items", padding=10)
        bill_items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        bill_columns = ('Medicine', 'Qty', 'Rate', 'Amount')
        self.bill_tree = ttk.Treeview(bill_items_frame, columns=bill_columns, show='headings', height=8)
        for col in bill_columns:
            self.bill_tree.heading(col, text=col)
            self.bill_tree.column(col, width=150)
        self.bill_tree.pack(fill=tk.BOTH, expand=True)
        
        
        total_frame = ttk.LabelFrame(self.billing_frame, text="Billing Summary", padding=10)
        total_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.subtotal_var = tk.StringVar(value="₹0.00")
        self.tax_var = tk.StringVar(value="₹0.00")
        self.grandtotal_var = tk.StringVar(value="₹0.00")
        
        ttk.Label(total_frame, text="Subtotal:").pack(side=tk.LEFT)
        ttk.Label(total_frame, textvariable=self.subtotal_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(total_frame, text="GST (5%):").pack(side=tk.LEFT)
        ttk.Label(total_frame, textvariable=self.tax_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(total_frame, text="Grand Total:").pack(side=tk.LEFT)
        ttk.Label(total_frame, textvariable=self.grandtotal_var, font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # Bill buttons
        btn_frame = ttk.Frame(self.billing_frame)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🗑️ Clear Bill", command=self.clear_bill).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="💾 Save Bill", command=self.save_bill).pack(side=tk.RIGHT, padx=5)
        
        self.bill_items = []
        self.bill_search_results = []
    
    def search_for_bill(self, event=None):
        term = self.bill_search.get().lower()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, selling_price, quantity FROM medicines 
            WHERE name LIKE ? OR generic_name LIKE ? AND quantity > 0
        """, (f'%{term}%', f'%{term}%'))
        self.bill_search_results = cursor.fetchall()
    
    def add_to_bill(self):
        if self.bill_search_results:
            med = self.bill_search_results[0]
            med_id, name, rate, avail_qty = med
            qty_window = tk.Toplevel(self.root)
            qty_window.title("Quantity")
            qty_window.geometry("300x150")
            
            ttk.Label(qty_window, text=f"{name} - Available: {avail_qty}").pack(pady=20)
            qty_var = tk.IntVar(value=1)
            spin = ttk.Spinbox(qty_window, from_=1, to=avail_qty, textvariable=qty_var, width=10)
            spin.pack(pady=10)
            
            def add_item():
                qty = qty_var.get()
                amount = qty * rate
                self.bill_items.append({'id': med_id, 'name': name, 'qty': qty, 'rate': rate, 'amount': amount})
                self.bill_tree.insert('', tk.END, values=(name, qty, f"₹{rate}", f"₹{amount}"))
                self.update_bill_total()
                qty_window.destroy()
            
            ttk.Button(qty_window, text="Add", command=add_item).pack(pady=10)
    
    def update_bill_total(self):
        subtotal = sum(item['amount'] for item in self.bill_items)
        tax = subtotal * 0.05
        grand_total = subtotal + tax
        
        self.subtotal_var.set(f"₹{subtotal:.2f}")
        self.tax_var.set(f"₹{tax:.2f}")
        self.grandtotal_var.set(f"₹{grand_total:.2f}")
    
    def clear_bill(self):
        self.bill_items.clear()
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        self.bill_search.set('')
        self.cust_name.delete(0, tk.END)
        self.cust_phone.delete(0, tk.END)
        self.update_bill_total()
    
    def save_bill(self):
        if not self.bill_items:
            messagebox.showwarning("Warning", "No items in bill!")
            return
        
        bill_no = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        customer = self.cust_name.get() or "Walk-in Customer"
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor = self.conn.cursor()
        for item in self.bill_items:
            cursor.execute("""
                INSERT INTO sales(bill_no, medicine_id, qty_sold, total_amount, sale_date, customer_name)
                VALUES(?,?,?,?,?,?)
            """, (bill_no, item['id'], item['qty'], item['amount'], today, customer))
            
            
            cursor.execute("UPDATE medicines SET quantity = quantity - ? WHERE id = ?", 
                         (item['qty'], item['id']))
        
        self.conn.commit()
        messagebox.showinfo("Success", f"Bill {bill_no} saved!\nGrand Total: ₹{float(self.grandtotal_var.get().replace('₹','')):.2f}")
        self.clear_bill()
        self.update_dashboard()
    
    def create_reports(self):
        # Report notebook
        report_note = ttk.Notebook(self.reports_frame)
        report_note.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Low stock report
        low_frame = ttk.Frame(report_note)
        report_note.add(low_frame, text="⚠️ Low Stock")
        self.create_low_stock_report(low_frame)
        
        # Sales report
        sales_frame = ttk.Frame(report_note)
        report_note.add(sales_frame, text="💰 Sales")
        self.create_sales_report(sales_frame)
    
    def create_low_stock_report(self, parent):
        columns = ('ID', 'Name', 'Batch', 'Quantity', 'Expiry')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, batch_no, quantity, expiry_date FROM medicines WHERE quantity < 10 ORDER BY quantity")
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)
        
        ttk.Button(parent, text="Refresh", command=refresh).pack(pady=10)
        refresh()
    
    def create_sales_report(self, parent):
        columns = ('Bill No', 'Medicine', 'Qty', 'Amount', 'Date', 'Customer')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT s.bill_no, m.name, s.qty_sold, s.total_amount, s.sale_date, s.customer_name
                FROM sales s JOIN medicines m ON s.medicine_id = m.id
                ORDER BY s.sale_date DESC
            """)
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)
        
        ttk.Button(parent, text="Refresh", command=refresh).pack(pady=10)
        refresh()

def main():
    root = tk.Tk()
    app = MedicalShopSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
