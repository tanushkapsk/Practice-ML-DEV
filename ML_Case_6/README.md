### Настройка проекта 

1. Если не установлено виртуальное окружение, то выполнить команду в консоли: 
   - python3 -m pip install venv

2. Запустить виртуальное окружение командой:
   - python3 -m venv env

3. Активировать виртуальное окружение командой:
   - source venv/bin/python

4. Установить все необходимые пакеты для работы pip install -r requirements.txt
Сразу будут установлены все зависимости для приложения.

5. После этого нужно запустить модуль alembic для создания базы и миграций в ней:
   5.1 - выполняем команду: alembic revision --autogenerate
   5.2 - выполняем обновление командой: alembic upgrade head

6. Запустить проект командой (стандартная ссылка на главную страницу - http://127.0.0.1:8000/):
   - uvicorn main:app --reload

7. Чтобы прервать работу сервиса, использовать сочетание клавиш Ctrl + C

8. По ссылке /docs доступны все запросы - для правильной работы приложения сначала надо загрузить файл csv с данными.
Нужно использовать запрос /upload_csv_file и в него загрузить файл. Запрос был сделан на основе файла csv из задачи.
Этот файл находится в архиве dataset6.zip

9. Все остальные запросы нужны для авторизации, регистрации и прочего функционала приложения.