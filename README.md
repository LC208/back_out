
### Установка
1. Скачиваем репу
2. Создаем виртуальное окружение в папке с проектом с помощью команды
  Windows: py -m venv venv
  Linux: python/python3 -m venv venv
3. Активируем виртуальное окружение с помощью
     Windows: venv\Scripts\activate
     Linux: source venv/bin/activate
4. Устанавливаем все пакеты с помощью команды pip install -r req.txt

### Запуск через Docker 
1. в out/settings.py меняем HOST на 'db'
2. docker-compose/docker compose up
