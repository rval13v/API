# импортируем библиотеку
import requests
import json
# Адрес на который будем отправлять запрос
url = "https://official-joke-api.appspot.com/jokes/random"
# Выводит на печать URL,по которому отправляем запрос
print(url)
# Создали переменную резалт и присвоили ей запрос с методом get на указанный url
result = requests.get(url)
# Выводит на печать статус-код ответа
print("Статус код: " + str(result.status_code))
# Проверяем ОР с ФР
assert result.status_code == 200
print('Статус код корректен')
result.encoding = 'utf-8'
print(result.json())