import requests
import os
from typing import List, Dict, Optional


class TMDBService:
    def __init__(self):
        self.api_key = os.environ.get('TMDB_API_KEY', 'your-tmdb-api-key-here')
        self.base_url = "https://api.themoviedb.org/3"
        self.language = "ru-RU"

    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """Поиск фильмов в TMDB"""
        url = f"{self.base_url}/search/multi"
        params = {
            'api_key': self.api_key,
            'query': query,
            'language': self.language,
            'page': page,
            'include_adult': False
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB Search Error: {e}")
            return None

    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """Получение популярных фильмов"""
        url = f"{self.base_url}/movie/popular"
        params = {
            'api_key': self.api_key,
            'language': self.language,
            'page': page,
            'region': 'RU'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB Popular Movies Error: {e}")
            return None

    def get_popular_tv_shows(self, page: int = 1) -> Optional[Dict]:
        """Получение популярных сериалов"""
        url = f"{self.base_url}/tv/popular"
        params = {
            'api_key': self.api_key,
            'language': self.language,
            'page': page
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB Popular TV Error: {e}")
            return None

    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Получение детальной информации о фильме"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'api_key': self.api_key,
            'language': self.language,
            'append_to_response': 'credits,release_dates'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB Movie Details Error: {e}")
            return None

    def get_tv_details(self, tv_id: int) -> Optional[Dict]:
        """Получение детальной информации о сериале"""
        url = f"{self.base_url}/tv/{tv_id}"
        params = {
            'api_key': self.api_key,
            'language': self.language,
            'append_to_response': 'credits,content_ratings'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB TV Details Error: {e}")
            return None

    def format_movie_data(self, movie_data: Dict) -> Dict:
        """Форматирование данных фильма для нашей базы"""
        return {
            'title': movie_data.get('title', ''),
            'year': int(movie_data.get('release_date', '0000')[:4]) if movie_data.get('release_date') else 0000,
            'genre': ', '.join([genre['name'] for genre in movie_data.get('genres', [])]),
            'rating': round(movie_data.get('vote_average', 0), 1),
            'duration': f"{movie_data.get('runtime', 0)} мин",
            'type': 'movie',
            'description': movie_data.get('overview', ''),
            'image_url': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}" if movie_data.get(
                'poster_path') else None
        }

    def format_tv_data(self, tv_data: Dict) -> Dict:
        """Форматирование данных сериала для нашей базы"""
        return {
            'title': tv_data.get('name', ''),
            'year': int(tv_data.get('first_air_date', '0000')[:4]) if tv_data.get('first_air_date') else 0000,
            'genre': ', '.join([genre['name'] for genre in tv_data.get('genres', [])]),
            'rating': round(tv_data.get('vote_average', 0), 1),
            'duration': f"{tv_data.get('number_of_seasons', 1)} сезон(ов)",
            'type': 'series',
            'description': tv_data.get('overview', ''),
            'image_url': f"https://image.tmdb.org/t/p/w500{tv_data.get('poster_path', '')}" if tv_data.get(
                'poster_path') else None
        }


# Глобальный экземпляр сервиса
tmdb_service = TMDBService()