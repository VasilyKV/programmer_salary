import collections
import requests
from pprint import pprint

languages = ['Python', 'Java', 'Javascript', 'Ruby' ,'PHP' , 'C++', 'C#']


# def predict_rub_salary(vacancy):
# 	salary = vacancy['salary']
# 	if salary:
# 		if salary['currency'] != 'RUR':
# 			return
# 		if (salary['from'] is not None) & (salary['to'] is not None):
# 			return (salary['from'] + salary['to'])/2
# 		elif (salary['from'] is None):
# 			return (salary['to'])*0.8
# 		elif (salary['to'] is None):
# 			return (salary['from'])*1.2			
	

# def average_salary(vacancies):
# 	average_salary = 0
# 	vacancies_processed = 0
# 	for vacancy in vacancies:
# 		vacancy_salary = predict_rub_salary(vacancy)
# 		if vacancy_salary:
# 			average_salary += vacancy_salary
# 			vacancies_processed += 1
# 	average_salary = int(average_salary/vacancies_processed)
# 	return(vacancies_processed, average_salary)

def get_salary(payment_from, payment_to):
		if payment_from and payment_to:
			return (payment_from + payment_to)/2
		elif payment_to:
			return payment_to*0.8
		elif payment_from:
			return payment_from*1.2			


def predict_rub_salary_hh(vacancies):
	salary_sum = 0
	vacancies_processed = 0
	for vacancy in vacancies:
		salary = vacancy['salary']
		if salary:
			vacancy_salary = get_salary(salary['from'] , salary['to'])
			if salary['currency'] == 'RUR'and vacancy_salary:
				salary_sum += vacancy_salary
				vacancies_processed += 1
	average_salary = int(salary_sum/vacancies_processed)
	return(vacancies_processed, average_salary)

def predict_rub_salary_sj(vacancies):
	salary_sum = 0
	vacancies_processed = 0
	for vacancy in vacancies:
		vacancy_salary = get_salary(vacancy['payment_from'] , vacancy['payment_to'])
		if vacancy['currency'] == 'rub' and vacancy_salary:
				salary_sum += vacancy_salary
				vacancies_processed += 1
	average_salary = int(salary_sum/vacancies_processed)
	return(vacancies_processed, average_salary)


def get_salary_hh(languages):

	url = 'https://api.hh.ru/vacancies'
	payload = {
			'text' : '',
			'area' : 1,
			'period' : 30,
			'page' : 0
			}	
	languages_stat = {}

	for language in languages:
		payload['text'] = f'программист {language}'
		vacancies = []
		page = 0
		pages_number = 10
		while page < pages_number:
			payload['page'] = page 
			response = requests.get(url, params=payload)
			response.raise_for_status()
			response_json = response.json()
			pages_number = min(pages_number, response_json['pages'])
			vacancies += response_json['items']
			page += 1
		average_salary = predict_rub_salary_hh(vacancies)
		language_stat = {
		"vacancies_found" : response_json['found'],
		"vacancies_processed": average_salary[0],
		"average_salary": average_salary[1]
		}
		languages_stat[language] = language_stat
	return(languages_stat)


# pprint(get_salary_hh(languages))
def get_salary_sj(languages):
	key_sj = 'v3.r.136715645.229b495365993c82076dca1d4673d5143fc5ca03.6431b147f94cb4885f30f18f33878aa21ca9da05'

	url = 'https://api.superjob.ru/2.0/vacancies/'
	request_headers = {
	    'X-Api-App-Id': key_sj
	}
	payload = {
		'keyword' : 'программист Python',
		'town' : 4,
		'period' : 7,
		'page' : 0
	}
	
	languages_stat = {}
	for language in languages:
		payload['keyword'] = f'программист {language}'
		vacancies = []
		page = 0
		pages_number = 100
		more_page = True
		while page < pages_number and more_page:
			payload['page'] = page 
			response = requests.get(url, headers=request_headers, params=payload)
			response.raise_for_status()
			response_json = response.json()
			more_page = response_json['more']
			vacancies += response_json['objects']
			page += 1

		average_salary = predict_rub_salary_sj(vacancies)
		language_stat = {
		"vacancies_found" : response_json['total'],
		"vacancies_processed": average_salary[0],
		"average_salary": average_salary[1]
		}
		languages_stat[language] = language_stat
	return(languages_stat)

pprint(get_salary_sj(languages))
# pprint(response_json)
