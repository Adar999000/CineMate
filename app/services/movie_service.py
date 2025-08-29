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

def get_recommended_movies_by_tags(user_rentals, limit=3):
    """
    מחזיר המלצות סרטים על בסיס תגיות מסרטים שהמשתמש צפה בהם
    """
    # מקבל את כל התגיות מסרטים שהמשתמש צפה בהם
    user_movie_tags = []
    for rental, movie in user_rentals:
        if movie.tags:
            user_movie_tags.extend(tag.strip() for tag in movie.tags.split(','))
    
    # מונה את התגיות הנפוצות ביותר
    tag_counter = Counter(user_movie_tags)
    if not tag_counter:
        return []
    
    # מקבל את כל הסרטים הזמינים שאינם הושכרו על ידי המשתמש
    rented_movie_ids = {movie.movie_id for _, movie in user_rentals}
    available_movies = Movie.query.filter(~Movie.movie_id.in_(rented_movie_ids)).all()
    
    # מדרג סרטים לפי התאמה לתגיות המועדפות
    movie_scores = []
    for movie in available_movies:
        if not movie.tags:
            continue
            
        movie_tags = [tag.strip() for tag in movie.tags.split(',')]
        score = sum(tag_counter[tag] for tag in movie_tags if tag in tag_counter)
        if score > 0:
            movie_scores.append((score, movie.movie_id, movie))
    
    # מחזיר את הסרטים המתאימים ביותר
    recommended = [movie for _, _, movie in sorted(movie_scores, reverse=True)][:limit]
    return recommended
