import os
import sys
import time
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.movie import db, Movie
from services.tmdb_service import tmdb_service
from services.streaming_service import streaming_service


class AutoImporter:
    def __init__(self):
        self.app = create_app()
        self.added_count = 0
        self.skipped_count = 0

    def import_popular_content(self, movies_count: int = 20, tv_count: int = 10):
        """Автоматически импортирует популярные фильмы и сериалы"""
        print("🎬 Начинаем автоматический импорт популярного контента...")

        with self.app.app_context():
            # Импортируем популярные фильмы
            print("\n📽️ Импортируем популярные фильмы...")
            self.import_popular_movies(movies_count)

            # Импортируем популярные сериалы
            print("\n📺 Импортируем популярные сериалы...")
            self.import_popular_tv_shows(tv_count)

            # Статистика
            total_movies = Movie.query.filter_by(type='movie').count()
            total_series = Movie.query.filter_by(type='series').count()

            print(f"\n🎉 Автоматический импорт завершен!")
            print(f"✅ Добавлено: {self.added_count} записей")
            print(f"⏭️ Пропущено (уже есть): {self.skipped_count} записей")
            print(f"📊 Всего в базе: {total_movies + total_series} записей")
            print(f"🎞️ Фильмы: {total_movies}")
            print(f"📺 Сериалы: {total_series}")

    def import_popular_movies(self, count: int):
        """Импортирует популярные фильмы"""
        page = 1

        while self.added_count < count:
            print(f"📄 Загружаем страницу {page} популярных фильмов...")
            data = tmdb_service.get_popular_movies(page)

            if not data or 'results' not in data:
                print("❌ Не удалось загрузить данные о фильмах")
                break

            movies = data['results']
            if not movies:
                print("ℹ️ Больше фильмов нет")
                break

            for movie_data in movies:
                if self.added_count >= count:
                    break

                # Получаем детальную информацию
                details = tmdb_service.get_movie_details(movie_data['id'])
                if not details:
                    continue

                # Форматируем данные
                movie_info = tmdb_service.format_movie_data(details)

                # Пропускаем если нет основных данных
                if not movie_info['title'] or not movie_info['year']:
                    continue

                # Проверяем, не существует ли уже
                existing_movie = Movie.query.filter_by(
                    title=movie_info['title'],
                    year=movie_info['year']
                ).first()

                if existing_movie:
                    print(f"⏭️ Уже есть: {movie_info['title']} ({movie_info['year']})")
                    self.skipped_count += 1
                    continue

                # Проверяем доступность на стриминговых платформах
                streaming_data = streaming_service.check_availability(
                    movie_info['title'], movie_info['year']
                )

                # Создаем фильм
                movie = Movie(
                    title=movie_info['title'],
                    year=movie_info['year'],
                    genre=movie_info['genre'],
                    rating=movie_info['rating'],
                    duration=movie_info['duration'],
                    type=movie_info['type'],
                    description=movie_info['description'],
                    image_url=movie_info['image_url']
                )

                # Обновляем информацию о стриминге
                movie.update_streaming_info(streaming_data)

                db.session.add(movie)
                self.added_count += 1
                print(f"✅ Добавлен: {movie.title} ({movie.year})")

                # Небольшая задержка чтобы не перегружать API
                time.sleep(0.5)

            page += 1
            time.sleep(1)  # Задержка между страницами

    def import_popular_tv_shows(self, count: int):
        """Импортирует популярные сериалы"""
        page = 1
        tv_added = 0

        while tv_added < count:
            print(f"📄 Загружаем страницу {page} популярных сериалов...")
            data = tmdb_service.get_popular_tv_shows(page)

            if not data or 'results' not in data:
                print("❌ Не удалось загрузить данные о сериалах")
                break

            tv_shows = data['results']
            if not tv_shows:
                print("ℹ️ Больше сериалов нет")
                break

            for tv_data in tv_shows:
                if tv_added >= count:
                    break

                # Получаем детальную информацию
                details = tmdb_service.get_tv_details(tv_data['id'])
                if not details:
                    continue

                # Форматируем данные
                tv_info = tmdb_service.format_tv_data(details)

                # Пропускаем если нет основных данных
                if not tv_info['title'] or not tv_info['year']:
                    continue

                # Проверяем, не существует ли уже
                existing_tv = Movie.query.filter_by(
                    title=tv_info['title'],
                    year=tv_info['year']
                ).first()

                if existing_tv:
                    print(f"⏭️ Уже есть: {tv_info['title']} ({tv_info['year']})")
                    self.skipped_count += 1
                    continue

                # Проверяем доступность на стриминговых платформах
                streaming_data = streaming_service.check_availability(
                    tv_info['title'], tv_info['year']
                )

                # Создаем сериал
                tv_show = Movie(
                    title=tv_info['title'],
                    year=tv_info['year'],
                    genre=tv_info['genre'],
                    rating=tv_info['rating'],
                    duration=tv_info['duration'],
                    type=tv_info['type'],
                    description=tv_info['description'],
                    image_url=tv_info['image_url']
                )

                # Обновляем информацию о стриминге
                tv_show.update_streaming_info(streaming_data)

                db.session.add(tv_show)
                self.added_count += 1
                tv_added += 1
                print(f"✅ Добавлен: {tv_show.title} ({tv_show.year})")

                # Небольшая задержка чтобы не перегружать API
                time.sleep(0.5)

            page += 1
            time.sleep(1)  # Задержка между страницами

    def search_and_import(self, query: str):
        """Ищет и импортирует контент по запросу"""
        print(f"🔍 Ищем и импортируем: {query}")

        with self.app.app_context():
            data = tmdb_service.search_movies(query)

            if not data or 'results' not in data:
                print("❌ Ничего не найдено")
                return

            for item in data['results']:
                # Определяем тип контента
                if item['media_type'] == 'movie':
                    details = tmdb_service.get_movie_details(item['id'])
                    if details:
                        movie_info = tmdb_service.format_movie_data(details)
                        self._import_item(movie_info)

                elif item['media_type'] == 'tv':
                    details = tmdb_service.get_tv_details(item['id'])
                    if details:
                        tv_info = tmdb_service.format_tv_data(details)
                        self._import_item(tv_info)

                time.sleep(0.5)

    def _import_item(self, item_info: Dict):
        """Импортирует один элемент"""
        # Проверяем, не существует ли уже
        existing_item = Movie.query.filter_by(
            title=item_info['title'],
            year=item_info['year']
        ).first()

        if existing_item:
            print(f"⏭️ Уже есть: {item_info['title']} ({item_info['year']})")
            self.skipped_count += 1
            return

        # Проверяем доступность на стриминговых платформах
        streaming_data = streaming_service.check_availability(
            item_info['title'], item_info['year']
        )

        # Создаем элемент
        item = Movie(
            title=item_info['title'],
            year=item_info['year'],
            genre=item_info['genre'],
            rating=item_info['rating'],
            duration=item_info['duration'],
            type=item_info['type'],
            description=item_info['description'],
            image_url=item_info['image_url']
        )

        # Обновляем информацию о стриминге
        item.update_streaming_info(streaming_data)

        db.session.add(item)
        self.added_count += 1
        print(f"✅ Добавлен: {item.title} ({item.year})")

        db.session.commit()


def main():
    importer = AutoImporter()

    print("🚀 Автоматический импорт контента из TMDB")
    print("=" * 50)

    # Импортируем популярный контент
    importer.import_popular_content(movies_count=15, tv_count=10)

    # Можно также добавить поиск конкретных фильмов
    # importer.search_and_import("Мстители")
    # importer.search_and_import("Игра престолов")


if __name__ == '__main__':
    main()