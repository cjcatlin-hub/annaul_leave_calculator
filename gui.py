import webbrowser
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from ttkbootstrap.dialogs import Messagebox
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

    # Menu bar
    menubar = tb.Menu(root)

    # Theme menu
    theme_menu = tb.Menu(menubar, tearoff=0)
    theme_menu.add_command(label="Light", command=lambda: set_theme("flatly"))
    theme_menu.add_command(label="Dark", command=lambda: set_theme("darkly"))
    menubar.add_cascade(label="Theme", menu=theme_menu)

    # About menu
    about_menu = tb.Menu(menubar, tearoff=0)

    def show_about():
        about_text = (
        "Annual Leave Calculator\n"
        "Version: 0.1\n\n"
        "Author: Christopher Catlin\n"
        "License: GNU General Public License v3.0\n\n"
        "Source Code:\nClick 'Open GitHub' below."
    )
    # Show info box
        Messagebox.show_info(title="About", message=about_text)

    def open_github():
        webbrowser.open("https://github.com/cjcatlin-hub/annaul_leave_calculator")

    about_menu.add_command(label="About", command=show_about)
    about_menu.add_command(label="GitHub Repo", command=open_github)
    menubar.add_cascade(label="About", menu=about_menu)

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
    hire_entry = DateEntry(emp_frame, width=27, bootstyle="info", dateformat="%d-%m-%Y")
    hire_entry.pack(pady=5)

    # Leave Period
    leave_frame = tb.Labelframe(input_frame, text="📆 Leave Period", padding=15, bootstyle="info")
    leave_frame.pack(fill=X, pady=10)
    tb.Label(leave_frame, text="Start Date").pack(anchor=W)
    start_entry = DateEntry(leave_frame, width=27, bootstyle="info", dateformat="%d-%m-%Y")
    start_entry.pack(pady=5)
    start_entry.set_date(datetime(today.year, 1, 1))
    tb.Label(leave_frame, text="End Date").pack(anchor=W)
    end_entry = DateEntry(leave_frame, width=27, bootstyle="info", dateformat="%d-%m-%Y")
    end_entry.pack(pady=5)
    end_entry.set_date(datetime(today.year, 12, 31))

    # Contracts
    contract_frame = tb.Labelframe(input_frame, text="📄 Contract Details", padding=15, bootstyle="info")
    contract_frame.pack(fill=X, expand=True, pady=10)

    canvas = tb.Canvas(contract_frame, width=550)
    scroll_y = tb.Scrollbar(contract_frame, orient="vertical", command=canvas.yview)
    periods_frame = tb.Frame(canvas)
    periods_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=periods_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scroll_y.pack(side=RIGHT, fill=Y)

    periods = []

    def add_period():
        frame = tb.Frame(periods_frame)
        frame.pack(fill=X, pady=3)

        # Default start date logic
        if periods:
            prev_end = periods[-1]["end"].get_date()
            default_start = prev_end + timedelta(days=1)
        else:
            default_start = start_entry.get_date()

        default_end = end_entry.get_date()

        start = DateEntry(frame, width=10, dateformat="%d-%m-%Y")
        start.set_date(default_start)
        start.grid(row=0, column=0, padx=3)

        end = DateEntry(frame, width=10, dateformat="%d-%m-%Y")
        end.set_date(default_end)
        end.grid(row=0, column=1, padx=3)

        hours = tb.Entry(frame, width=6)
        hours.grid(row=0, column=2, padx=3)

        tb.Label(frame, text="Start").grid(row=1, column=0)
        tb.Label(frame, text="End").grid(row=1, column=1)
        tb.Label(frame, text="Hours").grid(row=1, column=2)

        def delete_period():
            periods.remove(period_dict)
            frame.destroy()

        delete_btn = tb.Button(frame, text="❌", bootstyle=DANGER, width=4, command=delete_period)
        delete_btn.grid(row=0, column=3, padx=5)

        period_dict = {"start": start, "end": end, "hours": hours}
        periods.append(period_dict)

    tb.Button(contract_frame, text="➕ Add Contract Change", bootstyle=INFO, command=add_period).pack(pady=5)

    # Output Box
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
