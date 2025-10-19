import requests
import json
import time

class test_new_location():
  
  
    def __init__(self):
        self.list_place_id = []  # Пустой список place id

    def test_create_new_location(self):

        base_url = 'https://rahulshettyacademy.com'
        key = '?key=qaclick123'
        post_resourse = '/maps/api/place/add/json'
        post_url = base_url + post_resourse + key
        print(post_url)

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

        result_post = requests.post(post_url, json=json_location)
        print(result_post.json())

        print(f'Статус-код: {result_post.status_code}')
        assert result_post.status_code == 200
        print('Стату-код POST корректен')

        check_response_post = result_post.json()

        status = check_response_post.get('status')
        print(status)
        assert status == 'OK'
        print('Поле Status корректно')

        place_id = check_response_post.get('place_id')
        print(f'Поле place_id: {place_id}')
        return place_id

    def save_place_ids_to_file(self, filename: str, count: int):
        print(f"\n Создание {count} локаций и запись place_id в файл {filename}")
        self.list_place_id = []
        for i in range(count):
            place_id = self.test_create_new_location()
            self.list_place_id.append(place_id)
        
        with open(filename, 'w') as f:
            for place_id in self.list_place_id:
                f.write(f"{place_id}\n")
        print(f"Все {count} place_id записаны в файл {filename}")
    
    
    def test_locations_from_file(self, filename: str, delay_seconds):
        print(f"\n Чтение place_id из файла и проверка через GET запрос с задержкой 10 сек.")
        time.sleep(delay_seconds)
        
        try:
            with open(filename, 'r') as file:
                file_place_ids = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
            return

        base_url = 'https://rahulshettyacademy.com'
        key = '?key=qaclick123'
        get_resourse = '/maps/api/place/get/json'

        for place_id in file_place_ids:
            if place_id:
                get_url = base_url + get_resourse + key + '&place_id=' + place_id
                result_get = requests.get(get_url)
                
                print(f"Проверка place_id '{place_id}': Статус-код GET: {result_get.status_code}")
                assert result_get.status_code == 200

                
start = test_new_location()
start.save_place_ids_to_file("place_ids.txt", 5)
start.test_locations_from_file("place_ids.txt", delay_seconds=10)
print('\nТест завершен успешно')

  




