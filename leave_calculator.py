import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def calculate_leave():
    try:
        # Get inputs
        emp_number = entry_emp_number.get().strip()
        start_date = datetime.strptime(entry_start.get().strip(), "%Y-%m-%d")
        end_date = datetime.strptime(entry_end.get().strip(), "%Y-%m-%d")
        hire_date = datetime.strptime(entry_hire.get().strip(), "%Y-%m-%d")
        termination_input = entry_termination.get().strip()
          if termination_input:
              termination_date = datetime.strptime(termination_input, "%Y-%m-%d")
          else:
              # Default to end of leave year
              end_date = datetime.strptime(entry_end.get().strip(), "%Y-%m-%d")
        termination_date = datetime(end_date.year, 12, 31)
        contracted_hours = float(entry_contracted.get().strip() or 37.5)
        full_time_entitlement = float(entry_entitlement.get().strip() or 247.5)

        # Calculations
        days_worked = (end_date - start_date).days
        weeks_worked = days_worked / 7
        days_employed = (termination_date - hire_date).days
        years_employed = days_employed / 365.25

        prorated_entitlement = (contracted_hours / 37.5) * full_time_entitlement
        long_service_award = (contracted_hours / 37.5) * 7.5 if days_employed >= 5 * 365 else 0
        total_entitlement = prorated_entitlement + long_service_award

        # Output
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
fields = [
    ("Employee Number", "emp_number"),
    ("Employment Start Date (yyyy-mm-dd)", "start"),
    ("Employment End Date (yyyy-mm-dd)", "end"),
    ("Hire Date (yyyy-mm-dd)", "hire"),
    ("Termination Date (yyyy-mm-dd)", "termination"),
    ("Contracted Weekly Hours (default 37.5)", "contracted"),
    ("Full-Time Entitlement (default 247.5)", "entitlement")
]

entries = {}
for i, (label, key) in enumerate(fields):
    ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w")
    entry = ttk.Entry(frame, width=30)
    entry.grid(row=i, column=1)
    entries[key] = entry

entry_emp_number = entries["emp_number"]
entry_start = entries["start"]
entry_end = entries["end"]
entry_hire = entries["hire"]
entry_termination = entries["termination"]
entry_contracted = entries["contracted"]
entry_entitlement = entries["entitlement"]

# Calculate button
ttk.Button(frame, text="Calculate Leave", command=calculate_leave).grid(row=len(fields), column=0, columnspan=2, pady=10)

# Output box
text_output = tk.Text(root, wrap="word", height=20, width=80)
text_output.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
