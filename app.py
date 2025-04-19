import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
from io import StringIO
import tempfile
import openai
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.set_page_config(page_title="GenAI-Powered EDA & Email App", layout="wide")
st.title("📊 GenAI-Powered Business Summary & EDA App")

# === App Access Control ===
MASTER_APP_PASSWORD = "wuklxccsnrfxmpo"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔒 Enter App Password")
    user_password = st.text_input("Enter the access password to use this app:", type="password")
    submit_pass = st.button("Unlock")
    if submit_pass and user_password == MASTER_APP_PASSWORD:
        st.session_state.authenticated = True
        st.success("🔓 Access granted!")
        st.rerun()
    elif submit_pass:
        st.error("❌ Incorrect app password. Please try again.")
    st.stop()

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "eda_path" not in st.session_state:
    st.session_state.eda_path = ""

# Upload section
st.header("📁 Upload Your Data File")
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1]
    if file_extension == ".csv":
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    elif file_extension == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    # 🔍 Auto-cleaning and type detection
    st.subheader("🧹 Data Cleaning & Format Detection")
    original_shape = df.shape

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Drop empty or constant columns
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, df.nunique(dropna=False) > 1]

    # Trim string cells
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype(str).str.strip()

    # Convert date-like columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                converted = pd.to_datetime(df[col])
                if converted.notnull().sum() > 0:
                    df[col] = converted
            except Exception:
                pass

    cleaned_shape = df.shape
    st.success(f"Cleaned dataset: {original_shape} → {cleaned_shape} (rows, columns)")

    # Data Preview
    st.header("🔍 Data Preview")
    st.dataframe(df.head())

    # 📈 Visual Insights Section
    st.header("📊 Visual Insights")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    if numeric_cols:
        st.subheader("Histogram for Numeric Columns")
        col_to_plot = st.selectbox("Select numeric column for histogram", numeric_cols)
        fig1 = px.histogram(df, x=col_to_plot, nbins=30, title=f"Histogram of {col_to_plot}")
        st.plotly_chart(fig1)

        st.subheader("Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig2, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig2)

    if categorical_cols:
        st.subheader("Pie Chart for Categorical Columns")
        cat_col = st.selectbox("Select categorical column for pie chart", categorical_cols)
        pie_data = df[cat_col].value_counts().reset_index()
        pie_data.columns = [cat_col, 'count']
        fig3 = px.pie(pie_data, names=cat_col, values='count', title=f"Distribution of {cat_col}")
        st.plotly_chart(fig3)

    # EDA Section
    st.header("📊 Exploratory Data Analysis (EDA) Report")
    if st.button("Generate EDA Report"):
        with st.spinner("Generating report..."):
            profile = ProfileReport(df, title="EDA Report", explorative=True)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                profile.to_file(tmp_file.name)
                st.session_state.eda_path = tmp_file.name

            with open(st.session_state.eda_path, "rb") as f:
                st.download_button(
                    label="📥 Download EDA Report",
                    data=f,
                    file_name="EDA_Report.html",
                    mime="text/html"
                )

    # GPT Summary Toggle
    st.header("🤖 AI-Generated Summary")
    use_gpt = st.checkbox("Use Real GPT-3.5 Summary (requires OpenAI API key)")

    if use_gpt:
        openai_key = st.text_input("Enter your OpenAI API key (starts with sk-...)", type="password")

    if st.button("Generate Summary"):
        if use_gpt and openai_key:
            try:
                openai.api_key = openai_key
                basic_info = f"Dataset with {df.shape[0]} rows and {df.shape[1]} columns. Columns: {', '.join(df.columns[:5])}"
                prompt = f"Analyze the following dataset description and provide an insightful summary:\n{basic_info}"

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a data analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )

                st.session_state.summary = response.choices[0].message.content.strip()
            except Exception as e:
                st.session_state.summary = f"❌ GPT Summary failed: {e}"
        else:
            st.session_state.summary = f"""
            - Number of rows: {df.shape[0]}
            - Number of columns: {df.shape[1]}
            - Columns: {', '.join(df.columns[:5])}...
            - Missing values detected: {df.isnull().sum().sum()} cells
            """

    st.text_area("Summary Preview", value=st.session_state.summary, height=150)

    # Email Section
    st.header("📧 Send Summary via Email")
    with st.form("email_form"):
        sender_email = st.text_input("Sender Gmail (App password required)")
        sender_password = st.text_input("App Password", type="password")
        receiver_email = st.text_input("Receiver Email")
        subject = st.text_input("Email Subject", value="Business Summary Report")
        attach_eda = st.checkbox("📎 Attach EDA Report to Email")
        submitted = st.form_submit_button("Send Email")

        if submitted:
            if not (sender_email and sender_password and receiver_email and subject and st.session_state.summary.strip()):
                st.warning("⚠ All fields are required, including a generated summary!")
            else:
                try:
                    msg = EmailMessage()
                    msg["Subject"] = subject
                    msg["From"] = sender_email
                    msg["To"] = receiver_email
                    msg.set_content(st.session_state.summary)

                    if attach_eda:
                        if not st.session_state.eda_path:
                            with st.spinner("Generating EDA Report for email..."):
                                profile = ProfileReport(df, title="EDA Report", explorative=True)
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                                    profile.to_file(tmp_file.name)
                                    st.session_state.eda_path = tmp_file.name

                        with open(st.session_state.eda_path, "rb") as f:
                            msg.add_attachment(f.read(), maintype='text', subtype='html', filename="EDA_Report.html")

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(sender_email, sender_password)
                        smtp.send_message(msg)

                    st.success("✅ Email sent successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")
else:
    st.info("Please upload a dataset to begin.")
