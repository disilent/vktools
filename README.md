# vktools
Модуль для анализа публичных данных пользователей vk.
Для работы требуется модуль `vk`.
## Usage
```python
from vktools import vktools
ACCESS_TOKEN = 'access_token'
  
test = vktools(ACCESS_TOKEN)
```
## Основные используемые функции:
### HiddenFriends
Выводит список всех доступных скрытых друзей пользователя.
```python
test.HiddenFriends([target], ids=user_ids)
#target - целевой id
#user_ids - список id людей, потенциально связанных с целью(опциональный аргумент)
#Если вывод результата не требуется, укажите агрумент output=False
```
### AllFriends
Выводит список всех доступных друзей пользователя.
```python
test.AllFriends([target], ids=user_ids)
#target - целевой id
#user_ids - список id людей, потенциально связанных с целью(опциональный аргумент)
#Если вывод результата не требуется, укажите агрумент output=False
```
### Friends
Выводит список открытых друзей пользователей.
```python
test.Friends(user_ids)
#user_ids - список id пользователей
#Если вывод результата не требуется, укажите агрумент output=False
```
### MutualFriends
Находит общих друзей группы пользователей.
```python
test.MutualFriends(user_ids)
#user_ids - список id пользователей
#Если вывод результата не требуется, укажите агрумент output=False
```
### GroupFriends
Отображает друзей пользователей, состоящих в такой-то группе.
```python
test.MutualFriends(user_ids, groups)
#user_ids - список id пользователей
#groups - список коротких ссылок или id групп
#Если вывод результата не требуется, укажите агрумент output=False
```
