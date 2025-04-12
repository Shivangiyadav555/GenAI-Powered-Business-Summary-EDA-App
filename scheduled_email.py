import pandas as pd
import smtplib
from email.message import EmailMessage
from ydata_profiling import ProfileReport
import tempfile
import os
from datetime import datetime

# === CONFIGURATION ===

CSV_PATH = "C:/Users/yadav/Downloads/Train.csv"
SENDER_EMAIL = "yadavshiavngi555@gmail.com"
APP_PASSWORD = "xwuklxccsnrfxmpo"
RECEIVER_EMAIL = "ankshi91666@gmail.com"
SEND_EDA_ATTACHMENT = True
EMAIL_SUBJECT = f"📈 Daily Business Summary - {datetime.today().strftime('%Y-%m-%d')}"


# === STEP 1: Load and clean data ===
def load_data(path):
    try:
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='ISO-8859-1')

    df.columns = df.columns.str.strip()
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, df.nunique(dropna=False) > 1]

    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype(str).str.strip()

    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                converted = pd.to_datetime(df[col])
                if converted.notnull().sum() > 0:
                    df[col] = converted
            except:
                pass

    return df

# === STEP 2: Generate text summary ===
def generate_summary(df):
    return f"""
    ✅ Automated Business Summary:
    - Rows: {df.shape[0]}
    - Columns: {df.shape[1]}
    - Top columns: {', '.join(df.columns[:5])}
    - Missing values: {df.isnull().sum().sum()} total cells
    """

# === STEP 3: Generate EDA Report (HTML) ===
def generate_eda(df):
    profile = ProfileReport(df, title="Automated EDA Report", explorative=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        profile.to_file(tmp_file.name)
        return tmp_file.name

# === STEP 4: Send Email ===
def send_email(summary, eda_path=None):
    msg = EmailMessage()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(summary)

    if eda_path and SEND_EDA_ATTACHMENT:
        with open(eda_path, "rb") as f:
            msg.add_attachment(f.read(), maintype='text', subtype='html', filename="EDA_Report.html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    df = load_data(CSV_PATH)
    summary = generate_summary(df)
    eda_file = generate_eda(df) if SEND_EDA_ATTACHMENT else None
    send_email(summary, eda_file)

    # Clean up temporary file
    if eda_file and os.path.exists(eda_file):
        os.remove(eda_file)
