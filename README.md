# vktools
Модуль для анализа публичных данных пользователей vk.
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
#user_ids - список людей, потенциально связанных с целью(опциональный аргумент)
#Если вывод результата не требуется, укажите агрумент print=False
```
### AllFriends
Выводит список всех доступных друзей пользователя.
```python
test.AllFriends([target], ids=user_ids)
#target - целевой id
#user_ids - список людей, потенциально связанных с целью(опциональный аргумент)
#Если вывод результата не требуется, укажите агрумент print=False
### Friends
Выводит список открытых друзей пользователей.
### MutualFriends
Находит общих друзей группы пользователей.
### GroupFriends
Отображает друзей пользователей, состоящих в такой-то группе.
