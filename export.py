import csv
import os
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def export_to_csv(output_box, filename="leave_summary.csv"):
    summary = output_box.get("1.0", "end")
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for line in summary.strip().split("\n"):
                writer.writerow([line])
        messagebox.showinfo("Export Successful", f"CSV file saved as {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export CSV: {e}")

def export_to_pdf(output_box, filename="leave_summary.pdf"):
    summary = output_box.get("1.0", "end")
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        y = height - 40
        for line in summary.strip().split("\n"):
            c.drawString(40, y, line)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40
        c.save()
        messagebox.showinfo("Export Successful", f"PDF file saved as {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export PDF: {e}")

def print_summary(filename="leave_summary.pdf"):
    try:
        os.startfile(filename, "print")
        messagebox.showinfo("Print", "Sent to printer.")
    except Exception as e:
        messagebox.showerror("Print Error", f"Failed to print: {e}")