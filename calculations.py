from datetime import datetime
import requests

weeks_entitlement = 5
WTE = 37.5
long_service_years = 5

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

def round_to_quarter_hour(hours):
    return round(hours * 4) / 4

def validate_contracted_hours(value):
    try:
        hours = float(value)
        return 0 <= hours <= 40 and round(hours * 4) == hours * 4
    except ValueError:
        return False

def calculate_entitlements(contracted_hours, leave_days, days_in_year, bank_holidays):
    base_entitlement = weeks_entitlement * WTE
    bh_entitlement = bank_holidays * 7.5
    full_time = base_entitlement + bh_entitlement

    prorated = round_to_quarter_hour((contracted_hours / 37.5) * full_time * (leave_days / days_in_year))
    base = round_to_quarter_hour((contracted_hours / 37.5) * base_entitlement * (leave_days / days_in_year))
    bh = round_to_quarter_hour((contracted_hours / 37.5) * bh_entitlement * (leave_days / days_in_year))

    return prorated, base, bh

def calculate_long_service(contracted_hours, years_employed, leave_days, days_in_year):
    blocks = int(years_employed // long_service_years)
    if blocks == 0:
        return 0, f"⚠️ Not eligible for long service award (less than {long_service_years} years)"
    award = round_to_quarter_hour((((contracted_hours / WTE) * 7.5) * blocks) * (leave_days / days_in_year))
    return award, f"Eligible: {blocks} × {long_service_years}-year block(s)"
