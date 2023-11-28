import os
import json
import aiohttp


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

    async def search_movie(self, query: str):
        session = await self.get_session()
        url = f'{self.url}movie?page=1&limit=5&rating.kp=4-10&year=2023&genres.name=криминал'
        async with session.get(url, headers=self.headers) as response:
            result = await response.json()
            with open('app/mock/result.json', 'w') as f:
                json.dump(result, f, indent=2)
            return result

    async def download_image(self, url: str, query: str):
        session = await self.get_session()
        if not os.path.exists(f'app/images/{query}'):
            os.makedirs(f'app/images/{query}')
        async with session.get(url) as response:
            if response.status == 200:
                if url[-4:] == '.jpg':
                    movie_id = url.split(".")[-2].split('/')[-1]
                else:
                    movie_id = url.split("/")[-2]
                if not os.path.isfile(f'app/images/{query}/{movie_id}.jpg'):
                    with open(f'app/images/{query}/{movie_id}.jpg', 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
    
    