# 👥 חלוקת קבצים לפי חברי צוות - CineMate

## 🎨 ארז ארנון: Frontend & UI/UX
אחראי על כל ממשקי המשתמש, עיצוב, וחוויית משתמש

### תבניות (Templates)
```
📂 templates/
  ├── layouts/
  │   ├── base.html               # תבנית הבסיס
  │   └── base_login.html         # תבנית להתחברות
  ├── public/
  │   ├── home_page.html          # דף הבית
  │   ├── about.html              # אודות
  │   ├── contact.html            # יצירת קשר
  │   └── faq.html               # שאלות נפוצות
  ├── user/
  │   ├── dashboard_user.html     # דשבורד משתמש
  │   ├── profile.html           # פרופיל
  │   ├── edit_profile.html      # עריכת פרופיל
  │   ├── all_movies.html        # רשימת סרטים
  │   ├── movie_details.html     # פרטי סרט
  │   └── my_rentals.html        # השכרות שלי
  ├── auth/
  │   ├── login.html             # התחברות
  │   ├── register.html          # הרשמה
  │   └── forgot_password.html   # שכחתי סיסמה
  ├── errors/
  │   ├── error_404.html         # דף 404
  │   └── error_500.html         # דף 500
  └── components/
      └── chat_widget.html       # ווידג'ט צ'אט
```

### קבצים סטטיים
```
📂 static/
  ├── css/                       # קבצי עיצוב
  ├── js/                        # סקריפטים
  ├── profile_images/            # תמונות פרופיל
  ├── movie_posters/            # פוסטרים של סרטים
  └── images/
      ├── logo.png              # לוגו האתר
      ├── chatbot.png           # אייקון צ'אטבוט
      └── user.png              # אייקון משתמש
```

## 💾 שובל מגיורא: Backend Core & Authentication
אחראי על תשתית המערכת, מסד הנתונים ומערכת ההרשאות

### קבצי ליבה
```
📂 app/
  ├── __init__.py               # הגדרת האפליקציה
  ├── config.py                 # הגדרות המערכת
  ├── models.py                 # מודלים של מסד הנתונים
  └── services/
      └── user_service.py       # שירותי משתמשים

📂 migrations/                  # סקריפטי מיגרציה למסד נתונים
requirements.txt               # תלויות הפרויקט
.env                          # משתני סביבה
```

### בדיקות
```
📂 tests/
  ├── test_auth.py             # בדיקות אימות
  ├── test_models.py           # בדיקות מודלים
  └── test_api.py              # בדיקות API
```

## 🔧 אדר זילברשטיין: Business Logic & Admin
אחראי על הלוגיקה העסקית וממשק הניהול

### לוגיקה עסקית
```
📂 app/
  ├── routes.py                # נתיבים ובקרים
  ├── ai_service.py            # שירות הצ'אטבוט
  └── services/
      ├── movie_service.py     # שירותי סרטים
      └── rental_service.py    # שירותי השכרות
```

### ממשק ניהול
```
📂 templates/admin/
  ├── dashboard_admin.html     # דשבורד מנהל
  ├── admin_edit_movies.html   # ניהול סרטים
  ├── admin_users_list.html    # ניהול משתמשים
  ├── admin_rentals.html       # ניהול השכרות
  ├── admin_submissions.html   # ניהול פניות
  ├── add_movie.html          # הוספת סרט
  └── edit_movie.html         # עריכת סרט

📂 utils/
  ├── email_utils.py          # שירותי אימייל
  └── admin_utils.py          # פונקציות עזר למנהל
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
