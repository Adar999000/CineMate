# ============================================
# ================= יבואים ===================
# ============================================

# ----- Flask ומודולים בסיסיים -----
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import time
from sqlalchemy import text

# ----- שירותים ומודלים -----
from app.services.user_service import (
    get_user_by_id, get_all_users, get_user_by_email_password,
    create_new_user, user_exists, get_user_by_email, update_user_by_admin
)
from app.services.movie_service import get_movie_by_id, get_all_movies, get_recommended_movies, get_available_movies
from app.services.rental_service import (
    create_rental, get_all_rentals_with_details, get_user_rentals_with_movie_details
)
from app.services.ai_service import MovieChatbot
from app.models import Rental, ContactSubmission, Movie, User

# ----- מערכת מיילים -----
from flask_mail import Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.email_utils import send_email

# ----- צ'אטבוט ושירותים נוספים -----
from . import mail, db, login_manager

# יצירת מופע גלובלי של הצ'אטבוט
chatbot = MovieChatbot()

bp = Blueprint('main', __name__)

# ============================================
# ========= ניהול משתמשים ואימות ===========
# ============================================

# ----- טעינת משתמש -----
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# ----- התחברות והרשמה -----
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email_password(email, password)
        if user:
            login_user(user)
            flash('התחברת בהצלחה!', 'success')
            if user.type == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('פרטי התחברות שגויים.', 'danger')
    return render_template('auth/login.html', hide_navbar=True, user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if user_exists(email):
            flash('האימייל כבר רשום במערכת.', 'danger')
            return redirect(url_for('main.register'))

        user = create_new_user(first_name, last_name, email, password)
        login_user(user)
        flash('נרשמת בהצלחה!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('auth/register.html', hide_navbar=True, user=current_user)

# ----- ניהול סיסמאות ויציאה -----
@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = get_user_by_email(email)

        if user:
            send_password_email(user.email, user.password)
            flash('📧הססמא נשלחה למייל שלך!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('❌ האימייל שהוזן אינו רשום במערכת.', 'danger')
            return redirect(url_for('main.forgot_password'))

    return render_template('auth/forgot_password.html', hide_navbar=True, user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('התנתקת בהצלחה!', 'info')
    return redirect(url_for('main.index'))

# ============================================
# ============= דפי משתמש ===================
# ============================================

# ----- דפים ראשיים -----
@bp.route('/')
def index():
    return render_template("public/home_page.html", hide_navbar=True, user=current_user)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.type == 'admin':
        rentals = get_all_rentals_with_details()
        return render_template('admin/dashboard_admin.html', rentals=rentals, user=current_user)
    
    user = get_user_by_id(current_user.user_id)
    rentals = get_user_rentals_with_movie_details(user.user_id)
    
    return render_template('user/dashboard_user.html',
                         user=current_user,
                         rentals=rentals,
                         available_movies=get_available_movies(user.user_id),
                         recommended_movies=get_recommended_movies(user.user_id))

# ----- ניהול פרופיל -----
@bp.route('/profile')
@login_required
def profile():
    user = get_user_by_id(current_user.user_id)

    if request.method == 'POST' and 'profile_image' in request.files:
        image = request.files['profile_image']
        if image and image.filename != '':
            filename = secure_filename(f"user_{user.user_id}.png")
            upload_path = os.path.join(current_app.root_path, 'static', 'profile_images', filename)
            image.save(upload_path)
            flash("תמונת הפרופיל עודכנה בהצלחה", "success")
        return redirect(url_for('main.profile'))

    rentals = get_user_rentals_with_movie_details(user.user_id)

    return render_template("user/profile.html", user=current_user, rentals=rentals)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = get_user_by_id(current_user.user_id)

    if request.method == 'POST':
        # עדכון שדות רק אם קיימים בטופס
        if request.form.get('first_name'):
            user.first_name = request.form.get('first_name')
        if request.form.get('last_name'):
            user.last_name = request.form.get('last_name')
        if request.form.get('email'):
            user.email = request.form.get('email')
        if request.form.get('password'):
            user.password = request.form.get('password')

        # טיפול בהעלאת תמונת פרופיל
        image = request.files.get('profile_image')
        if image and image.filename != '':
            filename = secure_filename(f"user_{user.user_id}.png")
            upload_path = os.path.join(current_app.root_path, 'static', 'profile_images', filename)
            image.save(upload_path)

        db.session.commit()
        flash("הפרופיל עודכן בהצלחה!", "success")
        return redirect(url_for('main.profile'))

    return render_template('user/edit_profile.html', user=current_user, edit_user=user)

# ============================================
# ============ ניהול סרטים =================
# ============================================

# ----- צפייה בסרטים -----
@bp.route('/all-movies')
@login_required
def all_movies():
    all_movies = get_all_movies()
    rentals = get_user_rentals_with_movie_details(current_user.user_id)
    rented_ids = [movie.movie_id for rental, movie in rentals]
    available_movies = [m for m in all_movies if m.movie_id not in rented_ids]
    return render_template("user/all_movies.html", movies=available_movies, user=current_user)

@bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return render_template('errors/error_404.html'), 404
    return render_template('user/movie_details.html', movie=movie, user=current_user)

# ----- המלצות סרטים -----
@bp.route('/recommended')
@login_required
def recommended_movies():
    return render_template("user/recommended_movies.html", user=current_user)

# ============================================
# =========== ניהול השכרות ================
# ============================================

# ----- פעולות השכרה -----
@bp.route('/rent/<int:movie_id>', methods=['POST'])
@login_required
def rent_movie(movie_id):
    try:
        create_rental(current_user.user_id, movie_id)
        flash('השכרה בוצעה בהצלחה!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'שגיאה בביצוע השכרה: {e}', 'danger')
    return redirect(url_for('main.dashboard'))

# ----- צפייה בהשכרות -----
@bp.route('/my-rentals')
@login_required
def my_rentals():
    rentals = get_user_rentals_with_movie_details(current_user.user_id)
    return render_template("user/my_rentals.html", rentals=rentals, user=current_user)

# ----- ביטול השכרות -----
@bp.route('/rentals/delete/<int:rental_id>', methods=['POST'])
@login_required
def delete_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    
    if rental.user_id != current_user.user_id and current_user.type != 'admin':
        return 'Unauthorized', 403
        
    try:
        # Get next rental before deleting
        next_rental = None
        if current_user.type == 'admin':
            next_rental = Rental.query.filter(Rental.rental_id > rental_id).order_by(Rental.rental_id.asc()).first()
            if next_rental:
                user = User.query.get(next_rental.user_id)
                movie = Movie.query.get(next_rental.movie_id)
                if user and movie:
                    next_rental_data = {
                        'rental_id': next_rental.rental_id,
                        'user_name': f'{user.first_name} {user.last_name}',
                        'email': user.email,
                        'movie_id': movie.movie_id,
                        'movie_title': movie.title,
                        'movie_genre': movie.genre,
                        'movie_year': movie.year,
                        'movie_poster': movie.poster_url,
                        'rent_date': next_rental.rent_date.strftime('%Y-%m-%d')
                    }

        db.session.delete(rental)
        db.session.commit()
        
        if current_user.type == 'admin' and next_rental:
            return jsonify(next_rental_data), 200
        return '', 204
    except Exception as e:
        db.session.rollback()
        return str(e), 500

# ============================================
# ============ ממשק מנהל ==================
# ============================================

# ----- דשבורד מנהל -----
@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    rentals = get_all_rentals_with_details()
    return render_template("admin/dashboard_admin.html", rentals=rentals, user=current_user)

# ----- ניהול משתמשים -----
@bp.route('/admin/users')
@login_required
def admin_users_list():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    users = get_all_users()
    return render_template("admin/admin_users_list.html", users=users, user=current_user)

@bp.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    user = get_user_by_id(user_id)
    if not user:
        flash("משתמש לא נמצא", "danger")
        return redirect(url_for('main.admin_users_list'))

    if request.method == 'POST':
        
        if 'send_email' in request.form:
            try:
                subject = "📧 הסיסמה שלך למערכת CineMate"
                body = f"""
שלום {user.first_name},

כפי שביקשת, הסיסמה שלך למערכת CineMate היא:
    
🔐 סיסמה: {user.password}

אם לא ביקשת זאת, ניתן להתעלם מהודעה זו.

בברכה,
צוות CineMate 🎬
"""
                msg = Message(
                    subject=subject,
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[user.email],
                    body=body
                )
                current_app.logger.info(f"Attempting to send email to {user.email}")
                mail.send(msg)
                current_app.logger.info("Email sent successfully")
                flash("הסיסמה נשלחה למייל של המשתמש.", "success")
            except Exception as e:
                current_app.logger.error(f"Failed to send email: {str(e)}")
                flash(f"שגיאה בשליחת המייל: {str(e)}", "danger")
            return redirect(url_for('main.admin_users_list'))
        
        # אם זו בקשה לעדכון פרטי המשתמש
        else:
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email']
            user.password = request.form['password']
            db.session.commit()
            flash("המשתמש עודכן בהצלחה!", "success")
            return redirect(url_for('main.admin_users_list'))

    return render_template("admin/admin_edit_user.html", user=current_user, edit_user=user)

@bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    user = get_user_by_id(user_id)
    if not user:
        flash('משתמש לא נמצא', 'danger')
        return redirect(url_for('main.admin_users_list'))

    db.session.delete(user)
    db.session.commit()
    flash('המשתמש נמחק בהצלחה', 'success')
    return redirect(url_for('main.admin_users_list'))

# ----- ניהול סרטים -----
@bp.route('/admin/movies')
@login_required
def admin_edit_movies():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))

    movies = get_all_movies()
    return render_template("admin/admin_edit_movies.html", movies=movies, user=current_user)

@bp.route('/admin/movies/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        genre = request.form['genre']
        description = request.form['description']
        tags = request.form['tags']
        poster_url = request.form['poster_url']

        # יצירת סרט חדש
        movie = Movie(
            title=title,
            year=year,
            genre=genre,
            description=description,
            tags=tags,
            poster_url=poster_url
        )
        db.session.add(movie)
        db.session.commit()
        flash('🎬 הסרט נוסף בהצלחה!', 'success')
        return redirect(url_for('main.admin_edit_movies'))

    return render_template('admin/add_movie.html', user=current_user)

@bp.route('/admin/movies/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('סרט לא נמצא.', 'danger')
        return redirect(url_for('main.admin_edit_movies'))

    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = int(request.form['year'])
        movie.genre = request.form['genre']
        movie.description = request.form['description']
        movie.tags = request.form['tags']
        
        # Handle poster URL
        poster_url = request.form.get('poster_url')
        if poster_url:
            movie.poster_url = poster_url

        try:
            db.session.commit()
            flash('🎬 הסרט עודכן בהצלחה!', 'success')
            return redirect(url_for('main.admin_edit_movies'))
        except Exception as e:
            db.session.rollback()
            flash(f'שגיאה בעדכון הסרט: {str(e)}', 'danger')
            return render_template('admin/edit_movie.html', movie=movie, user=current_user)

    return render_template('admin/edit_movie.html', movie=movie, user=current_user)

@bp.route('/admin/movies/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))
    
    movie = get_movie_by_id(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash('🎬 הסרט נמחק בהצלחה!', 'success')
    else:
        flash('הסרט לא נמצא.', 'danger')

    return redirect(url_for('main.admin_edit_movies'))

# ----- ניהול השכרות -----
@bp.route('/admin/rentals')
@login_required
def admin_rentals():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה", "danger")
        return redirect(url_for('main.index'))

    rentals = get_all_rentals_with_details()
    return render_template("admin/admin_rentals.html", rentals=rentals, user=current_user)

# ----- ניהול פניות -----
@bp.route('/admin/submissions')
@login_required
def admin_submissions():
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה.", "danger")
        return redirect(url_for('main.index'))
    
    submissions = ContactSubmission.query.order_by(ContactSubmission.timestamp.desc()).all()
    return render_template('admin/admin_submissions.html', submissions=submissions, user=current_user)

@bp.route('/admin/submission/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def admin_view_submission(submission_id):
    if current_user.type != 'admin':
        flash("אין לך הרשאה לגשת לדף זה.", "danger")
        return redirect(url_for('main.index'))

    submission = ContactSubmission.query.get_or_404(submission_id)

    # Mark as read when viewed
    if submission.is_new:
        submission.is_new = False
        db.session.commit()

    if request.method == 'POST':
        response_subject = request.form.get('response_subject')
        response_body = request.form.get('response_body')
        
        email_body = f"""שלום רב, בהמשך לפנייתך: 

{response_body}

בברכה,
צוות CineMate 🎬"""

        try:
            msg = Message(
                subject=response_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[submission.email],
                body=email_body
            )
            mail.send(msg)
            submission.response_sent = True
            db.session.commit()
            flash("התגובה נשלחה בהצלחה למשתמש.", "success")
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            flash("אירעה שגיאה בשליחת המייל. אנא נסה שוב מאוחר יותר.", "danger")
        return redirect(url_for('main.admin_submissions'))

    return render_template('admin/admin_view_submission.html', submission=submission, user=current_user)

@bp.route('/admin/delete_submission/<int:submission_id>', methods=['DELETE'])
@login_required
def delete_submission(submission_id):
    if current_user.type != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    submission = ContactSubmission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    return '', 204

# ============================================
# =========== דפים ציבוריים ===============
# ============================================

# ----- דפי מידע -----
@bp.route('/faq')
def faq():
    return render_template('public/faq.html', user=current_user)

# ----- יצירת קשר -----
@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('אנא מלא את כל השדות בטופס.', 'danger')
            # Return the contact page with the form data to avoid losing user input
            return render_template('public/contact.html', form_data=request.form, user=current_user)

        try:
            new_submission = ContactSubmission(
                name=name,
                email=email,
                message=message
            )
            db.session.add(new_submission)
            db.session.commit()
            flash('הפנייה נשלחה בהצלחה! ניצור איתך קשר בהקדם.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving contact submission: {e}")
            flash('אירעה שגיאה בשליחת הפנייה. אנא נסה שוב מאוחר יותר.', 'danger')
            return render_template('public/contact.html', form_data=request.form, user=current_user)

    return render_template('public/contact.html', user=current_user)

# ============================================
# ========== טיפול בשגיאות ===============
# ============================================

# ----- שגיאות מערכת -----
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/error_404.html'), 404

@bp.app_errorhandler(500)
def internal_error(e):
    return render_template('errors/error_500.html'), 500

# ============================================
# ============== צ'אטבוט ==================
# ============================================

# ----- טיפול בבקשות צ'אט -----
@bp.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = chatbot.get_response(message)
        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Chat error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'מצטער, נתקלתי בשגיאה. אנא נסה שוב.',
            'time': time.strftime("%H:%M")
        }), 500

# ============================================
# =========== פונקציות עזר ===============
# ============================================

# ----- ספירת פניות חדשות -----
@bp.app_context_processor
def inject_new_submissions_count():
    if current_user.is_authenticated and current_user.type == 'admin':
        new_submissions_count = ContactSubmission.query.filter_by(is_new=True).count()
        return dict(new_submissions_count=new_submissions_count)
    return dict(new_submissions_count=0)

# ----- שליחת מיילים -----
def send_password_email(recipient_email, password):
    sender_email = os.environ.get('MAIL_USERNAME', 'adar04954@gmail.com')
    sender_password = os.environ.get('MAIL_PASSWORD', 'ehrf ajby ukoo djsj')

    subject = "CineMate – שחזור סיסמה"
    body = f"""
שלום,
    
לפי בקשתך, הסיסמה שלך למערכת CineMate היא:
    
🔐 סיסמה: {password}
    
אם לא ביקשת זאת, התעלם מהודעה זו.
    
בברכה,
צוות CineMate 🎬
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"❌ שגיאה בשליחת מייל: {e}")
        return False
    return True
