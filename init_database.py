import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.movie import db, Movie
from services.streaming_service import streaming_service


def init_database():
    app = create_app()

    with app.app_context():
        db.create_all()

        # 20 фильмов и сериалов
        movies_data = [
            # Фильмы
            {
                "title": "Начало",
                "year": 2010,
                "genre": "Фантастика, Боевик, Триллер",
                "rating": 8.8,
                "duration": "148 мин",
                "type": "movie",
                "description": "Вор, крадущий корпоративные секреты с помощью технологии совместного использования снов, получает обратную задачу - внедрить идею в сознание генерального директора.",
                "image_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"
            },
            {
                "title": "Темный рыцарь",
                "year": 2008,
                "genre": "Боевик, Криминал, Драма",
                "rating": 9.0,
                "duration": "152 мин",
                "type": "movie",
                "description": "Когда угроза, известная как Джокер, сеет хаос и разрушение среди жителей Готэма, Бэтмен должен пройти одно из величайших психологических и физических испытаний.",
                "image_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
            },
            {
                "title": "Побег из Шоушенка",
                "year": 1994,
                "genre": "Драма",
                "rating": 9.3,
                "duration": "142 мин",
                "type": "movie",
                "description": "Два заключенных заводят дружбу на протяжении нескольких лет, находя утешение и eventual искупление через acts of common decency.",
                "image_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
            },
            {
                "title": "Крестный отец",
                "year": 1972,
                "genre": "Криминал, Драма",
                "rating": 9.2,
                "duration": "175 мин",
                "type": "movie",
                "description": "Стареющий патриарх organized crime dynasty передает контроль своего подпольной империи своему неохотному сыну.",
                "image_url": "https://image.tmdb.org/t/p/w500/3Tf8vXykYhzHdT0BtsYTp570JGQ.jpg"
            },
            {
                "title": "Форрест Гамп",
                "year": 1994,
                "genre": "Драма, Романтика",
                "rating": 8.8,
                "duration": "142 мин",
                "type": "movie",
                "description": "История жизни Форреста Гампа, добродушного и простодушного человека из Алабамы, который невольно оказывается вовлеченным в ключевые события истории США.",
                "image_url": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"
            },
            {
                "title": "Матрица",
                "year": 1999,
                "genre": "Боевик, Фантастика",
                "rating": 8.7,
                "duration": "136 мин",
                "type": "movie",
                "description": "Хакер по кличке Нео узнает шокирующую правду о реальности, и его роль в войне против ее controllers.",
                "image_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
            },
            {
                "title": "Криминальное чтиво",
                "year": 1994,
                "genre": "Криминал, Драма",
                "rating": 8.9,
                "duration": "154 мин",
                "type": "movie",
                "description": "Переплетающиеся истории двух гангстеров-убийц, боксера, гангстера и его жены, и пары грабителей ресторанов.",
                "image_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"
            },
            {
                "title": "Интерстеллар",
                "year": 2014,
                "genre": "Приключения, Драма, Фантастика",
                "rating": 8.6,
                "duration": "169 мин",
                "type": "movie",
                "description": "Команда исследователей путешествует через червоточину в космосе в попытке обеспечить выживание человечества.",
                "image_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
            },
            {
                "title": "Мстители: Финал",
                "year": 2019,
                "genre": "Боевик, Приключения, Фантастика",
                "rating": 8.4,
                "duration": "181 мин",
                "type": "movie",
                "description": "После опустошительных событий Войны Бесконечности Мстители снова собираются вместе, чтобы обратить вспять действия Таноса и восстановить баланс во вселенной.",
                "image_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
            },
            {
                "title": "Властелин колец: Братство кольца",
                "year": 2001,
                "genre": "Фэнтези, Приключения, Драма",
                "rating": 8.8,
                "duration": "178 мин",
                "type": "movie",
                "description": "Скромный хоббит из Шира и восемь спутников отправляются в путешествие, чтобы уничтожить могущественное кольцо и спасти Средиземье от Темного Лорда Саурона.",
                "image_url": "https://image.tmdb.org/t/p/w500/8HrWlc3etT04Wgc9VUcdVh1cVR.jpg"
            },

            # Сериалы
            {
                "title": "Очень странные дела",
                "year": 2016,
                "genre": "Драма, Фэнтези, Ужасы",
                "rating": 8.7,
                "duration": "4 сезона",
                "type": "series",
                "description": "Когда пропадает маленький мальчик, его мать, шеф полиции и друзья должны противостоять ужасающим сверхъестественным силам, чтобы вернуть его.",
                "image_url": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg"
            },
            {
                "title": "Игра престолов",
                "year": 2011,
                "genre": "Драма, Фэнтези, Приключения",
                "rating": 9.2,
                "duration": "8 сезонов",
                "type": "series",
                "description": "Девять знатных семей борются за контроль над землями Вестероса, пока древний враг возвращается после тысячелетнего покоя.",
                "image_url": "https://image.tmdb.org/t/p/w500/u3bZgnGQ9T01sWNhyveQz0wH0Hl.jpg"
            },
            {
                "title": "Во все тяжкие",
                "year": 2008,
                "genre": "Криминал, Драма, Триллер",
                "rating": 9.5,
                "duration": "5 сезонов",
                "type": "series",
                "description": "Учитель химии в старшей школе, у которого диагностировали неизлечимый рак легких, начинает производить и продавать метамфетамин, чтобы обеспечить будущее своей семьи.",
                "image_url": "https://image.tmdb.org/t/p/w500/3xnWaLQjelJDDF7LT1WBo6f4BRe.jpg"
            },
            {
                "title": "Мандалорец",
                "year": 2019,
                "genre": "Фантастика, Боевик, Приключения",
                "rating": 8.8,
                "duration": "3 сезона",
                "type": "series",
                "description": "Путешествия одинокого охотника за головами в отдаленных уголках галактики, вдали от власти Новой Республики.",
                "image_url": "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMOlEq0ku1Rzq7Y4wA.jpg"
            },
            {
                "title": "Ведьмак",
                "year": 2019,
                "genre": "Боевик, Приключения, Драма",
                "rating": 8.2,
                "duration": "3 сезона",
                "type": "series",
                "description": "Геральт из Ривии, мутировавший охотник на монстров, путешествует к своей судьбе в бурном мире, где люди часто оказываются более злыми, чем чудовища.",
                "image_url": "https://image.tmdb.org/t/p/w500/A6oF3KmUpWSWXoeh92K44sLM1t9.jpg"
            },
            {
                "title": "Ход королевы",
                "year": 2020,
                "genre": "Драма",
                "rating": 8.6,
                "duration": "1 сезон",
                "type": "series",
                "description": "Осиротев в нежном возрасте девяти лет, гениальная интровертка Бет Хармон открывает и осваивает игру в шахматы в США 1960-х годов.",
                "image_url": "https://image.tmdb.org/t/p/w500/zU0htwkhNvBQdVSIKB9s6hgVeFK.jpg"
            },
            {
                "title": "Дом Дракона",
                "year": 2022,
                "genre": "Фэнтези, Драма, Боевик",
                "rating": 8.5,
                "duration": "1 сезон",
                "type": "series",
                "description": "История семьи Таргариенов за 200 лет до событий 'Игры престолов'.",
                "image_url": "https://image.tmdb.org/t/p/w500/etj8E2o0Bud0HkONVQPjyCkIvpv.jpg"
            },
            {
                "title": "Локи",
                "year": 2021,
                "genre": "Фантастика, Боевик, Приключения",
                "rating": 8.2,
                "duration": "2 сезона",
                "type": "series",
                "description": "Бог хитрости Локи попадает в руки Управления временными изменениями после кражи Тессеракта.",
                "image_url": "https://image.tmdb.org/t/p/w500/voHUmluYmKyleFkTu3lOXQG702u.jpg"
            },
            {
                "title": "Корона",
                "year": 2016,
                "genre": "Драма, История",
                "rating": 8.6,
                "duration": "6 сезонов",
                "type": "series",
                "description": "История правления королевы Елизаветы II, от ее свадьбы в 1947 году до настоящего времени.",
                "image_url": "https://image.tmdb.org/t/p/w500/1H4WS2rI04iSX9gC6gYzZKb12hK.jpg"
            },
            {
                "title": "Наследники",
                "year": 2018,
                "genre": "Драма",
                "rating": 8.8,
                "duration": "4 сезона",
                "type": "series",
                "description": "История семьи Роу, владеющей одной из крупнейших медиа-империй в мире, и борьбы за контроль над компанией.",
                "image_url": "https://image.tmdb.org/t/p/w500/6U0eYfK1M2VKIXe0mJvnVP0g2cF.jpg"
            }
        ]

        print("🎬 Добавление фильмов и сериалов в базу данных...")
        added_count = 0

        for movie_data in movies_data:
            existing_movie = Movie.query.filter_by(
                title=movie_data['title'],
                year=movie_data['year']
            ).first()

            if not existing_movie:
                streaming_data = streaming_service.check_availability(
                    movie_data['title'], movie_data['year']
                )

                movie = Movie(
                    title=movie_data['title'],
                    year=movie_data['year'],
                    genre=movie_data['genre'],
                    rating=movie_data['rating'],
                    duration=movie_data['duration'],
                    type=movie_data['type'],
                    description=movie_data['description'],
                    image_url=movie_data['image_url']
                )
                movie.update_streaming_info(streaming_data)
                db.session.add(movie)
                added_count += 1
                print(f"✅ Добавлен: {movie.title} ({movie.year})")

        db.session.commit()

        # Статистика
        total_movies = Movie.query.filter_by(type='movie').count()
        total_series = Movie.query.filter_by(type='series').count()

        print(f"\n🎉 Инициализация базы данных завершена!")
        print(f"📊 Добавлено: {added_count} записей")
        print(f"🎞️ Фильмы: {total_movies}")
        print(f"📺 Сериалы: {total_series}")
        print(f"📈 Всего: {total_movies + total_series}")


if __name__ == '__main__':
    init_database()