AI Job Tracker & Resume Analyzer

Overview
AI Job Tracker is a Flask-based web application that helps users manage job applications, track interviews, analyze resumes, and improve ATS scores.

Features
Job Application Tracking
* Add new job applications
* Update application status
* Delete applications
* Track deadlines
* Track interview dates
  
Dashboard Analytics
* Total jobs applied
* Applied jobs count
* Interview count
* Offer count
* Rejected count
* Analytics chart visualization
  
Search & Filter
* Search jobs by company
* Filter jobs by status
  
Resume Analyzer
* Upload PDF resumes
* Extract skills automatically
* ATS score calculation
* Job Description matching
* Missing skills detection
* Resume improvement suggestions

Email Reminder System
* Send interview reminders using Gmail SMTP
* Flask-Mail integration
  
CSV Export
* Export all job applications into CSV format
  
Technologies Used
Frontend
* HTML5
* CSS3
* Jinja2 Templates
  
Backend
* Python
* Flask
* SQLAlchemy
  
Database
* SQLite
  
AI & Data Processing
* spaCy
* PDFPlumber
* Matplotlib
  
Email Service
* Flask-Mail
  
Project Structure
AI-Job-Tracker/
├── app.py
├── models.py
├── requirements.txt
├── templates/
│ ├── dashboard.html
│ ├── login.html
│ ├── register.html
│ ├── resume_result.html
│ ├── edit_job.html
│ └── interview_questions.html
├── static/
│ ├── style.css
│ └── chart.png
├── uploads/
└── README.md

Installation
Clone Repository
git clone https://github.com/yourusername/AI-Job-Tracker.git
Install Dependencies
pip install -r requirements.txt
Run Application
python app.py
Open Browser
http://127.0.0.1:5004

Future Enhancements
* Pie Chart Analytics
* Job Recommendation System
* LinkedIn Job Integration
* AI Interview Preparation Bot
* Email Scheduling
* Cloud Deployment
Author
Chakiri Shanmukha Sai
Computer Science Graduate
Aspiring Software Developer & AI Enthusiast

VSCODE terminal - pwd
Run commands - git init , git add . git commit -m "Initial AI Job Tracker Project"
