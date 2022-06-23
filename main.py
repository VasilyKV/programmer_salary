import collections
import requests
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def predict_rub_salary(vacancies, website):
    salary_sum = 0
    vacancies_processed = 0
    for vacancy in vacancies:
        if website == 'hh' and vacancy['salary']:
            payment_from = vacancy['salary']['from']
            payment_to = vacancy['salary']['to']
            is_currency_rub = (vacancy['salary']['currency'] == 'RUR')
        elif website == 'sj':
            payment_from = vacancy['payment_from']
            payment_to = vacancy['payment_to']
            is_currency_rub = (vacancy['currency'] == 'rub')
        else:
            continue
        vacancy_salary = predict_salary(payment_from, payment_to)
        if vacancy_salary and is_currency_rub:
            salary_sum += vacancy_salary
            vacancies_processed += 1
    average_salary = int(salary_sum / max(vacancies_processed, 1))
    return vacancies_processed, average_salary


def get_salary_hh(languages, pages_number):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': '',
        'area': 1,
        'period': 30,
        'page': 0
    }
    languages_stat = {}
    for language in languages:
        payload['text'] = f'программист {language}'
        vacancies = []
        page = 0
        while page < pages_number:
            payload['page'] = page
            response = requests.get(url, params=payload)
            response.raise_for_status()
            collected_data = response.json()
            pages_number = min(pages_number, collected_data['pages'])
            vacancies += collected_data['items']
            page += 1
        vacancies_processed, average_salary = predict_rub_salary(vacancies, 'hh')
        language_stat = {
            'vacancies_found': collected_data['found'],
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
        languages_stat[language] = language_stat
    return languages_stat


def get_salary_sj(languages, key_sj, pages_number):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    request_headers = {
        'X-Api-App-Id': key_sj
    }
    payload = {
        'keyword': 'программист Python',
        'town': 4,
        'period': 7,
        'page': 0
    }
    languages_stat = {}
    for language in languages:
        payload['keyword'] = f'программист {language}'
        vacancies = []
        page = 0
        more_page = True
        while page < pages_number and more_page:
            payload['page'] = page
            response = requests.get(url, headers=request_headers, params=payload)
            response.raise_for_status()
            collected_data = response.json()
            more_page = collected_data['more']
            vacancies += collected_data['objects']
            page += 1
        vacancies_processed, average_salary = predict_rub_salary(vacancies, 'sj')
        language_stat = {
            'vacancies_found': collected_data['total'],
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
        languages_stat[language] = language_stat
    return languages_stat


def print_table(languages_stat, title):
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for language, language_stat in languages_stat.items():
        table_row = [
            language,
            language_stat['vacancies_found'],
            language_stat['vacancies_processed'],
            language_stat['average_salary']
        ]
        table_data.append(table_row)
    table = AsciiTable(table_data, title)
    print(table.table)


def main():
    load_dotenv()
    key_sj = os.getenv('KEY_SUPERJOB')
    languages = os.getenv('LANGUAGES', default='Python').split(', ')
    pages_number = int(os.getenv('PAGES_NUMBER', default=1000))

    print_table(get_salary_hh(languages, pages_number), 'HeadHunter-Moscow')
    print('')
    print_table(get_salary_sj(languages, key_sj, pages_number), 'SuperJob-Moscow')


if __name__ == '__main__':
    main()