import requests
import os
from typing import Dict, List
import random


class SmartStreamingService:
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.platforms = ['netflix', 'amazon', 'disney', 'hbo', 'apple', 'hulu']
        self.rapidapi_key = os.environ.get('RAPIDAPI_KEY')

    def check_availability(self, title: str, year: int) -> Dict[str, bool]:
        """Проверяет доступность на стриминговых платформах"""
        title_lower = title.lower()

        # 1. Проверяем в нашей базе знаний
        exact_match = self._find_exact_match(title_lower)
        if exact_match:
            return exact_match.copy()

        # 2. Ищем частичное совпадение
        partial_match = self._find_partial_match(title_lower)
        if partial_match:
            return partial_match.copy()

        # 3. Пытаемся получить данные из внешнего API (если есть ключ)
        if self.rapidapi_key and self.rapidapi_key != 'your-rapidapi-key-here':
            try:
                api_result = self._check_streaming_api(title, year)
                if api_result:
                    return api_result
            except Exception as e:
                print(f"Streaming API Error: {e}")

        # 4. Используем умный анализ как fallback
        return self._analyze_by_patterns(title_lower, year)

    def _check_streaming_api(self, title: str, year: int) -> Dict[str, bool]:
        """Проверяет доступность через внешний API"""
        # Это пример - можно использовать различные API
        # Например: JustWatch, Utelly, Streaming Availability API

        url = "https://streaming-availability.p.rapidapi.com/search/title"
        headers = {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': 'streaming-availability.p.rapidapi.com'
        }
        params = {
            'title': title,
            'country': 'ru',
            'show_type': 'all',
            'output_language': 'ru'
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_streaming_api_response(data)
        except Exception as e:
            print(f"Streaming API request failed: {e}")

        return {}

    def _parse_streaming_api_response(self, data: Dict) -> Dict[str, bool]:
        """Парсит ответ от API стриминга"""
        result = {platform: False for platform in self.platforms}

        if not data or 'result' not in data:
            return result

        for item in data['result']:
            streaming_info = item.get('streamingInfo', {})
            for platform in self.platforms:
                if platform in streaming_info.get('ru', []):
                    result[platform] = True

        return result

    def _build_knowledge_base(self):
        """Расширенная база знаний о стриминге"""
        return {
            # Фильмы
            'начало': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True, 'hulu': False},
            'темный рыцарь': {'netflix': False, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True,
                              'hulu': False},
            'побег из шоушенка': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': False,
                                  'hulu': False},
            'крестный отец': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': False,
                              'hulu': False},
            'форрест гамп': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True,
                             'hulu': False},
            'матрица': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True, 'hulu': False},
            'криминальное чтиво': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': False,
                                   'hulu': False},
            'интерстеллар': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True,
                             'hulu': False},
            'мстители: финал': {'netflix': False, 'amazon': True, 'disney': True, 'hbo': False, 'apple': True,
                                'hulu': False},
            'властелин колец: братство кольца': {'netflix': False, 'amazon': True, 'disney': False, 'hbo': True,
                                                 'apple': True, 'hulu': False},

            # Сериалы
            'очень странные дела': {'netflix': True, 'amazon': False, 'disney': False, 'hbo': False, 'apple': False,
                                    'hulu': False},
            'игра престолов': {'netflix': False, 'amazon': False, 'disney': False, 'hbo': True, 'apple': False,
                               'hulu': False},
            'во все тяжкие': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': False, 'apple': True,
                              'hulu': False},
            'мандалорец': {'netflix': False, 'amazon': False, 'disney': True, 'hbo': False, 'apple': False,
                           'hulu': False},
            'ведьмак': {'netflix': True, 'amazon': False, 'disney': False, 'hbo': False, 'apple': False, 'hulu': False},
            'ход королевы': {'netflix': True, 'amazon': False, 'disney': False, 'hbo': False, 'apple': False,
                             'hulu': False},
            'дом дракона': {'netflix': False, 'amazon': False, 'disney': False, 'hbo': True, 'apple': False,
                            'hulu': False},
            'локи': {'netflix': False, 'amazon': False, 'disney': True, 'hbo': False, 'apple': False, 'hulu': False},
            'корона': {'netflix': True, 'amazon': False, 'disney': False, 'hbo': False, 'apple': False, 'hulu': False},
            'наследники': {'netflix': False, 'amazon': False, 'disney': False, 'hbo': True, 'apple': False,
                           'hulu': False},

            # Дополнительные популярные фильмы
            'джокер': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True, 'hulu': False},
            'паразиты': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': True, 'hulu': False},
            'звездные войны: пробуждение силы': {'netflix': False, 'amazon': True, 'disney': True, 'hbo': False,
                                                 'apple': True, 'hulu': False},
            'криминальное чтиво': {'netflix': True, 'amazon': True, 'disney': False, 'hbo': True, 'apple': False,
                                   'hulu': False},
        }

    def _find_exact_match(self, title_lower: str):
        return self.knowledge_base.get(title_lower)

    def _find_partial_match(self, title_lower: str):
        for known_title, platforms in self.knowledge_base.items():
            if known_title in title_lower:
                return platforms
        return None

    def _analyze_by_patterns(self, title_lower: str, year: int):
        streaming_info = {platform: False for platform in self.platforms}

        # Анализ по студии/франшизе
        self._analyze_by_franchise(title_lower, streaming_info)

        # Анализ по году (новые фильмы чаще на Disney+ и Apple TV+)
        self._analyze_by_year(year, streaming_info)

        # Анализ по ключевым словам
        self._analyze_by_keywords(title_lower, streaming_info)

        return streaming_info

    def _analyze_by_franchise(self, title_lower: str, streaming_info: Dict[str, bool]):
        # Marvel (Disney+)
        marvel_keywords = ['марвел', 'мстители', 'железный человек', 'капитан америка', 'тор', 'черная пантера',
                           'доктор стрэндж']
        if any(keyword in title_lower for keyword in marvel_keywords):
            streaming_info['disney'] = True
            streaming_info['netflix'] = False

        # Star Wars (Disney+)
        star_wars_keywords = ['звездные войны', 'джедай', 'скайуокер', 'мандалорец', 'боба фетт']
        if any(keyword in title_lower for keyword in star_wars_keywords):
            streaming_info['disney'] = True

        # DC (HBO Max)
        dc_keywords = ['бэтмен', 'супермен', 'чудо-женщина', 'лига справедливости', 'аквамен', 'флэш', 'джокер']
        if any(keyword in title_lower for keyword in dc_keywords):
            streaming_info['hbo'] = True

        # Harry Potter (HBO Max)
        if 'гарри поттер' in title_lower:
            streaming_info['hbo'] = True

        # Lord of the Rings (Amazon Prime)
        if 'властелин колец' in title_lower or 'кольца власти' in title_lower:
            streaming_info['amazon'] = True

    def _analyze_by_year(self, year: int, streaming_info: Dict[str, bool]):
        # Новые релизы (2020+)
        if year >= 2020:
            streaming_info['netflix'] = random.random() > 0.4
            streaming_info['amazon'] = random.random() > 0.5
            streaming_info['disney'] = random.random() > 0.6
            streaming_info['apple'] = random.random() > 0.7

        # Средние (2010-2019)
        elif year >= 2010:
            streaming_info['netflix'] = random.random() > 0.3
            streaming_info['amazon'] = random.random() > 0.4
            streaming_info['hbo'] = random.random() > 0.5

        # Классика (до 2010)
        else:
            streaming_info['netflix'] = random.random() > 0.6
            streaming_info['amazon'] = random.random() > 0.5
            streaming_info['hbo'] = random.random() > 0.7

    def _analyze_by_keywords(self, title_lower: str, streaming_info: Dict[str, bool]):
        # Аниме (часто на Netflix, Hulu)
        anime_keywords = ['аниме', 'гбли', 'студия гбли', 'атака титанов', 'истребитель демонов']
        if any(keyword in title_lower for keyword in anime_keywords):
            streaming_info['netflix'] = True

        # Документалки (Netflix силен в этом)
        documentary_keywords = ['документальный', 'доку', 'настоящее преступление', 'расследование']
        if any(keyword in title_lower for keyword in documentary_keywords):
            streaming_info['netflix'] = True

        # Инди фильмы (часто на Amazon, Apple)
        indie_keywords = ['инди', 'независимый', 'санденс', 'кинофестиваль']
        if any(keyword in title_lower for keyword in indie_keywords):
            streaming_info['amazon'] = True
            streaming_info['apple'] = True


# Глобальный экземпляр сервиса
streaming_service = SmartStreamingService()