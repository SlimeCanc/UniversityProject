from flask import Blueprint, render_template, request, jsonify
from models.movie import Movie
from sqlalchemy import or_, and_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Главная страница с популярными фильмами"""
    popular_movies = Movie.query.order_by(Movie.rating.desc()).limit(8).all()
    return render_template('index.html', popular_movies=popular_movies)


@main_bp.route('/search')
def search():
    """Страница поиска с фильтрами"""
    search_query = request.args.get('q', '').strip()
    genre_filter = request.args.get('genre', 'all')
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    min_rating = request.args.get('min_rating', type=float)
    content_type = request.args.get('type', 'all')
    streaming_platforms = request.args.getlist('streaming')

    # Базовый запрос
    query = Movie.query

    # Применяем фильтры
    if search_query:
        query = query.filter(Movie.title.ilike(f'%{search_query}%'))

    if genre_filter != 'all':
        query = query.filter(Movie.genre.ilike(f'%{genre_filter}%'))

    if year_from:
        query = query.filter(Movie.year >= year_from)

    if year_to:
        query = query.filter(Movie.year <= year_to)

    if min_rating:
        query = query.filter(Movie.rating >= min_rating)

    if content_type != 'all':
        query = query.filter(Movie.type == content_type)

    if streaming_platforms:
        platform_filters = []
        if 'netflix' in streaming_platforms:
            platform_filters.append(Movie.netflix_available == True)
        if 'amazon' in streaming_platforms:
            platform_filters.append(Movie.amazon_available == True)
        if 'disney' in streaming_platforms:
            platform_filters.append(Movie.disney_available == True)
        if 'hbo' in streaming_platforms:
            platform_filters.append(Movie.hbo_available == True)

        if platform_filters:
            query = query.filter(or_(*platform_filters))

    movies = query.order_by(Movie.rating.desc()).all()
    total_results = len(movies)

    return render_template('search_results.html',
                           movies=movies,
                           search_query=search_query,
                           total_results=total_results)


@main_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Страница с полным описанием фильма/сериала"""
    movie = Movie.query.get_or_404(movie_id)

    # Находим похожие фильмы/сериалы (по жанру и типу)
    similar_movies = Movie.query.filter(
        Movie.id != movie_id,
        Movie.type == movie.type
    ).filter(
        or_(
            *[Movie.genre.like(f'%{genre.strip()}%') for genre in movie.genre.split(',')]
        )
    ).order_by(Movie.rating.desc()).limit(6).all()

    # Если похожих мало, добавляем случайные того же типа
    if len(similar_movies) < 4:
        additional_movies = Movie.query.filter(
            Movie.id != movie_id,
            Movie.type == movie.type,
            ~Movie.id.in_([m.id for m in similar_movies])
        ).order_by(Movie.rating.desc()).limit(6 - len(similar_movies)).all()
        similar_movies.extend(additional_movies)

    return render_template('movie_detail.html',
                           movie=movie,
                           similar_movies=similar_movies)


@main_bp.route('/api/search_suggestions')
def search_suggestions():
    """API для автодополнения поиска"""
    query = request.args.get('q', '').strip()

    if len(query) < 2:
        return jsonify([])

    suggestions = Movie.query.filter(
        Movie.title.ilike(f'%{query}%')
    ).order_by(Movie.rating.desc()).limit(8).all()

    result = []
    for movie in suggestions:
        result.append({
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'genre': movie.genre,
            'rating': movie.rating,
            'type': movie.type,
            'image_url': movie.image_url
        })

    return jsonify(result)


@main_bp.route('/api/check_streaming/<int:movie_id>')
def check_streaming(movie_id):
    """API для проверки доступности на стриминговых платформах"""
    movie = Movie.query.get_or_404(movie_id)

    try:
        from services.streaming_service import streaming_service
        streaming_data = streaming_service.check_availability(movie.title, movie.year)
        movie.update_streaming_info(streaming_data)

        db.session.commit()

        return jsonify({
            'success': True,
            'title': movie.title,
            'streaming_platforms': {
                'netflix': movie.netflix_available,
                'amazon': movie.amazon_available,
                'disney': movie.disney_available,
                'hbo': movie.hbo_available,
                'apple': movie.apple_available,
                'hulu': movie.hulu_available
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500