import collections
import requests
from pprint import pprint

languages = ['Python', 'Java', 'Javascript', 'Ruby' ,'PHP' , 'C++', 'C#']

def predict_rub_salary(vacancy):
	salary = vacancy['salary']
	if salary:
		if salary['currency'] != 'RUR':
			return
		if (salary['from'] is not None) & (salary['to'] is not None):
			return (salary['from'] + salary['to'])/2
		elif (salary['from'] is None):
			return (salary['to'])*0.8
		elif (salary['to'] is None):
			return (salary['from'])*1.2			
		
def average_salary(vacancies):
	average_salary = 0
	vacancies_processed = 0
	for vacancy in vacancies:
		vacancy_salary = predict_rub_salary(vacancy)
		if vacancy_salary:
			average_salary += vacancy_salary
			vacancies_processed += 1
	average_salary = int(average_salary/vacancies_processed)
	return(vacancies_processed, average_salary)







def get_salary_hh(languages):

	url = 'https://api.hh.ru/vacancies'
	languages_stat = {}
	pages_number = 2

	for language in languages:
		vacancies = []
		page = 0
		while page < pages_number:
			payload = {
					'text' : f'программист {language}',
					'area' : 1,
					'period' : 30,
					'page' : page
			}
			response = requests.get(url, params=payload)
			response.raise_for_status()
			response_json = response.json()
			pages_number = min(pages_number, response_json['pages'])
			vacancies += response_json['items']
			page += 1
		average_salar = average_salary(vacancies)
		language_stat = {
		"vacancies_found" : response_json['found'],
		"vacancies_processed": average_salar[0],
		"average_salary": average_salar[1]
		}
		languages_stat[language] = language_stat
	return(languages_stat)


pprint(get_salary_hh(languages))

