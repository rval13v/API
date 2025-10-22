import requests

# Создаем класс.
class TestNewLocation:
    def __init__(self) -> None: # Конструктора класса. Позволяет сохранять и повторно использовать данные, которые нужны всем методам класса.
        # Базовый URL для API.
        self.base_url = 'https://rahulshettyacademy.com'
        # Ключ API для аутентификации.
        self.key = '?key=qaclick123'
        # Ресурс для POST-запроса
        self.post_resource = '/maps/api/place/add/json'
        # Ресурс для GET-запроса
        self.get_resource = '/maps/api/place/get/json'
        # Ресурс для DELETE-запроса
        self.delete_resource = '/maps/api/place/delete/json'

    def test_create_new_location(self) -> str:
        """
        Отправляет POST-запрос для создания новой локации и
        проверяет, что запрос прошёл успешно.
        Возвращает 'place_id' новой локации.
        """
        # Полный URL для POST-запроса
        post_url = self.base_url + self.post_resource + self.key
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

        # Выполняем GET-запрос для каждого place_id из файла.
        for place_id in file_place_ids:
            if place_id:
                # Создаём полный URL для GET-запроса.
                get_url = self.base_url + self.get_resource + self.key + '&place_id=' + place_id
                result_get = requests.get(get_url)
                # Проверяем, что статус-код GET-запроса — 200.
                print(f"Проверка place_id '{place_id}': Статус-код GET: {result_get.status_code}")
                assert result_get.status_code == 200

        # 2. Удаляем 2-ю и 4-ю локации
        print("\n--- Шаг 2: Удаление 2-й и 4-й локации ---")
        if len(file_place_ids) >= 4:
            place_id_to_delete_2 = file_place_ids[1]  # 2-я локация (индекс 1)
            place_id_to_delete_4 = file_place_ids[3]  # 4-я локация (индекс 3)

            self.delete_location(place_id_to_delete_2)
            self.delete_location(place_id_to_delete_4)
        else:
            print("Недостаточно place_id в файле для удаления 2-й и 4-й локации.")

        
    def delete_location(self, place_id: str) -> None:
        """
        Вспомогательный метод для выполнения DELETE-запроса и проверки.
        """
        delete_url = self.base_url + self.delete_resource + self.key
        json_delete_location = {"place_id": place_id}
        result_delete = requests.delete(delete_url, json=json_delete_location)
        response_json = result_delete.json()


    def check_location_with_get(self, place_id: str) -> None:
        print(f"\n Чтение place_id из файла и проверка через GET запрос после удаления 2 и 4")
        try:
            with open(filename, 'r') as file:
                file_place_ids = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
            return
          
        for place_id in file_place_ids[1],[4]]:
            if place_id:
                get_url = self.base_url + self.get_resource + self.key + '&place_id=' + place_id
                result_get = requests.get(get_url)
                print(f"Проверка place_id '{place_id}': Статус-код GET: {result_get.status_code}")
                assert result_get.status_code == 404
                print("Локации 2 и 4 удалены и проверены")

        # print(f"Отправка DELETE-запроса для place_id '{place_id}':")
        # print(f"  Статус-код: {result_delete.status_code}")
        # assert result_delete.status_code == 200
        # print(f"  Статус из ответа: {response_json.get('status')}")
        # assert response_json.get('status') == 'OK'
        # print("  Удаление успешно.")

        # get_url = self.base_url + self.get_resource + self.key + '&place_id=' + place_id
        # result_get = requests.get(get_url)
        # print(result_get.json())

        # print(f'Статус-код: {result_get.status_code}')
        # assert result_get.status_code == 404
        # print('Стутс-код корректен, локация удалена')

        # check_response_get = result_get.json()
        # msg = check_response_get.get('msg')
        # print(msg)
        # assert msg == "Get operation failed, looks like place_id  doesn't exists"
        # print('Поле MSG корректно')


# Создаём экземпляр класса для запуска тестов.
start = TestNewLocation()

# Создаём 5 новых локаций и сохраняем их идентификаторы в файл "place_ids.txt".
start.save_place_ids_to_file("place_ids.txt", 5)

# Проверяем локации, сохранённые в файле, с помощью GET-запросов.
start.test_locations_from_file("place_ids.txt")

print('\nТест завершен успешно')
