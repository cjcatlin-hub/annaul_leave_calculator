def format_summary(emp_number, hire_date, contracted_hours, days_employed, years_employed,
                   bank_holiday_count, leave_year, region, start_date, end_date, leave_days,
                   prorated_entitlement, prorated_base, prorated_bh,
                   long_service_award, long_service_note, total_entitlement):
    return f"""\
================== ANNUAL LEAVE SUMMARY ==================

👤 Employee: {emp_number}
📅 Hire Date: {hire_date.strftime('%d %b %Y')}
🕒 Contracted Hours: {contracted_hours} hrs/week
📈 Continuous Service: {days_employed} days ({years_employed:.2f} yrs)
🏖️ Bank Holidays in {leave_year} ({region}): {bank_holiday_count}

📆 Leave Period: {start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')} ({leave_days} days)

------------------ OPTIMA UPLOAD ------------------
Entitlement Basis : Annual Rate
Entitlement Type  : Annual Leave
Units             : Hours Only
Period Start      : January

Base Hours        : {prorated_entitlement:.2f}
Long Service Hrs  : {long_service_award:.2f}
Carry Forward     : 0
Lieu Hours        : 0
Adjusted Hours    : 0
Total Hours       : {total_entitlement:.2f}

------------------ BREAKDOWN ------------------
Total Entitlement : {total_entitlement:.2f}
  ├─ Basic        : {prorated_entitlement:.2f}
  │   ├─ Base     : {prorated_base:.2f}
  │   └─ Bank Hol : {prorated_bh:.2f}
  └─ Long Service : {long_service_award:.2f} - {long_service_note}

📝 All values rounded to the nearest 15 minutes
==================================================
"""