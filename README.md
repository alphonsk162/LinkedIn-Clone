# 📌 LinkedIn Clone (Django)

A LinkedIn-like social networking web application built using **Django**.  
Users can create posts, like and comment (with replies), send connection requests, and manage their profiles — just like LinkedIn.  

---

## 🚀 Features

- ✅ User authentication (Sign up, login, logout)  
- ✅ User profile with photo, background image, headline, and summary   
- ✅ Like system with toggle functionality  
- ✅ Comment system with nested replies  
- ✅ Send, accept, and ignore connection requests  
- ✅ Feed displaying posts in reverse chronological order  
- ✅ Implemented profile management features that allow users to add and update their Education and Experience details.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)  
- **Database:** SQLite3 (default, easy to set up)  
- **Frontend:** Django Templates, HTML, CSS, JavaScript  
- **Static Files:** Django static files (CSS, JS, default images)  
- **Media Files:** For user uploads (profile photos, post images)  

---

## ⚙️ Setup Instructions

### 1 Clone the Repository
```bash
git clone https://github.com/your-username/linkedin-clone.git
cd linkedin-clone
```


### 2 Create and Activate Virtual Environment
```
python -m venv venv

# Activate virtual environment

# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate
```


### 3 Install Dependencies
```
pip install -r requirements.txt
```

### 4 Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 5 Run Development Server
```
python manage.py runserver
```

## Project Structure

```
├── background_photos
├── feed
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── linkedin_clone
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── post_images
├── profile_photos
├── README.md
├── Requirements
│   ├── Database_diagram.mmd
│   ├── User_personas.md
│   └── User_stories.md
├── requirements.txt
├── static
│   ├── css
│   ├── images
│   └── js
├── templates
│   ├── home.html
│   ├── landing_page.html
│   ├── login.html
│   ├── profile_page.html
│   ├── search_results.html
│   ├── signup.html
│   └── view_profile.html
├── User
│   ├── admin.py
│   ├── apps.py
│   ├── helper_functions.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── templatetags
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── venv


```