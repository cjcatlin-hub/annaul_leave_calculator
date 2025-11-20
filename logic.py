from datetime import datetime
import requests

# ---------------- CONFIG ---------------- #
DEFAULT_WEEKS_ENTITLEMENT = 5
DEFAULT_WTE = 37.5
DEFAULT_LONG_SERVICE_YEARS = 5

# ---------------- BANK HOLIDAYS ---------------- #
def get_bank_holidays(year, region="england-and-wales"):
    """Fetch UK bank holidays for a given year and region."""
    try:
        url = "https://www.gov.uk/bank-holidays.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        holidays = data.get(region, {}).get("events", [])
        return sum(1 for h in holidays if datetime.strptime(h["date"], "%Y-%m-%d").year == year)
    except Exception:
        return 0  # Fallback to 0 if API fails

# ---------------- VALIDATION ---------------- #
def validate_contracted_hours(value):
    """Validate contracted hours: >0, <=40, multiple of 0.25."""
    try:
        hours = float(value)
        return hours > 0 and hours <= 40 and round(hours * 4) == hours * 4
    except ValueError:
        return False

# ---------------- HELPERS ---------------- #
def round_to_quarter_hour(hours):
    """Round hours to nearest quarter hour."""
    return round(hours * 4) / 4

# ---------------- SINGLE PERIOD CALCULATION ---------------- #
def calculate_entitlements(contracted_hours, leave_days, days_in_year, bank_holidays,
                           weeks_entitlement=DEFAULT_WEEKS_ENTITLEMENT, WTE=DEFAULT_WTE):
    """Calculate prorated entitlement for a single period."""
    base_entitlement = weeks_entitlement * WTE
    bh_entitlement = bank_holidays * 7.5
    full_time = base_entitlement + bh_entitlement

    prorated = round_to_quarter_hour((contracted_hours / WTE) * full_time * (leave_days / days_in_year))
    base = round_to_quarter_hour((contracted_hours / WTE) * base_entitlement * (leave_days / days_in_year))
    bh = round_to_quarter_hour((contracted_hours / WTE) * bh_entitlement * (leave_days / days_in_year))

    return prorated, base, bh

# ---------------- LONG SERVICE ---------------- #
def calculate_long_service(contracted_hours, years_employed, leave_days, days_in_year,
                           long_service_years=DEFAULT_LONG_SERVICE_YEARS, WTE=DEFAULT_WTE):
    """Calculate long service award based on years employed."""
    blocks = int(years_employed // long_service_years)
    if blocks == 0:
        return 0, f"⚠️ Not eligible (<{long_service_years} years)"
    award = round_to_quarter_hour((((contracted_hours / WTE) * 7.5) * blocks) * (leave_days / days_in_year))
    return award, f"Eligible: {blocks} × {long_service_years}-year block(s)"

# ---------------- MULTIPLE PERIODS ---------------- #
def calculate_multiple_periods(periods, leave_start, leave_end, bank_holidays, hire_date,
                                weeks_entitlement=DEFAULT_WEEKS_ENTITLEMENT, WTE=DEFAULT_WTE):
    """
    Calculate entitlement across multiple contract periods.
    Includes long service per contract.
    """
    base_entitlement = weeks_entitlement * WTE
    bh_entitlement = bank_holidays * 7.5
    full_time = base_entitlement + bh_entitlement

    total_prorated = 0
    total_long_service = 0
    breakdown = []

    total_days = (leave_end - leave_start).days + 1
    years_employed = (datetime.today().date() - hire_date).days / 365

    for p in periods:
        actual_start = max(p["start"], leave_start)
        actual_end = min(p["end"], leave_end)
        leave_days = (actual_end - actual_start).days + 1

        # Entitlement for this period
        prorated = round_to_quarter_hour((p["hours"] / WTE) * full_time * (leave_days / total_days))

        # Long service for this period
        long_service_award, long_service_msg = calculate_long_service(p["hours"], years_employed, leave_days, total_days)

        breakdown.append(
            f"{actual_start.strftime('%d-%m-%Y')}–{actual_end.strftime('%d-%m-%Y')}: "
            f"{prorated} hrs | Long Service: {long_service_award} hrs ({long_service_msg})"
        )

        total_prorated += prorated
        total_long_service += long_service_award

    return total_prorated, total_long_service, breakdown
