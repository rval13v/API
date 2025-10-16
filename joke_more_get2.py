import requests


class TestCreateJokeCategory:
    url = "https://api.chucknorris.io/jokes"

    def get_categories(self, expected_status_code):
        # получаем список всех категорий и проверяем статус код
        path_category = '/categories'
        url_category = self.url + path_category

        result = requests.get(url_category)

        print(f'Получение списка категорий: {url_category}')
        print(f'Статус-код: {result.status_code}')
        assert result.status_code == expected_status_code
        print('Статус-код корректен')

        categories = result.json()
        print('Список всех категорий: ', categories)
        return categories

    def get_joke_by_category(self, category):
        #Извлекает одну случайную шутку для данной категории.
        path_random_joke = '/random'
        params = {'category': category}
        url_joke = self.url + path_random_joke

        print(f'\nПолучение шутки из категории: ')
        result = requests.get(url_joke, params=params)
        result.raise_for_status()

        joke_data = result.json()
        # API возвращает значение шутки в поле 'value'.
        return joke_data.get('value')

    def request_joke_from_user(self):
        # Получает список категорий и запрашивает у пользователя одну из них
        categories = self.get_categories(200)

        while True:
            # Запрос у пользователя категории
            user_input = input("\nВведите категорию, по которой хотите получить шутку, или 'exit' для завершения: ").lower()

            if user_input == 'exit':
                print("Программа завершена.")
                break

            if user_input in categories:
                joke = self.get_joke_by_category(user_input)
                if joke:
                    print(f"\nШутка из категории '{user_input}':")
                    print(joke)
                else:
                    print("\nНе удалось получить шутку.")
            else:
                print("\nТакой категории не существует. Bыберите из списка выше.")


start = TestCreateJokeCategory()
start.request_joke_from_user()
