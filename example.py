import requests

# Создаем класс.
class TestNewLocation:
    def __init__(self): # Конструктора класса. Позволяет сохранять и повторно использовать данные, которые нужны всем методам класса. 
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
        post_url = f'{self.base_url}{self.post_resource}{self.key}'
        print(f"\nОтправка POST-запроса по URL: {post_url}")

        json_location = {
            "location": {
                "lat": -38.383494,
                "lng": 33.427362
            },
            "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": ["shoe park", "shop"],
            "website": "http://google.com",
            "language": "French-IN"
        }

        result_post = requests.post(post_url, json=json_location)
        response_json = result_post.json()
        print(f"Ответ POST-запроса: {response_json}")

        print(f'Статус-код: {result_post.status_code}')
        assert result_post.status_code == 200
        print('Статус-код POST корректен')

        status = response_json.get('status')
        print(f"Статус из ответа: {status}")
        assert status == 'OK'
        print('Поле Status корректно')

        place_id = response_json.get('place_id')
        print(f'Получен place_id: {place_id}')
        return place_id

    def save_place_ids_to_file(self, filename: str, count: int) -> None:
        """
        Создаёт указанное количество локаций и записывает их place_id в файл.
        filename: Имя файла для сохранения place_id.
        count: Количество локаций для создания.
        """
        print(f"\nСоздание {count} локаций и запись place_id в файл {filename}")
        with open(filename, 'w') as f:
            for _ in range(count):
                place_id = self.test_create_new_location()
                f.write(f"{place_id}\n")
        print(f"Все {count} place_id записаны в файл {filename}")

    def test_locations_from_file(self, filename: str) -> None:
        """
        Читает place_id из файла, проверяет каждую локацию,
        удаляет 2-ю и 4-ю, и затем проверяет их удаление.
        filename: Имя файла, содержащего place_id.
        """
        print(f"\nЧтение place_id из файла и проверка через GET")
        try:
            with open(filename, 'r') as file:
                file_place_ids = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
            return
        
        # 1. Проверяем все локации до удаления
        print("\n--- Шаг 1: Проверка всех локаций через GET ---")
        for place_id in file_place_ids:
            self._check_location_with_get(place_id, expected_status=200)

        # 2. Удаляем 2-ю и 4-ю локации
        print("\n--- Шаг 2: Удаление 2-й и 4-й локации ---")
        if len(file_place_ids) >= 4:
            place_id_to_delete_2 = file_place_ids[1]  # 2-я локация (индекс 1)
            place_id_to_delete_4 = file_place_ids[3]  # 4-я локация (индекс 3)

            self._delete_location(place_id_to_delete_2)
            self._delete_location(place_id_to_delete_4)
        else:
            print("Недостаточно place_id в файле для удаления 2-й и 4-й локации.")

        # 3. Проверяем, что удаленные локации больше недоступны
        print("\n--- Шаг 3: Проверка удаленных локаций (ожидается 404) ---")
        if len(file_place_ids) >= 4:
            self._check_location_with_get(file_place_ids[1], expected_status=404, msg="Get operation failed, looks like place_id doesn't exists")
            self._check_location_with_get(file_place_ids[3], expected_status=404, msg="Get operation failed, looks like place_id doesn't exists")

        # 4. Проверяем, что оставшиеся локации по-прежнему доступны
        print("\n--- Шаг 4: Проверка оставшихся локаций (ожидается 200) ---")
        if len(file_place_ids) >= 5:
            self._check_location_with_get(file_place_ids[0], expected_status=200)
            self._check_location_with_get(file_place_ids[2], expected_status=200)
            self._check_location_with_get(file_place_ids[4], expected_status=200)
        
        print("\nТест по работе с файлом завершен.")

    def _check_location_with_get(self, place_id: str, expected_status: int, msg: str = None) -> None:
        """
        Вспомогательный метод для выполнения GET-запроса и проверки статуса.
        """
        get_url = f'{self.base_url}{self.get_resource}{self.key}&place_id={place_id}'
        result_get = requests.get(get_url)
        
        print(f"Проверка place_id '{place_id}': Статус-код GET: {result_get.status_code}")
        assert result_get.status_code == expected_status

        if msg:
            response_json = result_get.json()
            assert response_json.get('msg') == msg
            print('Поле msg корректно')

    def _delete_location(self, place_id: str) -> None:
        """
        Вспомогательный метод для выполнения DELETE-запроса и проверки.
        """
        delete_url = f'{self.base_url}{self.delete_resource}{self.key}'
        json_delete_location = {"place_id": place_id}
        result_delete = requests.delete(delete_url, json=json_delete_location)
        response_json = result_delete.json()

        print(f"Отправка DELETE-запроса для place_id '{place_id}':")
        print(f"  Статус-код: {result_delete.status_code}")
        assert result_delete.status_code == 200
        print(f"  Статус из ответа: {response_json.get('status')}")
        assert response_json.get('status') == 'OK'
        print("  Удаление успешно.")

# Создаём экземпляр класса для запуска тестов.
start = TestNewLocation()

# Создаём 5 новых локаций и сохраняем их идентификаторы в файл "place_ids.txt".
start.save_place_ids_to_file("place_ids.txt", 5)

# Проверяем локации из файла, удаляем 2-ю и 4-ю и проверяем их отсутствие.
start.test_locations_from_file("place_ids.txt")

print('\nТест завершен успешно')
