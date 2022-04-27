<h1>Создание pdf-файлов из актуальных статей на Хабре о Python </h1>

<p>
1. Парсим актуальные хабы о python  ‘https://habr.com/ru/hub/python/’.<br>
2. Создаем базу данных (Sqlite3), 3 поля  типа-TEXT, 1 поле типа-BLOB.<br>
3. Упаковываем BLOB-данные и складываем, не забываем об обновлении.<br>
4. Легкое оформление для контента на reportlab для title и text. (Модуль reportlab из коробки не поддерживает "кириллицу"), 
  поэтому на помощь приходит шрифт 'DejaVuSerif.ttf'.<br>
5. Распаковываем данные из бд себе на пк.<br>
6. Читаем и радуемся.<br>
</p>
<h2>Библиотеки:</h2> <h3>beautifulSoup, requests, sqlite3, reportlab, pickle, os</h3>
<img width="537" alt="Screenshot_1" src="https://user-images.githubusercontent.com/85381084/165484948-d3b42996-8aed-4164-a861-076e186f0e23.png">
<img width="432" alt="Screenshot_2" src="https://user-images.githubusercontent.com/85381084/165485104-96d3880f-d828-4969-b443-598d5bb1fec3.png">
<img width="637" alt="Screenshot_3" src="https://user-images.githubusercontent.com/85381084/165485259-5b244c3c-c52c-4db1-879d-153cbb1472b4.png">
<img width="613" alt="Screenshot_4" src="https://user-images.githubusercontent.com/85381084/165485275-b5adafa1-e521-4fd2-91e0-f52136af1746.png">
<img width="618" alt="Screenshot_5" src="https://user-images.githubusercontent.com/85381084/165485294-92c86d57-92e0-4f8c-9378-6bc5ff7e0fa4.png">
<img width="690" alt="Screenshot_6" src="https://user-images.githubusercontent.com/85381084/165485312-b41539ae-2db4-4b8f-8f80-3831f274cdcf.png">
