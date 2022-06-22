# Космический Телеграм

Проект предназначен для скачивания фотографий с популярных ресурсов космической тематики: Spacex, Nasa и их
публикации в телеграм-канале.

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

`pip install -r requirements.txt`

### Переменные окружения
Необходимо создать файл .env, в котором должны быть указаны значения следующие переменные:  
NASA_API_KEY = {NASA_API_KEY}  
TELEGRAM_TOKEN = {TELEGRAM_TOKEN}  
TELEGRAM_CHAT_ID = {TELEGRAM_CHAT_ID}  
EXECUTION_PERIOD = {seconds}

Для получения API_KEY NASA, пройдите регистрацию на сайте: https://api.nasa.gov/  
Создайте Telegram бота, получите API токен бота. [Как регистировать бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html).  
Воспользуйтесь существующим Telegram каналом или [создайте новый канал](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/), куда бот будет публиковать фото. Созданного бота необходимо добавить в администраторы канала.
Узнайте CHAT_ID вашего канала.  
EXECUTION_PERIOD - временной период публикации фотографий Telegram ботом, задается в секундах.

### Структура проекта
fetch_nasa.py. Скрипт скачивает фотографии в указанную папку, используя API Nasa:  
1. Astronomic picture of the day APOD: https://api.nasa.gov/#apod  
2. Earth Polychromatic imaging Camera EPIC: https://api.nasa.gov/#epic  

fetch_spacex.py. Скрипт скачивает фотографии в указанную папку, используя API SpaceX. [Репозиторий на Github API SpaceX](https://github.com/r-spacex/SpaceX-API). 

post_telegram.py. Telegram бот публикует фото из указанной папки с заданным интервалом. 


### Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
