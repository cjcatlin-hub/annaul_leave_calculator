import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from datetime import datetime
from logic import calculate_leave
from output_utils import export_to_csv, export_to_pdf, print_summary


def build_gui():
    root = tb.Window(themename="flatly")
    root.title("Annual Leave Calculator")
    root.state("zoomed")  # Start maximized

    today = datetime.today()

    # Theme switcher logic
    def set_theme(theme_name):
        root.style.theme_use(theme_name)

    # Menu bar with theme toggle
    menubar = tb.Menu(root)
    theme_menu = tb.Menu(menubar, tearoff=0)
    theme_menu.add_command(label="Light", command=lambda: set_theme("flatly"))
    theme_menu.add_command(label="Dark", command=lambda: set_theme("darkly"))
    menubar.add_cascade(label="Theme", menu=theme_menu)
    root.config(menu=menubar)

    # Header
    tb.Label(root, text="🗓️ Annual Leave Calculator", font=("Segoe UI", 20, "bold"), bootstyle="primary").pack(pady=(20, 5))
    tb.Label(root, text="Calculate prorated leave and long service awards with ease", font=("Segoe UI", 11)).pack(pady=(0, 15))

    # Main horizontal container
    main_frame = tb.Frame(root)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Left: Input section
    input_frame = tb.Frame(main_frame)
    input_frame.pack(side=LEFT, fill=Y, expand=False, padx=(0, 10))

    # Right: Output section
    output_frame = tb.Frame(main_frame)
    output_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Employee Info
    emp_frame = tb.Labelframe(input_frame, text="👤 Employee Information", padding=15, bootstyle="info")
    emp_frame.pack(fill=X, pady=10)
    tb.Label(emp_frame, text="Employee Number").pack(anchor=W)
    emp_entry = tb.Entry(emp_frame, width=30, bootstyle="info")
    emp_entry.pack(pady=5)
    tb.Label(emp_frame, text="Hire Date").pack(anchor=W)
    hire_entry = DateEntry(emp_frame, width=27, bootstyle="info")
    hire_entry.pack(pady=5)

    # Leave Period
    leave_frame = tb.Labelframe(input_frame, text="📆 Leave Period", padding=15, bootstyle="info")
    leave_frame.pack(fill=X, pady=10)
    tb.Label(leave_frame, text="Start Date").pack(anchor=W)
    start_entry = DateEntry(leave_frame, width=27, bootstyle="info")
    start_entry.pack(pady=5)
    start_entry.set_date(datetime(today.year, 1, 1))
    tb.Label(leave_frame, text="End Date").pack(anchor=W)
    end_entry = DateEntry(leave_frame, width=27, bootstyle="info")
    end_entry.pack(pady=5)
    end_entry.set_date(datetime(today.year, 12, 31))

    # Contract Info
    contract_frame = tb.Labelframe(input_frame, text="📄 Contract Details", padding=15, bootstyle="info")
    contract_frame.pack(fill=X, pady=10)
    tb.Label(contract_frame, text="Contracted Weekly Hours").pack(anchor=W)
    hours_entry = tb.Entry(contract_frame, width=30, bootstyle="info")
    hours_entry.pack(pady=5)
    tb.Label(contract_frame, text="Bank Holiday Region").pack(anchor=W)
    region_var = tb.StringVar(value="England & Wales")
    region_dropdown = tb.Combobox(contract_frame, textvariable=region_var,
                                  values=["England & Wales", "Scotland", "Northern Ireland"],
                                  state="readonly", width=27, bootstyle="info")
    region_dropdown.pack(pady=5)

    # Output Box (must be defined before buttons use it)
    output_box = tb.Text(output_frame, wrap="word", font=("Consolas", 10))
    output_box.pack(fill=BOTH, expand=True)


    # Buttons
    button_frame = tb.Frame(input_frame)
    button_frame.pack(pady=20)
    tb.Button(button_frame, text="🧮 Calculate", bootstyle=PRIMARY,
              command=lambda: calculate_leave(emp_entry, start_entry, end_entry, hire_entry,
                                              hours_entry, region_var, output_box)).grid(row=0, column=0, padx=10)
    tb.Button(button_frame, text="📤 Export CSV", bootstyle=INFO,
              command=lambda: export_to_csv(output_box)).grid(row=0, column=1, padx=10)
    tb.Button(button_frame, text="📝 Export PDF", bootstyle=SUCCESS,
              command=lambda: export_to_pdf(output_box)).grid(row=1, column=0, padx=10, pady=5)
    tb.Button(button_frame, text="🖨️ Print", bootstyle=SECONDARY,
              command=lambda: print_summary()).grid(row=1, column=1, padx=10, pady=5)
    
    root.mainloop()