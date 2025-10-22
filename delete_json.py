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

        # Удаляем 2-ю и 4-ю локации
        if len(file_place_ids) >= 4: # Тут проверяем больше ли 4х записей локаций
          place_id_to_delete_2 = file_place_ids[1]  # 2-я локация
          place_id_to_delete_4 = file_place_ids[3]  # 4-я локация

          self.delete_location(place_id_to_delete_2)
          self.delete_location(place_id_to_delete_4)
        else:
            print("Недостаточно place_id в файле для удаления 2-й и 4-й локации.")
        
        print("\nУдаление 2-й и 4-й локации прошло успешно")

    # Метод для удаления
    def delete_location(self, place_id: str) -> None:
        delete_url = self.base_url + self.delete_resource + self.key
        json_delete_location = {"place_id": place_id}
        result_delete = requests.delete(delete_url, json=json_delete_location)
        response_json = result_delete.json()
    
    # Метод, который проверяет удаленные локации и те что остались и записывает последние в новый файл.
    def check_location_with_get(self, filename, remaining_filename: str) -> None:
      try:
        with open(filename, 'r') as file:
          initial_place_ids = [line.strip() for line in file.readlines() if line.strip()]
      except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
      
      # Определяем, какие place_id должны были быть удалены      
      place_ids_to_delete = []
      if len(initial_place_ids) >= 4:
        place_ids_to_delete.append(initial_place_ids[1])
        place_ids_to_delete.append(initial_place_ids[3])
    
      # Определяем, какие place_id должны были остаться. На каждой итерации pid временно принимает значение текущего элемента списка initial_place_ids
      remaining_place_ids = [pid for pid in initial_place_ids if pid not in place_ids_to_delete]
    
      print("\n Удаляемые place_id:", place_ids_to_delete)
      print("Сохраняемые place_id:", remaining_place_ids)
        
      # Выполняем GET-запросы для проверки каждой локации
      for place_id in initial_place_ids:
        get_url = self.base_url + self.get_resource + self.key + '&place_id=' + place_id
        result_get = requests.get(get_url)
        
        if place_id in place_ids_to_delete:
            # Удаленные локации должны вернуть ошибку 404 Not Found)
            print(f"Проверка удаленной локации '{place_id}': Статус-код GET: {result_get.status_code}")
            assert result_get.status_code != 200, f"Ошибка: Удаленная локация {place_id} все еще доступна."
            if result_get.status_code == 404:
                print(f"Локация '{place_id}' была успешно удалена (статус 404).")
        else:
            # Ожидается, что оставшиеся локации вернут успешный статус (200 OK)
            print(f"Проверка оставшейся локации '{place_id}': Статус-код GET: {result_get.status_code}")
            assert result_get.status_code == 200, f"Ошибка: Оставшаяся локация {place_id} недоступна."
            if result_get.status_code == 200:
              print(f"Локация '{place_id}' осталась доступной (статус 200).")        
              
        
        print(f"\nСоздание локаций и запись place_id в файл {remaining_filename}")
        
        with open(remaining_filename, 'w') as new_file:
          for place_id in remaining_place_ids:
            new_file.write(f"{place_id}\n")
        print(f"Все оставшиеся place_id записаны в файл {remaining_filename}")


source_filename = "place_ids.txt"
remaining_filename = "remaining_place_ids.txt"

# Создаём экземпляр класса для запуска тестов.
start = TestNewLocation()

# Создаём 5 новых локаций и сохраняем их идентификаторы в файл "place_ids.txt".
start.save_place_ids_to_file("place_ids.txt", 5)

# Проверяем локации, сохранённые в файле, с помощью GET-запросов.
start.test_locations_from_file("place_ids.txt")
start.check_location_with_get(source_filename, remaining_filename)

print('\nТест завершен успешно')
