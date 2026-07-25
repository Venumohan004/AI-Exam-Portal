# 🎓 AI Exam Portal – Smart Online Examination System

<div align="center">

![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-7952B3?style=for-the-badge&logo=bootstrap)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 🚀 A modern AI-powered online examination platform with automated evaluation, performance analytics, and PDF result generation.

</div>

---

## 🔗 Live Demo

🌐 **Live Application:** [https://your-live-demo-link.com](https://your-live-demo-link.com)  
📂 **GitHub Repository:** [https://github.com/Venumohan004/AI-Exam-Portal](https://github.com/Venumohan004/AI-Exam-Portal)

---

## ✨ Features

### 👨‍🎓 Student Features
- Secure user registration & login
- Browse available exams
- Attempt timed online exams
- Automatic answer saving
- Instant result calculation
- AI-generated performance feedback
- Download result as PDF
- View detailed question analysis
- Track previous exam history

### 👨‍🏫 Admin Features
- Create, update, and delete exams
- Add multiple-choice questions
- Manage options and correct answers
- View student performance analytics
- Monitor exam attempts and scores
- Generate downloadable reports

### 🤖 AI Features
- Intelligent performance feedback
- Strength and weakness analysis
- Personalized improvement suggestions
- Difficulty-wise score evaluation

---

## 📸 Screenshots

| Dashboard | Exam Page |
|-----------|------------|
| ![Dashboard](assets/dashboard.png) | ![Exam](assets/exam-page.png) |

| Result Page | Analytics |
|-------------|------------|
| ![Result](assets/result-page.png) | ![Analytics](assets/analytics.png) |

> 📌 Replace the placeholder images with actual screenshots from the `assets/` folder.

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-------------|
| **Backend** | Django 5 |
| **Language** | Python 3 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | Bootstrap 5 |
| **Database** | SQLite |
| **PDF Generation** | ReportLab |
| **Authentication** | Django Auth System |
| **Templating** | Django Templates |
| **Version Control** | Git & GitHub |

---

## 🏗️ Project Architecture

```text
AI_Exam_Portal/
│
├── ai_exam_portal/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── exams/                   # Main application
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── templates/               # Global templates
│   └── base.html
│
├── static/                  # Global static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                   # Uploaded files
├── db.sqlite3               # SQLite database
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Venumohan004/AI-Exam-Portal.git
cd AI-Exam-Portal
```

---

## 🐍 Environment Setup

### Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Migration

Apply migrations to create the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Create Superuser

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:

- Username
- Email
- Password

---

## ▶️ Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## 🔑 Default Login Credentials

> ⚠️ Replace these placeholders before sharing publicly.

| Role | Username | Password |
|------|-----------|-----------|
| Admin | `admin` | `admin123` |
| Student | `student1` | `student123` |

---

## 📖 Usage Flow

### Student Workflow

```text
Register/Login
      ↓
View Available Exams
      ↓
Start Timed Exam
      ↓
Submit Answers
      ↓
Auto Evaluation
      ↓
View Result & AI Feedback
      ↓
Download PDF Report
```

### Admin Workflow

```text
Login to Admin Panel
      ↓
Create Exam
      ↓
Add Questions & Options
      ↓
Publish Exam
      ↓
Monitor Attempts
      ↓
Analyze Student Performance
```

---

## 🤖 AI Feedback Engine

The platform includes a lightweight AI feedback module that analyzes exam performance and generates personalized suggestions.

### Feedback Includes

- **Overall performance assessment**
- **Strong subject areas**
- **Weak concepts requiring attention**
- **Difficulty-wise analysis**
- **Recommended improvement strategy**

### Example

```text
Excellent performance! You scored 90%.
You have a strong understanding of Python basics.
Focus on improving exception handling and OOP concepts for advanced proficiency.
```

This feature helps students understand **why** they scored a particular result, not just the score itself.

---

## 📄 PDF Result Download

The system uses **ReportLab** to generate professional PDF reports.

### Report Contains

- Student name
- Exam title
- Subject
- Total score
- Percentage
- Pass/Fail status
- Submission date
- AI feedback summary

### Download Endpoint

```text
/results/<attempt_id>/pdf/
```

Students can download and share their result reports for academic records.

---

## 📊 Analytics Dashboard

The admin dashboard provides real-time insights into examination performance.

### Available Metrics

- Total exams
- Total students
- Total attempts
- Average score
- Pass percentage
- Subject-wise performance
- Difficulty-wise performance
- Recent exam activity

### Dashboard Highlights

| Metric | Description |
|--------|-------------|
| **Average Score** | Overall student performance |
| **Pass Rate** | Percentage of successful attempts |
| **Top Subject** | Best-performing subject |
| **Recent Attempts** | Latest student submissions |

---

## 🚀 Future Enhancements

- [ ] AI-based adaptive exams
- [ ] Question randomization
- [ ] Negative marking support
- [ ] Email notifications
- [ ] JWT/API integration
- [ ] REST API with Django REST Framework
- [ ] Excel report export
- [ ] Leaderboard & rankings
- [ ] Dark mode support
- [ ] Cloud deployment (Render/AWS)

---

## 📚 Learning Outcomes

This project helped me gain practical experience in:

- Django MVT architecture
- Authentication & authorization
- CRUD operations
- Form handling & validation
- Database design with SQLite
- Timer-based exam systems
- Automated evaluation logic
- PDF generation with ReportLab
- Bootstrap responsive UI design
- Git & GitHub workflow
- Building a complete production-style web application

---

## 📈 Project Status

| Module | Status |
|--------|--------|
| Authentication | ✅ Completed |
| Exam Management | ✅ Completed |
| Question Engine | ✅ Completed |
| Timer System | ✅ Completed |
| Auto Evaluation | ✅ Completed |
| AI Feedback | ✅ Completed |
| PDF Reports | ✅ Completed |
| Analytics Dashboard | ✅ Completed |
| Responsive UI | ✅ Completed |
| Deployment Ready | ✅ Completed |

---

## 👨‍💻 Author

<div align="center">

### **P. Venumohan**

🎓 **B.Tech – Computer Science & Data Science Engineering (2026)**

📌 **GitHub:** [github.com/Venumohan004](https://github.com/Venumohan004)  
💼 **LinkedIn:** [linkedin.com/in/venumohan-p-522017346](https://www.linkedin.com/in/venumohan-p-522017346)  
📧 **Email:** pvenumohan004@gmail.com

</div>

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

```bash
# Fork the repository
# Create a feature branch
git checkout -b feature/your-feature

# Commit changes
git commit -m "Add your feature"

# Push to GitHub
git push origin feature/your-feature
```

Then open a **Pull Request**.

---

## 📜 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 P. Venumohan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software.
```

---

<div align="center">

### ⭐ If you found this project useful, please give it a star on GitHub!

**Built with ❤️ using Django 5 and Bootstrap 5**

</div>
