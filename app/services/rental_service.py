from app.models import Rental, User, Movie
from app import db
from datetime import date

# ✔ יצירת השכרה חדשה
def create_rental(user_id, movie_id):
    rental = Rental(user_id=user_id, movie_id=movie_id, rent_date=date.today())
    db.session.add(rental)
    db.session.commit()

# ✔ החזרת כל ההשכרות בלבד
def get_all_rentals():
    return Rental.query.all()

# ✔ החזרת כל ההשכרות עם פרטי משתמש וסרט (עבור דשבורד אדמין)
def get_all_rentals_with_details():
    rentals = Rental.query.all()
    detailed_rentals = []
    for rental in rentals:
        user = User.query.get(rental.user_id)
        movie = Movie.query.get(rental.movie_id)
        detailed_rentals.append((rental, user, movie))
    return detailed_rentals

# ✔ השכרות לפי משתמש כולל פרטי סרט (לפרופיל אישי)
def get_user_rentals_with_movie_details(user_id):
    """
    מחזיר רשימה של זוגות (Rental, Movie) לפי מזהה משתמש
    """
    return db.session.query(Rental, Movie) \
        .join(Movie, Rental.movie_id == Movie.movie_id) \
        .filter(Rental.user_id == user_id) \
        .order_by(Rental.rent_date.desc()) \
        .all()
