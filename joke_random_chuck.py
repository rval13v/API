import requests
import json
# Создаем общий класс
class Testcreatejoke():
    # вывели url за метод, но оставили внутри класса
    url = "https://api.chucknorris.io"
    # Создали метод для теста
    def test_create_random_joke(self):

        endpoint = '/jokes/random' # прописали путь эндпоинт
        url_random_joke = self.url + endpoint #перем кот к оcн url добавляем наш путь
        print(url_random_joke)
        # Запрос к  url и Выводим шутку в формате json
        result = requests.get(url_random_joke)
        print(result.json())
        # Выводим статус код и проверяем ОР с ФР
        print(f'Статус код {result.status_code}')
        assert result.status_code == 200, f"Ошибка, код не корректен"
        print('Статус код корректен')

        check_joke = result.json()
        # Проверка, что категории - это пустой список
        joke_category = check_joke.get('categories', [])
        print(joke_category)
        assert joke_category == [], f"Ошибка: Список категорий не пуст."
        print('Категория корректна')

        # Извлекаем текст шутки
        joke_text = check_joke.get('value','').lower()
        # Проверяем есть ли слово chuck
        name_to_find = 'chuck'
        assert name_to_find in joke_text, f"Имя не найдено"
        print("Имя найдено")

        print("\nПолная шутка:")
        print(json.dumps(joke_text, indent=4, ensure_ascii=False))
        print("\nТест успешно завершен!")

# Экземпляр класса
start = Testcreatejoke()
start.test_create_random_joke() #вызов метода

