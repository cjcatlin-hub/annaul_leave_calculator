import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
from tkcalendar import DateEntry

# Fetch bank holidays from GOV.UK API
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

# Validate contracted hours
def validate_contracted_hours(value):
    try:
        hours = float(value)
        if hours < 0 or hours > 40:
            return False
        if round(hours * 4) != hours * 4:  # Check 15-min increments
            return False
        return True
    except ValueError:
        return False

def calculate_leave():
    try:
        emp_number = entry_emp_number.get().strip()
        start_date = entry_start.get_date()
        end_date = entry_end.get_date()
        hire_date = entry_hire.get_date()
        termination_date = entry_termination.get_date()

        contracted_input = entry_contracted.get().strip() or "37.5"
        if not validate_contracted_hours(contracted_input):
            messagebox.showerror("Error", "Contracted hours must be between 0 and 40 in 15-minute increments (0.25 hours).")
            return

        contracted_hours = float(contracted_input)
        full_time_entitlement = float(entry_entitlement.get().strip() or 247.5)

        # Bank holidays
        leave_year = end_date.year
        region_map = {
            "England & Wales": "england-and-wales",
            "Scotland": "scotland",
            "Northern Ireland": "northern-ireland"
        }
        selected_region = region_map[region_var.get()]
        bank_holiday_count = get_bank_holidays(leave_year, selected_region)

        # Calculations
        days_worked = (end_date - start_date).days
        days_employed = (termination_date - hire_date).days
        years_employed = days_employed / 365.25

        prorated_entitlement = (contracted_hours / 37.5) * full_time_entitlement

        # Long service award
        five_year_blocks = int(years_employed // 5)
        long_service_award = ((contracted_hours / 37.5) * 7.5) * five_year_blocks
        total_entitlement = prorated_entitlement + long_service_award

        # Output summary
        summary = f"""
============================================================
                ANNUAL LEAVE CALCULATION SUMMARY
============================================================

Employee Number: {emp_number}

Employment Period:
  Hire Date: {hire_date.strftime('%d %B %Y')}
  Termination Date: {termination_date.strftime('%d %B %Y')}
  Total Days Employed: {days_employed} days ({years_employed:.2f} years)

Leave Period:
  Start Date: {start_date.strftime('%d %B %Y')}
  End Date: {end_date.strftime('%d %B %Y')}
  Total Days Worked: {days_worked} days

Annual Leave Entitlement:
  Full-Time Entitlement: {full_time_entitlement} hours/year
  Contracted Weekly Hours: {contracted_hours} hours/week
  Prorated Annual Entitlement: {prorated_entitlement:.2f} hours/year
  Long Service Award: {long_service_award:.2f} hours
  Total Annual Entitlement: {total_entitlement:.2f} hours/year

Bank Holidays in {leave_year} ({region_var.get()}): {bank_holiday_count}
============================================================
"""
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, summary)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# GUI setup
root = tk.Tk()
root.title("Annual Leave Calculator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Input fields
ttk.Label(frame, text="Employee Number").grid(row=0, column=0, sticky="w")
entry_emp_number = ttk.Entry(frame, width=30)
entry_emp_number.grid(row=0, column=1)

ttk.Label(frame, text="Employment Start Date").grid(row=1, column=0, sticky="w")
entry_start = DateEntry(frame, width=27, date_pattern="yyyy-mm-dd")
entry_start.grid(row=1, column=1)

ttk.Label(frame, text="Employment End Date").grid(row=2, column=0, sticky="w")
entry_end = DateEntry(frame, width=27, date_pattern="yyyy-mm-dd")
entry_end.grid(row=2, column=1)

ttk.Label(frame, text="Hire Date").grid(row=3, column=0, sticky="w")
entry_hire = DateEntry(frame, width=27, date_pattern="yyyy-mm-dd")
entry_hire.grid(row=3, column=1)

ttk.Label(frame, text="Termination Date").grid(row=4, column=0, sticky="w")
entry_termination = DateEntry(frame, width=27, date_pattern="yyyy-mm-dd")
entry_termination.grid(row=4, column=1)

ttk.Label(frame, text="Contracted Weekly Hours (0-40, 15-min increments)").grid(row=5, column=0, sticky="w")
entry_contracted = ttk.Entry(frame, width=30)
entry_contracted.grid(row=5, column=1)

ttk.Label(frame, text="Full-Time Entitlement (default 247.5)").grid(row=6, column=0, sticky="w")
entry_entitlement = ttk.Entry(frame, width=30)
entry_entitlement.grid(row=6, column=1)

# Region dropdown
ttk.Label(frame, text="Bank Holiday Region").grid(row=7, column=0, sticky="w")
region_var = tk.StringVar(value="England & Wales")
region_dropdown = ttk.Combobox(frame, textvariable=region_var, values=["England & Wales", "Scotland", "Northern Ireland"], state="readonly", width=27)
region_dropdown.grid(row=7, column=1)

# Calculate button
ttk.Button(frame, text="Calculate Leave", command=calculate_leave).grid(row=8, column=0, columnspan=2, pady=10)

# Output box
text_output = tk.Text(root, wrap="word", height=20, width=80)
text_output.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
