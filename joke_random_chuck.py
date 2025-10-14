import requests
import json


class TestCreateJoke:

    url = "https://api.chucknorris.io/jokes/random"

    def test_create_random_joke(self, category):

        endpoint = f'?category={category}'
        url_random_joke = self.url + endpoint
        print(url_random_joke)

        result = requests.get(url_random_joke)
        print(result.json())

        print(f'Статус код {result.status_code}')
        assert result.status_code == 200, f"Ошибка, код не корректен"
        print('Статус код корректен')

        check_joke = result.json()
        joke_category = check_joke.get("categories", [])
        print(f'Категории шутки: {joke_category}')

        assert category in joke_category, f"Категория не верна."
        print('Категория корректна')

        joke_text = check_joke.get('value','').lower()
        name_to_find = 'chuck'
        assert name_to_find in joke_text, f"Имя не найдено"
        print('Имя найдено')

        print("\nПолная шутка:")
        print(json.dumps(joke_text, indent=4, ensure_ascii=False), "\nТест успешно завершен!")


start = TestCreateJoke()
start.test_create_random_joke("food")

