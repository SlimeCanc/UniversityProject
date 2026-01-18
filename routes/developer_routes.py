from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from models.movie import db, Movie
from services.tmdb_service import tmdb_service
from services.streaming_service import streaming_service
from config import Config


# Декоратор для проверки авторизации разработчика
def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('developer_logged_in'):
            flash('Требуется авторизация разработчика', 'error')
            return redirect(url_for('developer.developer_login'))
        return f(*args, **kwargs)

    return decorated_function


developer_bp = Blueprint('developer', __name__)


@developer_bp.route('/login', methods=['GET', 'POST'])
def developer_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == Config.DEVELOPER_PASSWORD:
            session['developer_logged_in'] = True
            flash('Успешный вход в панель разработчика', 'success')
            return redirect(url_for('developer.developer_panel'))
        else:
            flash('Неверный пароль', 'error')

    return render_template('login.html')


@developer_bp.route('/logout')
def developer_logout():
    session.pop('developer_logged_in', None)
    flash('Вы вышли из панели разработчика', 'info')
    return redirect(url_for('main.index'))


@developer_bp.route('/')
@developer_required
def developer_panel():
    total_movies = Movie.query.count()
    recent_movies = Movie.query.order_by(Movie.id.desc()).limit(5).all()

    return render_template('panel.html',
                           total_movies=total_movies,
                           recent_movies=recent_movies)


@developer_bp.route('/movies')
@developer_required
def movies_list():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.order_by(Movie.title).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('movies_list.html', movies=movies)


@developer_bp.route('/add', methods=['GET', 'POST'])
@developer_required
def add_movie():
    if request.method == 'POST':
        try:
            movie = Movie(
                title=request.form['title'],
                year=int(request.form['year']),
                genre=request.form['genre'],
                rating=float(request.form['rating']),
                duration=request.form.get('duration', ''),
                type=request.form['type'],
                description=request.form.get('description', ''),
                image_url=request.form.get('image_url', '')
            )

            # Обработка стриминговых платформ
            movie.netflix_available = bool(request.form.get('netflix_available'))
            movie.amazon_available = bool(request.form.get('amazon_available'))
            movie.disney_available = bool(request.form.get('disney_available'))
            movie.hbo_available = bool(request.form.get('hbo_available'))
            movie.apple_available = bool(request.form.get('apple_available'))
            movie.hulu_available = bool(request.form.get('hulu_available'))

            db.session.add(movie)
            db.session.commit()

            flash(f'Фильм "{movie.title}" успешно добавлен!', 'success')
            return redirect(url_for('developer.movies_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении фильма: {str(e)}', 'error')

    return render_template('add_movie.html')


@developer_bp.route('/delete/<int:movie_id>', methods=['POST'])
@developer_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    try:
        db.session.delete(movie)
        db.session.commit()
        flash(f'Фильм "{movie.title}" удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении фильма: {str(e)}', 'error')

    return redirect(url_for('developer.movies_list'))


@developer_bp.route('/import/tmdb')
@developer_required
def import_from_tmdb():
    # Простая форма для импорта из TMDB
    return render_template('tmdb_import.html')