import os
import json
from typing import Mapping
import aiohttp

from PIL import Image

from db.models import Movie


class KinoPoiskAPI:
    def __init__(self, token: str) -> None:
        self.url = 'https://api.kinopoisk.dev/v1.4/'
        self.headers = {
            'Accept': '*/*',
            'mode': 'sane-origin',
            'X-API-KEY': token
        }
        self.session = None

    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def search_movie(self, genre: str, year: int):
        session = await self.get_session()
        url = f'{self.url}movie?limit=5&rating.kp=8.5-10&year={year}&genres.name={genre}'
        
        async with session.get(url, headers=self.headers) as response:
            result = await response.json()
            with open(f'app/mock/{genre}_{year}.json', 'w') as f:
                json.dump(result, f, indent=2)
            return self.get_result(result)

    async def download_image(self, url: str, query: str):
        session = await self.get_session()
        if url[-4:] == '.jpg':
            movie_id = url.split(".")[-2].split('/')[-1]
        else:
            movie_id = url.split("/")[-2]
        file_path = f'app/images/{query}/{movie_id}.jpg'
        
        if not os.path.exists(f'app/images/{query}'):
            os.makedirs(f'app/images/{query}')
        if not os.path.isfile(file_path):
            async with session.get(url) as response:
                if response.status == 200:
                    if not os.path.isfile(file_path):
                        with open(file_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                    
                    image = Image.open(file_path)
                    resized_image = image.resize((360, 540))
                    resized_image.save(file_path)                  
        return f'{movie_id}.jpg'
    
    def get_result(data: Mapping) -> list[Movie]:
        result: list[Movie] = []
        for movie in data['docs']:
            result.append(
                Movie(
                    genres=[genre.get('name') for genre in  movie.get('genres')] if movie.get('genres') else [],
                    description=movie.get('description'),
                    rating_kp=movie.get('rating').get('kp'),
                    rating_imdb=movie.get('rating').get('imdb'),
                    year=movie.get('year'),
                    post_image_url=movie.get('poster').get('url'),
                    preview_url=movie.get('backdrop').get('previewUrl')
                )
            )
        return result
    