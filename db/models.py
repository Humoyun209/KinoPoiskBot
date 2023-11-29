from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Movie:
    name: str
    alternativeName: str | None
    genres: list[str]
    description: str | None
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
