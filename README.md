# Будущая зарплата

Проект предназначен для опроса сайтов [Headhunter.ru](https://hh.ru) и [SuperJob.ru](https://www.superjob.ru/) для получения статистики по зарпалатам программистов.  
Результат работы программы выводится в виде таблицы в консоли.

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Переменные окружения
Необходимо создать файл .env, в котором должны быть указаны значения следующие переменные:  
```
KEY_SUPERJOB = {KEY_SUPERJOB}  
LANGUAGES = {language1, language2, ...,languageN}  
PAGES_NUMBER = {PAGES_NUMBER}  
```
Пример:  
```
KEY_SUPERJOB = v3.r.xxxxxxxxxxxxxxxxxxxxxx4
LANGUAGES = Python, Java, Javascript, Ruby, PHP, C++, C#, Scala  
PAGES_NUMBER = 100
```
- KEY_SUPERJOB - обязательный параметр. Это 'Secret key' вашего приложения для сайта SuperJob.  
Для его получения необходимо пройти регистрацию на сайте https://api.superjob.ru/  
- LANGUAGES - указывается список языков программирования по которым собирается статистика.  
Разделитель между языками - запятая с пробелом ', '. Если LANGUAGES не указан, то применяется параметр по умолчанию:
```
LANGUAGES = Python
```
- PAGES_NUMBER - ограничение по количеству обрабатываемых вакансий. По умолчанию сайты [Headhunter.ru](https://hh.ru) и [SuperJob.ru](https://www.superjob.ru/) выдают по 20 объявлений на страницу. Данным параметром можно ограничить количество страниц обрабатываемых вакансий.  
- Если PAGES_NUMBER не указан, то применяется параметр по умолчанию:
```
PAGES_NUMBER = 1000
```
### Пример использования
```
python main.py
```

### Вывод результата
Результат выводится в табличной форме и имеет следующий стобцы:
- Язык программирования
- Вакансий найдено.
- Вакансий обработано. Данное значение формируется как выборка из найденных вакансий, ограниченное параметром PAGES_NUMBER, а так же теми вакансиями у которых указана зарабатная плата.
- Средняя зарплата. Если в вакансии указаны оба поля “зарплата от” и “ зарплата до”, то считается среднее. Если только “зарплата от”, то это значение умножается на 1.2, а если только “до”, это значение умножается на 0.8

### Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
