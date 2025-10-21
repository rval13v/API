# Файл для put_json.py
import requests


def test_put(place_id, get_url):
    base_url = 'https://rahulshettyacademy.com'
    key = '?key=qaclick123'
    put_resourse = '/maps/api/place/update/json'
    new_address = '50 Sovetskay street, RU'  
    put_url = base_url + put_resourse + key
    print(put_url)

    json_put_location = {
        "place_id" : place_id,
        "address" : new_address,
        "key" : "qaclick123"
    }

    result_put = requests.put(put_url, json=json_put_location)
    print(result_put.json())

    print(f'Статус-код: {result_put.status_code}')
    assert result_put.status_code == 200
    print('Статус-код PUT корректен')

    check_response_put = result_put.json()

    msg = check_response_put.get('msg')
    print(msg)
    assert msg == 'Address successfully updated'
    print('Поле MSG корректно')

    result_get = requests.get(get_url)
    print(result_get.json())
    check_response_get = result_get.json()

    print(f'Статус-код: {result_get.status_code}')
    assert result_get.status_code == 200
    print('Статус код GET корректен')

    actual_address = check_response_get.get('address')
    print(actual_address)
    assert actual_address == new_address
    print('Адрес изменился')
    
