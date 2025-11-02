# daily_report.py
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import random
import smtplib
from email.message import EmailMessage
import schedule
import time


# -----------------------------
# 1️⃣ Generate Random Sales Data
# -----------------------------
def generate_random_sales_csv(filepath):
    products = ["Protein Shake", "Gym Towel", "Water Bottle", "Yoga Mat", "Energy Bar"]
    rows = []

    for product in products:
        units_sold = random.randint(5, 50)
        revenue = units_sold * random.randint(20, 50)  # random price per unit
        rows.append(
            {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Product": product,
                "Units_Sold": units_sold,
                "Revenue": revenue,
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    print(f"✅ Random sales data generated at {filepath}")


# -----------------------------
# 2️⃣ Load CSV Data
# -----------------------------
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df


# -----------------------------
# 3️⃣ Generate Summary
# -----------------------------
def generate_summary(df):
    total_sales = df["Revenue"].sum()
    total_units = df["Units_Sold"].sum()
    top_product = df.loc[df["Revenue"].idxmax(), "Product"]

    summary = {
        "total_sales": total_sales,
        "total_units": total_units,
        "top_product": top_product,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
    }
    return summary


# -----------------------------
# 4️⃣ Create PDF
# -----------------------------
def create_pdf(summary, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Daily Sales Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Date: {summary['report_date']}")
    c.drawString(50, 730, f"Total Revenue: R{summary['total_sales']}")
    c.drawString(50, 700, f"Total Units Sold: {summary['total_units']}")
    c.drawString(50, 670, f"Top Performing Product: {summary['top_product']}")

    c.save()


# -----------------------------
# 5️⃣ Send Email with PDF
# -----------------------------
def send_email_with_attachment(to_email, subject, body, attachment_path):
    from_email = "endanisadafk@gmail.com"  # replace with your email
    password = "your-app-password"  # Gmail App Password

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
    msg.add_attachment(
        file_data, maintype="application", subtype="pdf", filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

    print(f"📧 Email sent to {to_email} with attachment {file_name}")


# -----------------------------
# 6️⃣ Generate Daily Report
# -----------------------------
def generate_daily_report():
    # Ensure data and report folders exist
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("reports"):
        os.makedirs("reports")

    csv_path = "data/sales_data.csv"

    # Generate random sales data
    generate_random_sales_csv(csv_path)

    # Load data and generate summary
    df = load_data(csv_path)
    summary = generate_summary(df)

    # Create PDF report
    filename = f"reports/daily_report_{summary['report_date']}.pdf"
    create_pdf(summary, filename)
    print(f"✅ Report generated: {filename}")

    # Send PDF via email
    send_email_with_attachment(
        to_email="endanisadafk@gmail.com",  # replace with the email to receive reports
        subject="Daily Sales Report",
        body="Here is the daily sales report.",
        attachment_path=filename,
    )


# -----------------------------
# 7️⃣ Optional: Schedule Daily
# -----------------------------
# Test run
schedule.every().day.at("06:00").do(generate_daily_report)

print("🕒 Scheduler started... Press CTRL+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
