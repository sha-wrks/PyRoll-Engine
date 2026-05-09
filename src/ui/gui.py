import tkinter as tk
from tkinter import messagebox, ttk
from ..database.database import Database
from ..engine.payroll import PayrollCalculator

class PyRollEngine:
    def __init__(self):
        self.db = Database()
        self.calc = PayrollCalculator()
        self.root = tk.Tk()
        self.root.title("PyRoll Engine - Payroll Calculator")
        self.root.geometry("500x650")
        self.root.configure(bg="#f0f0f0")
        
        # UI Frames
        self.frame_input = ttk.Frame(self.root, padding=10)
        self.frame_input.pack(fill="x")
        
        self.frame_buttons = ttk.Frame(self.root, padding=10)
        self.frame_buttons.pack(fill="x")
        
        self.frame_results = ttk.Frame(self.root, padding=10)
        self.frame_results.pack(fill="both", expand=True)
        
        # Title
        self.label_title = tk.Label(self.frame_input, text="PyRoll Engine", font=("Arial", 18, "bold"), bg="#f0f0f0")
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Inputs
        tk.Label(self.frame_input, text="Employee Name:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_name = tk.Entry(self.frame_input)
        self.entry_name.grid(row=1, column=1)
        
        tk.Label(self.frame_input, text="Hours Worked:", bg="#f0f0f0").grid(row=2, column=0, sticky="w")
        self.entry_hours = tk.Entry(self.frame_input)
        self.entry_hours.grid(row=2, column=1)
        
        tk.Label(self.frame_input, text="Hourly Rate:", bg="#f0f0f0").grid(row=3, column=0, sticky="w")
        self.entry_rate = tk.Entry(self.frame_input)
        self.entry_rate.grid(row=3, column=1)
        
        tk.Label(self.frame_input, text="Deductions:", bg="#f0f0f0").grid(row=4, column=0, sticky="w")
        self.entry_deductions = tk.Entry(self.frame_input)
        self.entry_deductions.grid(row=4, column=1)
        
        tk.Label(self.frame_input, text="Tax Rate (%):", bg="#f0f0f0").grid(row=5, column=0, sticky="w")
        self.entry_tax_rate = tk.Entry(self.frame_input)
        self.entry_tax_rate.grid(row=5, column=1)
        
        tk.Label(self.frame_input, text="Bonus:", bg="#f0f0f0").grid(row=6, column=0, sticky="w")
        self.entry_bonus = tk.Entry(self.frame_input)
        self.entry_bonus.grid(row=6, column=1)
        
        # Buttons
        self.button_calculate = tk.Button(self.frame_buttons, text="Calculate Salary", command=self.calculate_salary, bg="#4CAF50", fg="white")
        self.button_calculate.pack(side="left", padx=5)
        
        self.button_save = tk.Button(self.frame_buttons, text="Save Employee", command=self.save_employee, bg="#2196F3", fg="white")
        self.button_save.pack(side="left", padx=5)
        
        self.button_view = tk.Button(self.frame_buttons, text="View All Employees", command=self.view_employees, bg="#FF9800", fg="white")
        self.button_view.pack(side="left", padx=5)
        
        # Results
        self.text_results = tk.Text(self.frame_results, height=15, width=50, bg="#ffffff")
        self.text_results.pack(fill="both", expand=True)
    
    def calculate_salary(self):
        try:
            name = self.entry_name.get()
            hours = float(self.entry_hours.get())
            rate = float(self.entry_rate.get())
            deductions = float(self.entry_deductions.get())
            tax_rate = float(self.entry_tax_rate.get())
            bonus = float(self.entry_bonus.get())
            
            gross, tax, net = self.calc.calculate_salary(hours, rate, deductions, tax_rate, bonus)
            result = f"Employee: {name}\nGross Salary: ${gross:.2f}\nTax: ${tax:.2f}\nDeductions: ${deductions:.2f}\nBonus: ${bonus:.2f}\nNet Salary: ${net:.2f}"
            self.text_results.delete(1.0, tk.END)
            self.text_results.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
    
    def save_employee(self):
        try:
            name = self.entry_name.get()
            hours = float(self.entry_hours.get())
            rate = float(self.entry_rate.get())
            deductions = float(self.entry_deductions.get())
            tax_rate = float(self.entry_tax_rate.get())
            bonus = float(self.entry_bonus.get())
            
            gross, tax, net = self.calc.calculate_salary(hours, rate, deductions, tax_rate, bonus)
            employee = {"name": name, "hours": hours, "rate": rate, "deductions": deductions, "tax_rate": tax_rate, "bonus": bonus, "net_salary": net}
            self.db.save_employee(employee)
            messagebox.showinfo("Success", "Employee saved!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")
    
    def view_employees(self):
        employees = self.db.get_all_employees()
        if not employees:
            self.text_results.delete(1.0, tk.END)
            self.text_results.insert(tk.END, "No employees saved.")
            return
        
        result = "Saved Employees:\n"
        for emp in employees:
            result += f"Name: {emp['name']}, Net Salary: ${emp['net_salary']:.2f}\n"
        self.text_results.delete(1.0, tk.END)
        self.text_results.insert(tk.END, result)
    
    def run(self):
        self.root.mainloop()
