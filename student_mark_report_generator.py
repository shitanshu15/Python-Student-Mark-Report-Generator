import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# ✅ Ensure output directory exists
os.makedirs("output", exist_ok=True)

# ✅ New student data
students_data = {
    "Name": [
        "Raman Sharma", "Rohit Mehta", "Aman Saha", "Rekha Verma",
        "Shiva Singh", "Rohan maloo", "Jay Patekar", "Arvind Arora",
        "Virat Tomar", "Kuldeep Yadav"
    ],
    "Subject": [
        "Maths", "Science", "English", "History",
        "Maths", "Science", "English", "History",
        "computer", "Biology"
    ],
    "Marks": [70, 85, 90, 88, 68, 89, 77, 86, 80, 90]
}

# ✅ Create DataFrame and save to CSV
df = pd.DataFrame(students_data)
df.to_csv("data.csv", index=False)

# ✅ Calculate summary statistics
avg_marks = df["Marks"].mean()
topper = df.loc[df["Marks"].idxmax()]
lowest_scorer = df.loc[df["Marks"].idxmin()]
report_date = datetime.now().strftime("%d %B %Y")

# ✅ Custom PDF class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Student Marks Report", ln=True, align='C')
        self.set_font("Arial", '', 12)
        self.cell(0, 10, f"Report Date: {report_date}", ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

# ✅ Initialize PDF
pdf = PDF()
pdf.add_page()

# 📌 Summary Section
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Summary Statistics:", ln=True)

pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, f"Average Marks: {avg_marks:.2f}", ln=True)
pdf.cell(0, 10, f"Highest: {topper['Name']} ({topper['Subject']}) - {topper['Marks']} marks", ln=True)
pdf.cell(0, 10, f"Lowest: {lowest_scorer['Name']} ({lowest_scorer['Subject']}) - {lowest_scorer['Marks']} marks", ln=True)
pdf.ln(10)

# 📋 Table Header
pdf.set_font("Arial", 'B', 12)
pdf.set_fill_color(220, 230, 255)
pdf.cell(70, 10, "Name", border=1, align='C', fill=True)
pdf.cell(60, 10, "Subject", border=1, align='C', fill=True)
pdf.cell(30, 10, "Marks", border=1, align='C', fill=True)
pdf.ln()

# 📋 Table Rows
pdf.set_font("Arial", '', 12)
for _, row in df.iterrows():
    pdf.cell(70, 10, row["Name"], border=1)
    pdf.cell(60, 10, row["Subject"], border=1)
    pdf.cell(30, 10, str(row["Marks"]), border=1, align='C')
    pdf.ln()

# 💾 Export PDF
output_path = "output/student_marks_report.pdf"
pdf.output(output_path)
print(f"✅ PDF successfully saved to {output_path}")
