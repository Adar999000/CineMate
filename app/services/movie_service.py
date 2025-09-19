from app.models import Movie
from app import db
from collections import Counter

def get_all_movies():
    return Movie.query.all()

def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)

def update_movie(movie_id, **kwargs):
    movie = Movie.query.get(movie_id)
    if not movie:
        return None
        
    if 'year' in kwargs:
        kwargs['year'] = int(kwargs['year'])
        
    for key, value in kwargs.items():
        setattr(movie, key, value)
    
    try:
        db.session.commit()
        return movie
    except Exception as e:
        db.session.rollback()
        raise e

def get_recommended_movies(user_id, limit=3):
    """מקבל המלצות סרטים מותאמות אישית למשתמש לפי תגיות"""
    from app.services.rental_service import get_user_rentals_with_movie_details
    from collections import Counter
    
    # קבלת סרטים מושכרים של המשתמש
    rentals = get_user_rentals_with_movie_details(user_id)
    rented_movies = [movie for rental, movie in rentals]
    
    # אם אין היסטוריה, החזר רשימה ריקה
    if not rented_movies:
        return []
    
    # איסוף תגיות המשתמש
    user_movie_tags = []
    for rental, movie in rentals:
        if movie.tags:
            user_movie_tags.extend(tag.strip() for tag in movie.tags.split(','))
    
    # ספירת תדירות תגיות
    tag_counter = Counter(user_movie_tags)
    if not tag_counter:
        return []
    
    # קבלת סרטים זמינים שאינם מושכרים
    rented_movie_ids = {movie.movie_id for _, movie in rentals}
    all_movies = get_all_movies() or []
    available_movies = [movie for movie in all_movies if movie.movie_id not in rented_movie_ids]
    
    # דירוג סרטים לפי התאמה לתגיות
    movie_scores = []
    for movie in available_movies:
        if not movie.tags:
            continue
            
        movie_tags = [tag.strip() for tag in movie.tags.split(',')]
        score = sum(tag_counter[tag] for tag in movie_tags if tag in tag_counter)
        if score > 0:
            movie_scores.append((score, movie.movie_id, movie))
    
    # מיון והחזרת הסרטים המתאימים ביותר
    recommended = [movie for _, _, movie in sorted(movie_scores, reverse=True)][:limit]
    
    return [
        {
            'movie_id': movie.movie_id,
            'title': movie.title,
            'genre': movie.genre,
            'year': movie.year,
            'poster_url': movie.poster_url,
            'recommendation_rank': i,
            'tags': movie.tags
        }
        for i, movie in enumerate(recommended, 1)
    ]

def get_available_movies(user_id):
    """מחזיר רשימת סרטים שהמשתמש לא שכר עדיין"""
    from app.services.rental_service import get_user_rentals_with_movie_details
    
    rentals = get_user_rentals_with_movie_details(user_id)
    rented_ids = [movie.movie_id for rental, movie in rentals]
    all_movies = get_all_movies() or []
    
    return [
        {
            'movie_id': movie.movie_id,
            'title': movie.title,
            'genre': movie.genre,
            'year': movie.year,
            'poster_url': movie.poster_url
        }
        for movie in all_movies
        if movie.movie_id not in rented_ids
    ]
