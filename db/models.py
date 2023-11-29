from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Movie:
    genres: str
    description: str
    rating_kp: float
    rating_imdb: float
    year: int
    post_image_url: str
    preview_url: str


@dataclass(frozen=True, slots=True)
class UserQuery:
    genre_name: str
    year: int
    rating: int
