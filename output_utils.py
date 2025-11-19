import tempfile
import os
import webbrowser
from tkinter import filedialog
from fpdf import FPDF

def export_to_csv(output_box):
    content = output_box.get("1.0", "end").strip()
    if not content:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Save as CSV")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            for line in content.splitlines():
                f.write(line.replace(":", ",") + "\n")

def export_to_pdf(output_box):
    content = output_box.get("1.0", "end").strip()
    if not content:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files", "*.pdf")],
                                             title="Save as PDF")
    if file_path:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for line in content.splitlines():
            pdf.cell(0, 10, txt=line, ln=True)

        pdf.output(file_path)

def print_summary():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp_file.write(b"Annual Leave Summary\n\n")
    temp_file.close()
    webbrowser.open(temp_file.name)