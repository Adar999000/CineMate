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

### 1. הורדת הפרויקט
```bash
git clone https://github.com/your-username/cinemate.git
cd cinemate
```

### 2. יצירת סביבה וירטואלית
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 4. הגדרת משתני סביבה
צור קובץ `.env` בתיקיית הפרויקט:
```env
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+18+for+SQL+Server
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. הרצת המערכת
```bash
python run.py
```
המערכת תהיה זמינה בכתובת: `http://localhost:5000`

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
