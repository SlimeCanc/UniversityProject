from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50))
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))

    netflix_available = db.Column(db.Boolean, default=False)
    amazon_available = db.Column(db.Boolean, default=False)
    disney_available = db.Column(db.Boolean, default=False)
    hbo_available = db.Column(db.Boolean, default=False)
    apple_available = db.Column(db.Boolean, default=False)
    hulu_available = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'rating': self.rating,
            'duration': self.duration,
            'type': self.type,
            'description': self.description,
            'image_url': self.image_url,
            'streaming_platforms': {
                'netflix': self.netflix_available,
                'amazon': self.amazon_available,
                'disney': self.disney_available,
                'hbo': self.hbo_available,
                'apple': self.apple_available,
                'hulu': self.hulu_available
            }
        }

    def update_streaming_info(self, streaming_data):
        self.netflix_available = streaming_data.get('netflix', False)
        self.amazon_available = streaming_data.get('amazon', False)
        self.disney_available = streaming_data.get('disney', False)
        self.hbo_available = streaming_data.get('hbo', False)
        self.apple_available = streaming_data.get('apple', False)
        self.hulu_available = streaming_data.get('hulu', False)

    def __repr__(self):
        return f"<Movie {self.title} ({self.year})>"