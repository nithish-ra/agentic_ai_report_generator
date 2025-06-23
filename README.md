# 📄 AI Report Generator

A smart Flask web application that generates professional reports using Azure OpenAI and emails them to the user. Perfect for students, researchers, or businesses who want automated, personalized content on-demand.

---

## 🚀 Features

- 🔥 Uses **Azure OpenAI** to generate report content based on user input.
- ✉️ Emails the generated report to the user using **SMTP (Gmail)**.
- 🌐 Simple and responsive HTML frontend with a form.
- 🔐 Securely manages sensitive data with `.env` and ignores it from version control.
- 🧪 Easy to test and extend for new features or use cases.

---

## 🖼️ Screenshot

![App Screenshot](https://images/Screenshot 2025-06-23 141408.png.com)

---

## 🏗️ Folder Structure

ai-report-generator/
├── app.py # Main Flask app logic
├── templates/
│ └── index.html # Frontend UI (HTML form)
├── .env # Sensitive credentials (ignored in Git)
├── .env.example # Template for your environment config
├── .gitignore # Git ignore rules
└── README.md # This file


---

## 🧪 Tech Stack

- **Python 3.8+**
- **Flask** – web framework
- **Azure OpenAI Service** – for report generation
- **Gmail SMTP** – to send emails securely
- **dotenv** – for environment variable management

---

3. Create a .env File
Duplicate the .env.example file:
cp .env.example .env
Then fill in your real credentials:

env
Copy
Edit
AZURE_API_KEY=your-azure-api-key
AZURE_ENDPOINT=https://your-azure-endpoint
AZURE_DEPLOYMENT_NAME=your-model-deployment-name

SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

4. Run the App
python app.py
Open your browser and visit:
http://127.0.0.1:5000
