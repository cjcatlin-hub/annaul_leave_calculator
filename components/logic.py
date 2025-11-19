from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
from calculations import (
    get_bank_holidays,
    round_to_quarter_hour,
    validate_contracted_hours,
    calculate_entitlements,
    calculate_long_service
)
from formatting import format_summary

def calculate_leave(emp_entry, start_entry, end_entry, hire_entry,
                    hours_entry, region_var, output_box):
    try:
        emp_number = emp_entry.get().strip()
        start_date = start_entry.get_date()
        end_date = end_entry.get_date()
        hire_date = hire_entry.get_date()

        contracted_input = hours_entry.get().strip() or "37.5"
        if not validate_contracted_hours(contracted_input):
            Messagebox.show_error("Contracted hours must be between 0 and 40 in 15-minute increments.")
            return
        contracted_hours = float(contracted_input)

        leave_year = end_date.year
        region_map = {
            "England & Wales": "england-and-wales",
            "Scotland": "scotland",
            "Northern Ireland": "northern-ireland"
        }
        selected_region = region_map.get(region_var.get(), "england-and-wales")
        bank_holiday_count = get_bank_holidays(leave_year, selected_region)

        days_employed = (end_date - hire_date).days
        years_employed = days_employed / 365.25
        days_in_year = 366 if (leave_year % 4 == 0 and (leave_year % 100 != 0 or leave_year % 400 == 0)) else 365
        leave_days = (end_date - start_date).days + 1

        prorated_entitlement, prorated_base, prorated_bh = calculate_entitlements(
            contracted_hours, leave_days, days_in_year, bank_holiday_count
        )
        long_service_award, long_service_note = calculate_long_service(
            contracted_hours, years_employed, leave_days, days_in_year
        )
        total_entitlement = prorated_entitlement + long_service_award

        summary = format_summary(
            emp_number, hire_date, contracted_hours, days_employed, years_employed,
            bank_holiday_count, leave_year, region_var.get(), start_date, end_date, leave_days,
            prorated_entitlement, prorated_base, prorated_bh,
            long_service_award, long_service_note, total_entitlement
        )

        output_box.delete("1.0", "end")
        output_box.insert("end", summary)

    except Exception as e:
        Messagebox.show_error(f"Invalid input: {e}")