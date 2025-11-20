# Annual Leave Calculator 🏖️ 💼 📅
## With GUI as portable app

###### A simple, user-friendly Python application for calculating annual leave entitlements based on employment dates, contracted hours, and long service awards. Built with Tkinter for a clean and portable desktop experience.

---

## ✨ Features

- Calculates prorated annual leave based on contracted weekly hours (37.5 = full-time)
- Automatically adds a **7.5-hour long service award** on the 5th anniversary and every 5th year thereafter (prorated)
- Defaults termination date to **31 December** of the leave year if left blank
- Clean, scrollable summary output
- Internet connection required after packaging to fetch bank holidays from GOV API

---

## 🖥️ Requirements

- Python 3.7 or later
- pyinstaller

---

## 🚀 How to Run

### Run from Python

1. Clone or download this repository
2. Open a terminal in the project folder
3. Run the app:
   `python main.py`

### Build standalone Windows App
1. Install PyInstaller:
2. Build .exe <br>
   `pyinstaller --onefile --windowed main.py`

### Input Fields
-`Employee Number`: employee number <br>
-`Leave period Start/End`: used to calcaulte entitlemt for the period <br>
-`Hire Date`: Original employee hire date - used to calcualte long service award <br>
-`Contracted Weekly Hours`: Defaults to 37.5 - scheduled weekly hours <br>
-`Full-Time Entitlement`: Defualts to 247.5 hours per year <br>



### 📄 Output
A detailed summary of:
- Employment and leave periods
- Prorated annual leave entitlement
- Long service award (if applicable)
- Total annual leave entitlement

### 🛠️ Todo
- **Add full long service entitlement (+7.5 hours every 5 years) - done**
- **Export summary to PDF or CSV - done**
- **Add GUI theming or dark mode - done**
- Batch processing for multiple employees
- Batch processing for contract hours changes
- **Get bank holidays from .gov API - done**
- **Change output to match Optima input - done**
- **Limit contract hours to 0 - 40 in 0.25 increments - done**
- **Proata entitlements for number of days between start_date and end_Date - done**
- ** Make code modular - done**

### 🙌 Author <br>
Created by Chris Catlin <br>
Adapted from jessicastow/annual_leave_calculator
