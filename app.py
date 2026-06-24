from flask import Flask, render_template, request, redirect
from models import db, User, Job
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import os
import pdfplumber
import spacy
import csv
from flask import Response
from datetime import datetime, date

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'greeshmita.bhogadi@gmail.com'
app.config['MAIL_PASSWORD'] = 'wkqfjprxinjluhvm'

mail = Mail(app)

app.secret_key = "mysecretkey123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/dashboard')

        return "Invalid Login"

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')
    


@app.route("/add_job", methods=["POST"])
def add_job():

    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    notes = request.form.get("notes", "")

    # ADD HERE
    job_link = request.form.get("job_link")

    priority = request.form.get(
        "priority",
        "Medium"
    )

    deadline = request.form.get("deadline")

    if deadline:
        deadline = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        ).date()
    else:
        deadline = None

    interview_date = request.form.get("interview_date")

    if interview_date:
        interview_date = datetime.strptime(
            interview_date,
            "%Y-%m-%d"
        ).date()
    else:
        interview_date = None

    new_job = Job(
    company=company,
    role=role,
    status=status,
    notes=notes,
    deadline=deadline,
    interview_date=interview_date,
    job_link=job_link,
    priority=priority
)

    db.session.add(new_job)
    db.session.commit()

    return redirect("/dashboard")

    db.session.add(new_job)
    
    db.session.commit()

    return redirect("/dashboard")
    notes = request.form["notes"]

    new_job = Job(
    company=company,
    role=role,
    status=status,
    notes=notes
)


@app.route('/delete/<int:id>')
def delete(id):

    job = Job.query.get_or_404(id)

    db.session.delete(job)

    db.session.commit()

    return redirect('/dashboard')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(
    name=name,
    email=email,
    password=generate_password_hash(password)
)
        

        db.session.add(new_user)
        db.session.commit()

        return "Registration Successful"

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    status = request.args.get("status")

    if status:
        jobs = Job.query.filter_by(status=status).all()
    else:
        jobs = Job.query.all()

    search = request.args.get("search")

    if search:
        jobs = Job.query.filter(
            Job.company.contains(search)
        ).all()

    total_jobs = len(jobs)

    applied = len(
        [j for j in jobs if j.status == "Applied"]
    )

    interview = len(
        [j for j in jobs if j.status == "Interview"]
    )

    offer = len(
        [j for j in jobs if j.status == "Offer"]
    )

    rejected = len(
        [j for j in jobs if j.status == "Rejected"]
    )

        # Generate Analytics Chart
    labels = ["Applied", "Interview", "Offer", "Rejected"]

    counts = [
        applied,
        interview,
        offer,
        rejected
    ]

    plt.figure(figsize=(5, 3))
    plt.bar(labels, counts)
    plt.title("Job Application Status")
    plt.tight_layout()
    plt.savefig("static/chart.png")
    plt.close()

    upcoming_interviews = Job.query.filter(
        Job.interview_date != None,
        Job.interview_date >= date.today()
    ).all()

    upcoming_deadlines = Job.query.filter(
        Job.deadline != None,
        Job.deadline >= date.today()
    ).all()

    

    return render_template(
    "dashboard.html",
    jobs=jobs,
    total_jobs=total_jobs,
    applied=applied,
    interview=interview,
    rejected=rejected,
    offer=offer,
    upcoming_interviews=upcoming_interviews,
    upcoming_deadlines=upcoming_deadlines
)

@app.route('/users')
def users():

    all_users = User.query.all()

    output = ""

    for user in all_users:
        output += f"{user.name} - {user.email}<br>"

    return output

@app.route('/upload_resume', methods=['POST'])
def upload_resume():

    resume = request.files['resume']

    if resume:

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            resume.filename
        )

        resume.save(filepath)

        text = ""

        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

        SKILLS = [
            "python",
            "java",
            "html",
            "css",
            "javascript",
            "react",
            "mysql",
            "flask",
            "aws",
            "machine learning"
        ]

        text_lower = text.lower()

        job_description = request.form.get(
            "job_description",
            ""
        ).lower()

        # Resume Skills
        found_skills = []

        for skill in SKILLS:
            if skill in text_lower:
                found_skills.append(skill)

        # JD Skills
        jd_skills = []

        for skill in SKILLS:
            if skill in job_description:
                jd_skills.append(skill)

        # Matching Skills
        matched_skills = []

        for skill in jd_skills:
            if skill in found_skills:
                matched_skills.append(skill)

        # Missing Skills
        missing_skills = []

        for skill in jd_skills:
            if skill not in found_skills:
                missing_skills.append(skill)

        # Match Score
        if len(jd_skills) > 0:
            match_score = int(
                len(matched_skills) /
                len(jd_skills) * 100
            )
        else:
            match_score = 0

        # ATS Score
        score = int(
            (len(found_skills) / len(SKILLS)) * 100
        )

        # Suggestions
        suggestions = []

        if score < 50:
            suggestions.append(
                "Add more technical skills"
            )

        if "aws" not in found_skills:
            suggestions.append(
                "Add AWS"
            )

        if "react" not in found_skills:
            suggestions.append(
                "Add React"
            )

        if "flask" not in found_skills:
            suggestions.append(
                "Add Flask projects"
            )

        return render_template(
            "resume_result.html",
            score=score,
            skills=found_skills,
            suggestions=suggestions,
            match_score=match_score,
            missing_skills=missing_skills
        )

    return redirect("/dashboard")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    job = Job.query.get_or_404(id)

    if request.method == 'POST':

        job.company = request.form['company']
        job.role = request.form['role']
        job.status = request.form['status']
        job.notes = request.form.get('notes', '')

        deadline = request.form.get('deadline')
        interview_date = request.form.get('interview_date')

        if deadline:
            job.deadline = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()
        else:
            job.deadline = None

        if interview_date:
            job.interview_date = datetime.strptime(
                interview_date,
                "%Y-%m-%d"
            ).date()
        else:
            job.interview_date = None

        db.session.commit()

        return redirect('/dashboard')

    return render_template(
        'edit_job.html',
        job=job
    )

@app.route('/export')
def export():

    jobs = Job.query.all()

    def generate():

        yield "Company,Role,Status,Date Applied,Deadline,Notes\n"

        for job in jobs:

            date_applied = (
                job.date_applied.strftime("%d-%m-%Y")
                if job.date_applied else ""
            )

            deadline = (
                job.deadline.strftime("%d-%m-%Y")
                if job.deadline else ""
            )

            yield (
                f"{job.company},"
                f"{job.role},"
                f"{job.status},"
                f"{date_applied},"
                f"{deadline},"
                f"{job.notes}\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=jobs.csv"
        }
    )
@app.route('/questions')
def questions():

    questions = [

        "Tell me about yourself",

        "Explain your project",

        "What is Flask?",

        "What is SQL?",

        "Difference between SQL and NoSQL?",

        "What is React?",

        "What is AWS?",

        "What is Machine Learning?"

    ]

    return render_template(
        "interview_questions.html",
        questions=questions
    )

@app.route('/send_mail')
def send_mail():

    msg = Message(
        "Interview Reminder",
        sender="greeshmita.bhogadi@gmail.com",
        recipients=["greeshmita.bhogadi@gmail.com"]
    )

    msg.body = """
Interview scheduled tomorrow.

Prepare:
- Resume
- Projects
- SQL
- Python
"""

    mail.send(msg)

    return "Email Sent Successfully"
if __name__ == '__main__':
    app.run(debug=True, port=5004)