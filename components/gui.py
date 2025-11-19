import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from logic import calculate_leave
from export import export_to_csv, export_to_pdf, print_summary

def build_gui():
    root = tk.Tk()
    root.title("Annual Leave Calculator")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky="nsew")

    today = datetime.today()
    default_start = datetime(today.year, 1, 1)
    default_end = datetime(today.year, 12, 31)

    # Widgets
    ttk.Label(frame, text="Employee Number").grid(row=0, column=0, sticky="w")
    emp_entry = ttk.Entry(frame, width=30)
    emp_entry.grid(row=0, column=1)

    ttk.Label(frame, text="Leave Period Start Date").grid(row=1, column=0, sticky="w")
    start_entry = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_start.year, month=default_start.month, day=default_start.day)
    start_entry.grid(row=1, column=1)

    ttk.Label(frame, text="Leave Period End Date").grid(row=2, column=0, sticky="w")
    end_entry = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", year=default_end.year, month=default_end.month, day=default_end.day)
    end_entry.grid(row=2, column=1)

    ttk.Label(frame, text="Hire Date").grid(row=3, column=0, sticky="w")
    hire_entry = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy")
    hire_entry.grid(row=3, column=1)

    ttk.Label(frame, text="Termination Date").grid(row=4, column=0, sticky="w")
    termination_entry = DateEntry(frame, width=27, date_pattern="dd-mm-yyyy", state="disabled")
    termination_entry.grid(row=4, column=1)

    termination_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="Include Termination Date", variable=termination_var,
                    command=lambda: termination_entry.config(state="normal" if termination_var.get() else "disabled")).grid(row=4, column=2)

    ttk.Label(frame, text="Contracted Weekly Hours").grid(row=5, column=0, sticky="w")
    hours_entry = ttk.Entry(frame, width=30)
    hours_entry.grid(row=5, column=1)

    ttk.Label(frame, text="Bank Holiday Region").grid(row=7, column=0, sticky="w")
    region_var = tk.StringVar(value="England & Wales")
    region_dropdown = ttk.Combobox(frame, textvariable=region_var,
                                   values=["England & Wales", "Scotland", "Northern Ireland"],
                                   state="readonly", width=27)
    region_dropdown.grid(row=7, column=1)

    output_box = tk.Text(root, wrap="word", height=100, width=100)
    output_box.grid(row=1, column=0, padx=10, pady=10)

    # Buttons
    ttk.Button(frame, text="Calculate Leave", command=lambda: calculate_leave(
        emp_entry, start_entry, end_entry, hire_entry, termination_entry,
        termination_var, hours_entry, region_var, output_box
    )).grid(row=8, column=0, columnspan=2, pady=10)

    ttk.Button(frame, text="Export to CSV", command=lambda: export_to_csv(output_box)).grid(row=9, column=0)
    ttk.Button(frame, text="Export to PDF", command=lambda: export_to_pdf(output_box)).grid(row=9, column=1)
    ttk.Button(frame, text="Print Summary", command=lambda: print_summary()).grid(row=9, column=2)

    root.mainloop()