from tkinter import messagebox
from datetime import datetime
import requests

def get_bank_holidays(year, region="england-and-wales"):
    try:
        url = "https://www.gov.uk/bank-holidays.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        holidays = data.get(region, {}).get("events", [])
        return sum(1 for h in holidays if datetime.strptime(h["date"], "%Y-%m-%d").year == year)
    except Exception:
        return "Unavailable"

def validate_contracted_hours(value):
    try:
        hours = float(value)
        return 0 <= hours <= 40 and round(hours * 4) == hours * 4
    except ValueError:
        return False

def calculate_leave(emp_entry, start_entry, end_entry, hire_entry, termination_entry,
                    termination_var, hours_entry, region_var, output_box):
    try:
        emp_number = emp_entry.get().strip()
        start_date = start_entry.get_date()
        end_date = end_entry.get_date()
        hire_date = hire_entry.get_date()
        termination_date = datetime.strptime(termination_entry.get(), "%d-%m-%Y") if termination_var.get() else end_date

        contracted_input = hours_entry.get().strip() or "37.5"
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

        days_employed = (termination_date - hire_date).days
        years_employed = days_employed / 365.25

        days_in_year = 366 if leave_year % 4 == 0 else 365
        leave_days = (end_date - start_date).days + 1

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
  Total Days in Period: {leave_days} days

Annual Leave Entitlement:
  Base Entitlement (incl. B/H): {prorated_entitlement:.2f} hours
      Basic component: {proated_base:.2f} hours
      Bank holiday component: {proated_bh:.2f} hours
  Long Service Award: {long_service_award:.2f} hours
  Total Annual Entitlement: {total_entitlement:.2f} hours

Bank Holidays in {leave_year} ({region_var.get()}): {bank_holiday_count}
============================================================
"""
        output_box.delete("1.0", "end")
        output_box.insert("end", summary)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")