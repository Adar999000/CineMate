# חלוקת צוות - CineMate

## 👨‍💻 ארז ארנון: Frontend & UI/UX
אחראי על ממשק המשתמש וחווית המשתמש

### View Layer
```
📂 app/templates/
  ├── layouts/                # תבניות בסיס
  │   ├── base.html
  │   └── base_login.html
  ├── public/                # דפים ציבוריים
  │   ├── home_page.html
  │   ├── about.html
  │   ├── contact.html
  │   └── faq.html
  ├── user/                  # דפי משתמש
  │   ├── dashboard_user.html
  │   ├── profile.html
  │   ├── edit_profile.html
  │   ├── all_movies.html
  │   ├── movie_details.html
  │   └── movies_list.html
  └── errors/                # דפי שגיאה
      ├── error_404.html
      └── error_500.html
```
### Authentication
```
📂 app/templates/auth/
  ├── login.html            # התחברות
  ├── register.html         # הרשמה
  └── forgot_password.html  # שחזור סיסמה

### Static Assets
```
📂 app/static/
  ├── css/                   # סגנונות
  ├── js/                    # סקריפטים
  ├── profile_images/        # תמונות פרופיל
  └── images/                # תמונות כלליות
      ├── logo.png
      └── chatbot.png
```

## 🔒 שובל מגיורא: Backend Core & Authentication
אחראי על ליבת המערכת ומערכת האימות

### Core Components
```
📂 app/
  ├── __init__.py           # אתחול האפליקציה
  ├── config.py             # הגדרות
  └── models.py             # מודלים
```

```

### API & Database
```
📂 app/
  ├── routes.py             # נתיבי API
  └── migrations/           # מיגרציות DB
```

## 🎯 אדר זילברשטיין: Business Logic, Admin & AI Bot
אחראי על הלוגיקה העסקית, ממשק ניהול וצ'אטבוט AI

### Business Logic
```
📂 app/services/
  └── user_service.py       # שירותי משתמשים
  ├── movie_service.py      # שירותי סרטים
  └── rental_service.py     # שירותי השכרות

📂 app/utils/
  └── email_utils.py        # שירותי אימייל
```

### Admin Interface
```
📂 app/templates/admin/
  ├── dashboard_admin.html  # דשבורד ניהול
  ├── admin_edit_movies.html # ניהול סרטים
  ├── admin_users_list.html # ניהול משתמשים
  ├── admin_rentals.html    # ניהול השכרות
  ├── admin_submissions.html # ניהול פניות
  ├── admin_edit_user.html  # עריכת משתמש
  ├── add_movie.html       # הוספת סרט
  └── edit_movie.html      # עריכת סרט
```

### AI Chatbot
```
📂 app/
  ├── ai_service.py         # שירות הצ'אטבוט
  └── templates/components/
      └── chat_widget.html  # ממשק צ'אט
```


## 📂 קבצי תצורה
```
📂 root/
  ├── run.py               # הפעלת השרת
  └── requirements.txt     # תלויות
```

## 🤝 קבצים משותפים
```
README.md                     # תיעוד הפרויקט
team_division.md             # חלוקת קבצים לצוות (קובץ זה)
.gitignore                   # הגדרות Git
```

## 📝 הערות
- כל מפתח אחראי על הבדיקות היחידה של הקבצים שלו
- שינויים בקבצים משותפים דורשים תיאום בין חברי הצוות
- כל מפתח אחראי לתעד את הקוד שלו
- יש לעקוב אחר סטנדרט הקוד המוסכם
