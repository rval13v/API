import requests


# Создаем класс.
class TestNewLocation:
    def test_create_new_location(self) -> str:
        """
        Отправляет POST-запрос для создания новой локации и
        проверяет, что запрос прошёл успешно.
        Возвращает 'place_id' новой локации.
        """
        # Базовый URL для API.
        base_url = 'https://rahulshettyacademy.com'
        # Ключ API для аутентификации.
        key = '?key=qaclick123'
        # Ресурс для POST-запроса
        post_resourse = '/maps/api/place/add/json'
        # Полный URL для POST-запроса
        post_url = base_url + post_resourse + key
        print(post_url)

        # Тело запроса в формате JSON с данными для новой локации.
        json_location = {
            "location": {
                "lat": -38.383494,
                "lng": 33.427362
            }, "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "http://google.com",
            "language": "French-IN"
        }

        # Отправляем POST-запрос с JSON-данными.
        result_post = requests.post(post_url, json=json_location)
        # Выводим ответ сервера в формате JSON.
        print(result_post.json())

        # Проверяем, что статус-код ответа — 200.
        print(f'Статус-код: {result_post.status_code}')
        assert result_post.status_code == 200
        print('Стату-код POST корректен')

        # Получаем данные из JSON-ответа.
        check_response_post = result_post.json()

        # Проверяем, что поле status в ответе имеет значение OK.
        status = check_response_post.get('status')
        print(status)
        assert status == 'OK'
        print('Поле Status корректно')

        # Извлекаем place_id из ответа.
        place_id = check_response_post.get('place_id')
        print(f'Поле place_id: {place_id}')
        return place_id

    # Метод для создания нескольких локаций и сохранения их place_id в файл.
    def save_place_ids_to_file(self, filename: str, count: int) -> None:
        """
        Создаёт указанное количество локаций и записывает их place_id в файл.
        filename Имя файла для сохранения place_id.
        count Количество локаций для создания.
        """
        print(f"\nСоздание {count} локаций и запись place_id в файл {filename}")
       # Записываем каждый place_id в файл на новой строке.
        with open(filename, 'w') as f:
            for _ in range(count):
                place_id = self.test_create_new_location()
                f.write(f"{place_id}\n")
        print(f"Все {count} place_id записаны в файл {filename}")

    # Метод для проверки локаций из файла с помощью GET-запросов.
    def test_locations_from_file(self, filename: str) -> None:
        """
        Читает place_id из файла и проверяет каждую локацию
        с помощью GET-запроса, убеждаясь в корректности ответа.
        filename: Имя файла, содержащего place_id.
        """
        print(f"\n Чтение place_id из файла и проверка через GET запрос")
        # Читаем place_id из файла.
        try:
            with open(filename, 'r') as file:
                # Удаляем пробелы в начале и конце каждой строки.
                file_place_ids = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
            return

        # Базовые параметры для GET-запроса.
        base_url = 'https://rahulshettyacademy.com'
        key = '?key=qaclick123'
        get_resourse = '/maps/api/place/get/json'

        # Выполняем GET-запрос для каждого place_id из файла.
        for place_id in file_place_ids:
            if place_id:
                # Создаём полный URL для GET-запроса.
                get_url = base_url + get_resourse + key + '&place_id=' + place_id
                result_get = requests.get(get_url)
                # Проверяем, что статус-код GET-запроса — 200.
                print(f"Проверка place_id '{place_id}': Статус-код GET: {result_get.status_code}")
                assert result_get.status_code == 200

# Создаём экземпляр класса для запуска тестов.
start = TestNewLocation()

# Создаём 5 новых локаций и сохраняем их идентификаторы в файл "place_ids.txt".
start.save_place_ids_to_file("place_ids.txt", 5)

# Проверяем локации, сохранённые в файле, с помощью GET-запросов.
start.test_locations_from_file("place_ids.txt")

print('\nТест завершен успешно')
