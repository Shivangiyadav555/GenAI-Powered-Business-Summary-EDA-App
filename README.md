

# 📊 GenAI-Powered Business Summary & EDA App
![011](https://github.com/user-attachments/assets/dc4c1e42-ee6a-4d5c-a5a1-a5d19b1d39e5)

A powerful, interactive app built with **Streamlit**, combining **automated EDA**, **visual insights**, and **GPT-based business summaries**. It enables users to upload datasets, explore key metrics, visualize distributions, and email executive summaries — all in real time.

---

## 🚀 Features!

![22](https://github.com/user-attachments/assets/32237f11-e294-432e-9625-6447ea66afef)


- 🔐 **Password-pro!
tected dashboard**
- 📁 Upload `.csv` or `.xlsx` files
- 🧹 Auto data cleaning & format detection
- 📊 Visualizations: Histogram, Pie Chart, Correlation Heatmap

![44](https://github.com/user-attachments/assets/3754d800-c06e-4690-8fed-8d86bb93d879)

![33](https://github.com/user-attachments/assets/3fe509e2-94de-4e81-b8cf-a8eaa48955ae)


- 📈 EDA report via [YData Profiling](https://github.com/ydataai/ydata-profiling)
  

- ![55](https://github.com/user-attachments/assets/9655f9b7-6a99-4316-8409-80e42d0a51f5)


- 🤖 GPT-based summary generation (mock/GPT-3.5)
- ✉️ Send summary + EDA report via Gmail SMTP
![66](https://github.com/user-attachments/assets/dda376f1-2d19-4116-b646-248d0ae9d124)

- 📥 Export plots as downloadable PNGs

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **Pandas**, **NumPy**
- **YData Profiling**
- **Seaborn**, **Plotly**
- **smtplib**, **email.message**
- **OpenAI GPT (optional)**

---

## 📂 Project Structure

📦 Project Folder ├── app.py # Main Streamlit app ├── eda_report.html # Auto-generated EDA report ├── extract_eda_insights.py # Extracts EDA stats ├── generate_business_report.py# Creates prompt from stats ├── gpt_summary.py # GPT or mock summary engine ├── scheduled_email.py # Sends email with summary + EDA


## 🧠 GPT Integration (Customizable)

```python
# In gpt_summary.py
USE_GPT = False  # Change to True and add your OpenAI key to use real GPT

...

## ✉️ Email Automation
In `scheduled_email.py`, configure:

```python
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"
RECEIVER_EMAIL = "recipient@example.com"
SEND_EDA_ATTACHMENT = True

⚙️ Run Locally
# Install required packages
pip install -r requirements.txt

# Launch Streamlit App
streamlit run app.py

# Optional: Send email via CLI
python scheduled_email.py

