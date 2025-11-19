import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests, csv, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# Get current year bounds
today = datetime.today()
default_start = datetime(today.year, 1, 1)
default_end = datetime(today.year, 12, 31)

# GUI setup
root = tk.Tk()
root.title("Annual Leave Calculator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Theme setup
style = ttk.Style()
style.theme_use("clam")

# Input fields
ttk.Label(frame, text="Employee Number").grid(row=0, column=0, sticky="w")
entry_emp_number = ttk.Entry(frame, width=30)
entry_emp_number.grid(row=0, column=1)

ttk.Label(frame, text="Leave Period Start Date").grid(row=1, column=0, sticky="w")
entry_start = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_start.year, month=default_start.month, day=default_start.day)
entry_start.grid(row=1, column=1)

ttk.Label(frame, text="Leave Period End Date").grid(row=2, column=0, sticky="w")
entry_end = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_end.year, month=default_end.month, day=default_end.day)
entry_end.grid(row=2, column=1)

ttk.Label(frame, text="Hire Date").grid(row=3, column=0, sticky="w")
entry_hire = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy")
entry_hire.grid(row=3, column=1)

ttk.Label(frame, text="Termination Date").grid(row=4, column=0, sticky="w")
entry_termination = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", state="disabled")
entry_termination.grid(row=4, column=1)

termination_var = tk.BooleanVar(value=False)
ttk.Checkbutton(frame, text="Include Termination Date", variable=termination_var, command=lambda: entry_termination.config(state="normal" if termination_var.get() else "disabled")).grid(row=4, column=2, padx=5)

ttk.Label(frame, text="Contracted Weekly Hours (0-40, 15-min increments)").grid(row=5, column=0, sticky="w")
entry_contracted = ttk.Entry(frame, width=30)
entry_contracted.grid(row=5, column=1)

ttk.Label(frame, text="Full-Time Entitlement (default 247.5)").grid(row=6, column=0, sticky="w")
entry_entitlement = ttk.Entry(frame, width=30)
entry_entitlement.grid(row=6, column=1)

ttk.Label(frame, text="Bank Holiday Region").grid(row=7, column=0, sticky="w")
region_var = tk.StringVar(value="England & Wales")
region_dropdown = ttk.Combobox(frame, textvariable=region_var, values=["England & Wales", "Scotland", "Northern Ireland"], state="readonly", width=27)
region_dropdown.grid(row=7, column=1)

ttk.Button(frame, text="Calculate Leave", command=lambda: calculate_leave()).grid(row=8, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="Export to CSV", command=lambda: export_to_csv()).grid(row=9, column=0, pady=5)
ttk.Button(frame, text="Export to PDF", command=lambda: export_to_pdf()).grid(row=9, column=1, pady=5)
ttk.Button(frame, text="Print Summary", command=lambda: print_summary()).grid(row=9, column=2, pady=5)


text_output = tk.Text(root, wrap="word", height=20, width=100)
text_output.grid(row=1, column=0, padx=10, pady=10)

apply_theme("light")

# Functional logic
def get_bank_holidays(year, region="england-and-wales"):
    try:
        url = "https://www.gov.uk/bank-holidays.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        holidays = data.get(region, {}).get("events", [])
        count = sum(1 for h in holidays if datetime.strptime(h["date"], "%Y-%m-%d").year == year)
        return count
    except Exception:
        return "Unavailable"

def validate_contracted_hours(value):
    try:
        hours = float(value)
        return 0 <= hours <= 40 and round(hours * 4) == hours * 4
    except ValueError:
        return False

def calculate_leave():
    try:
        emp_number = entry_emp_number.get().strip()
        start_date = entry_start.get_date()
        end_date = entry_end.get_date()
        hire_date = entry_hire.get_date()
        termination_date = datetime.strptime(entry_termination.get(), "%d-%m-%Y") if termination_var.get() else end_date

        contracted_input = entry_contracted.get().strip() or "37.5"
        if not validate_contracted_hours(contracted_input):
            messagebox.showerror("Error", "Contracted hours must be between 0 and 40 in 15-minute increments.")
            return
        contracted_hours = float(contracted_input)

        leave_year = end_date.year
        region_map = {
            "England & Wales": "england-and-wales",
            "Scotland": "scotland",
            "Northern Ireland": "northern-ireland"
        }
        selected_region = region_map[region_var.get()]
        bank_holiday_count = get_bank_holidays(leave_year, selected_region)

        entitlement = 5.0 * 37.5
        bh_entitlement = bank_holiday_count * 7.5
        full_time_entitlement = entitlement + bh_entitlement

        days_worked = (end_date - start_date).days
        days_employed = (termination_date - hire_date).days
        years_employed = days_employed / 365.25

        days_in_year = 366 if leave_year % 4 == 0 else 365
        leave_days = (end_date - start_date).days + 1  # inclusive

        prorated_entitlement = (contracted_hours / 37.5) * full_time_entitlement * (leave_days / days_in_year)
        proated_base = (contracted_hours / 37.5) * entitlement * (leave_days / days_in_year)
        proated_bh = (contracted_hours / 37.5) * bh_entitlement * (leave_days / days_in_year)

        five_year_blocks = int(years_employed // 5)
        long_service_award = (((contracted_hours / 37.5) * 7.5) * five_year_blocks) * (leave_days / days_in_year)
        total_entitlement = prorated_entitlement + long_service_award

        summary = f"""
============================================================
                ANNUAL LEAVE CALCULATION SUMMARY
============================================================

Employee Number: {emp_number}

Employment Period:
  Hire Date: {hire_date.strftime('%d %B %Y')}
  Termination Date: {termination_date.strftime('%d %B %Y')}
  Contracted Weekly Hours: {contracted_hours} hours/week
  Total Days Employed: {days_employed} days ({years_employed:.2f} years)

Leave Period:
  Start Date: {start_date.strftime('%d %B %Y')}
  End Date: {end_date.strftime('%d %B %Y')}
  Total Days Worked: {days_worked} days

Annual Leave Entitlement:
  Base Entitlement (including B/H): {prorated_entitlement:.2f} hours
      Basic component: {proated_base:.2f} hours
      Bank holiday component: {proated_bh:.2f} hours
  Long Service Award: {long_service_award:.2f} hours
  Total Annual Entitlement: {total_entitlement:.2f} hours

Bank Holidays in {leave_year} ({region_var.get()}): {bank_holiday_count}
============================================================
"""
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, summary)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Export to CSV
def export_to_csv():
    summary = text_output.get("1.0", tk.END)
    try:
        with open("leave_summary.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for line in summary.strip().split("\n"):
                writer.writerow([line])
        messagebox.showinfo("Export Successful", "CSV file saved as leave_summary.csv")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export CSV: {e}")

# Export to PDF
def export_to_pdf():
    summary = text_output.get("1.0", tk.END)
    try:
        c = canvas.Canvas("leave_summary.pdf", pagesize=A4)
        width, height = A4
        y = height - 40
        for line in summary.strip().split("\n"):
            c.drawString(40, y, line)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40
        c.save()
        messagebox.showinfo("Export Successful", "PDF file saved as leave_summary.pdf")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export PDF: {e}")

# Print PDF
def print_summary():
    try:
        os.startfile("leave_summary.pdf", "print")
        messagebox.showinfo("Print", "Sent to printer.")
    except Exception as e:
        messagebox.showerror("Print Error", f"Failed to print: {e}")

# Toggle termination field
def toggle_termination():
    if termination_var.get():
        entry_termination.config(state="normal")
    else:
        entry_termination.config(state="disabled")

# GUI setup
root = tk.Tk()
root.title("Annual Leave Calculator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Input fields
ttk.Label(frame, text="Employee Number").grid(row=0, column=0, sticky="w")
entry_emp_number = ttk.Entry(frame, width=30)
entry_emp_number.grid(row=0, column=1)

ttk.Label(frame, text="Leave Period Start Date").grid(row=1, column=0, sticky="w")
entry_start = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_start.year, month=default_start.month, day=default_start.day)
entry_start.grid(row=1, column=1)

ttk.Label(frame, text="Leave Period End Date").grid(row=2, column=0, sticky="w")
entry_end = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_end.year, month=default_end.month, day=default_end.day)
entry_end.grid(row=2, column=1)

ttk.Label(frame, text="Hire Date").grid(row=3, column=0, sticky="w")
entry_hire = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy")
entry_hire.grid(row=3, column=1)

ttk.Label(frame, text="Termination Date").grid(row=4, column=0, sticky="w")
entry_termination = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", state="disabled")
entry_termination.grid(row=4, column=1)

termination_var = tk.BooleanVar(value=False)
ttk.Checkbutton(frame, text="Include Termination Date", variable=termination_var, command=toggle_termination).grid(row=4, column=2, padx=5)

ttk.Label(frame, text="Contracted Weekly Hours (0-40, 15-min increments)").grid(row=5, column=0, sticky="w")
entry_contracted = ttk.Entry(frame, width=30)
entry_contracted.grid(row=5, column=1)

ttk.Label(frame, text="Full-Time Entitlement (default 247.5)").grid(row=6, column=0, sticky="w")
entry_entitlement = ttk.Entry(frame, width=30)
entry_entitlement.grid(row=6, column=1)

# Region dropdown
ttk.Label(frame, text="Bank Holiday Region").grid(row=7, column=0, sticky="w")
region_var = tk.StringVar(value="England & Wales")
region_dropdown = ttk.Combobox(
    frame,
    textvariable=region_var,
    values=["England & Wales", "Scotland", "Northern Ireland"],
    state="readonly",
    width=27
)
region_dropdown.grid(row=7, column=1)

# Calculate button
ttk.Button(frame, text="Calculate Leave", command=calculate_leave).grid(row=8, column=0, columnspan=2, pady=10)

# Export and print buttons
ttk.Button(frame, text="Export to CSV", command=export_to_csv).grid(row=9, column=0, pady=5)
ttk.Button(frame, text="Export to PDF", command=export_to_pdf).grid(row=9, column=1, pady=5)
ttk.Button(frame, text="Print Summary", command=print_summary).grid(row=9, column=2, pady=5)

# Output box
text_output = tk.Text(root, wrap="word", height=100, width=100)
text_output.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()