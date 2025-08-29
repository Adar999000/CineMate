# CineMate - מערכת השכרת סרטים 🎬

מערכת ניהול השכרת סרטים מתקדמת המאפשרת למשתמשים לשכור סרטים ולמנהלים לנהל את מלאי הסרטים, המשתמשים וההשכרות.

## 🌟 תכונות עיקריות
- **ניהול משתמשים**: הרשמה, התחברות ועריכת פרופיל
- **ניהול סרטים**: הוספה, עריכה ומחיקה של סרטים
- **מערכת השכרות**: ניהול השכרות סרטים ומעקב אחר היסטוריה
- **צ'אטבוט AI**: עוזר חכם המבוסס על Ollama לייעוץ בבחירת סרטים
- **ממשק מנהל**: ניהול משתמשים, סרטים והשכרות
- **מערכת פניות**: טופס יצירת קשר וניהול פניות משתמשים

## 🛠️ טכנולוגיות
- **Backend**: Python 3.11, Flask 3.1.0
- **Database**: SQL Server (מאוחסן ב-Somee.com)
- **ORM**: SQLAlchemy 2.0.40
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **AI Integration**: Ollama (Mistral model)
- **Email Service**: Gmail SMTP

## 📋 דרישות מערכת
- Python 3.11 ומעלה
- ODBC Driver 18 for SQL Server
- pip (Python Package Manager)

## ⚙️ התקנה והגדרה

### 1. דרישות מקדימות
1. התקן את Python 3.11 או גרסה חדשה יותר מ-[python.org](https://www.python.org/downloads/)
2. התקן את ODBC Driver 18 for SQL Server מ-[Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
3. וודא ש-pip מותקן ומעודכן:
   ```bash
   python -m pip install --upgrade pip
   ```
4. התקן את Ollama מ-[ollama.ai](https://ollama.ai/download)

### 2. הורדת הפרויקט
```bash
# העתקת הפרויקט
git clone https://github.com/adar0/cinemate.git
cd cinemate
```

### 3. יצירת סביבה וירטואלית
```bash
# יצירת סביבה חדשה
python -m venv venv

# הפעלת הסביבה
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. התקנת תלויות
```bash
# התקנת כל החבילות הנדרשות
pip install -r requirements.txt

# הורדת מודל ה-AI
ollama pull mistral
```

### 5. הגדרת משתני סביבה
צור קובץ `.env` בתיקיית הפרויקט עם התוכן הבא:
```env
# חיבור למסד הנתונים
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://username:password@CinemaDB.mssql.somee.com/CinemaDB?driver=ODBC+Driver+18+for+SQL+Server

# מפתח הצפנה (שנה לערך מורכב)
SECRET_KEY=your-very-long-and-secure-secret-key

# הגדרות שירות האימייל
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password  # צור ב-Google Account -> Security -> App Passwords
```

### 6. אתחול מסד הנתונים
```bash
# יצירת טבלאות ונתוני בסיס
flask db upgrade
```

### 7. הרצת המערכת
```bash
# הפעלת השרת
python run.py
```
המערכת תהיה זמינה בכתובת: `http://localhost:5000`

### 8. בדיקת התקנה
1. וודא שהשרת פועל ללא שגיאות
2. היכנס ל-`http://localhost:5000`
3. נסה להירשם ולהתחבר
4. בדוק שהצ'אטבוט מגיב

## 🔑 הרשאות משתמשים

### משתמש רגיל
- צפייה ברשימת סרטים
- השכרת סרטים
- צפייה בהיסטוריית השכרות
- עריכת פרופיל אישי
- שליחת פניות

### מנהל מערכת
- כל הרשאות המשתמש הרגיל
- ניהול משתמשים
- ניהול מלאי סרטים
- ניהול השכרות
- טיפול בפניות משתמשים

## 📡 API Endpoints

### Authentication
- `POST /login`: התחברות למערכת
- `POST /register`: הרשמה למערכת
- `GET /logout`: התנתקות מהמערכת

### Users
- `GET /profile`: צפייה בפרופיל אישי
- `PUT /profile/edit`: עריכת פרופיל
- `POST /forgot-password`: שחזור סיסמה

### Movies
- `GET /movies`: רשימת כל הסרטים
- `GET /movies/<id>`: פרטי סרט ספציפי
- `POST /movies/rent/<id>`: השכרת סרט

### Admin
- `GET /admin/dashboard`: דשבורד ניהול
- `GET /admin/users`: ניהול משתמשים
- `GET /admin/movies`: ניהול סרטים
- `GET /admin/rentals`: ניהול השכרות
- `GET /admin/submissions`: ניהול פניות

### AI Chatbot
- `POST /chat`: שליחת שאלה לצ'אטבוט

## 🔧 תצורת מסד הנתונים
המערכת משתמשת במסד נתונים SQL Server המאוחסן ב-Somee.com:
- שרת: `CinemaDB.mssql.somee.com`
- מסד נתונים: `CinemaDB`
- דרייבר: `ODBC Driver 18 for SQL Server`

## 🤝 תרומה לפרויקט
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📝 רישיון
MIT License - ראה קובץ [LICENSE](LICENSE) לפרטים נוספים.

## 👥 יוצרים
- אדר זילברשטיין
- ארז ארנון
- שובל מגיורא
- [GitHub](https://github.com/adar0)
- [LinkedIn](https://linkedin.com/in/adar-zilberstein)
