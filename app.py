from flask import Flask, request, jsonify, render_template
import requests
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Azure settings from .env file
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")


@app.route('/')
def index():
    return render_template('index.html')


def personalize_report(report, user_name):
    today = datetime.now().strftime("%B %d, %Y")
    
    # Replace placeholders if they exist
    personalized = report.replace("[Your Name]", user_name).replace("[Date]", today)
    
    # If Azure didn’t include placeholders, add a signature manually
    if "[Your Name]" not in report and user_name not in report:
        personalized += f"\n\nRegards,\n{user_name}"

    return personalized


def generate_report_from_azure(topic, name):
    if not all([AZURE_ENDPOINT, AZURE_API_KEY, AZURE_DEPLOYMENT_NAME]):
        raise Exception("Missing Azure configuration! Check .env file.")

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    prompt = (
        f"Write a professional report for a user named {name} on the topic: {topic}. "
        f"Include [Your Name] and [Date] placeholders at appropriate places in the report."
    )

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 600
    }

    url = f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT_NAME}/chat/completions?api-version=2023-03-15-preview"
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "error" in result:
        raise Exception(f"Azure API Error: {result['error']['message']}")
    
    if "choices" not in result:
        raise Exception("Missing 'choices' in Azure response.")

    return result['choices'][0]['message']['content']


def send_email(to_email, report_content):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    msg = MIMEText(report_content)
    msg["Subject"] = "Your AI Generated Report"
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


@app.route('/generate-report', methods=['POST'])
def handle_report():
    data = request.get_json()
    name = data['name']
    topic = data['topic']
    email = data['email']

    raw_report = generate_report_from_azure(topic, name)
    personalized_report = personalize_report(raw_report, name)

    send_email(email, personalized_report)

    return f"Report generated and sent to {email}!"


if __name__ == '__main__':
    app.run(debug=True)
