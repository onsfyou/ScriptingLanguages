import requests
import json

def testGET(tz_name):
    response = requests.get('http://localhost:8000/' + tz_name)
    print('GET ', tz_name, response.text)

def testConvert(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8000/api/v1/convert', data=json.dumps(data), headers=headers)
    print('POST-convert', response.text)

def testDiff(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8000/api/v1/datediff', data=json.dumps(data), headers=headers)
    print('POST-diff', response.text)

testGET('Asia/Barnaul')
testGET('Europe/Moscow')

data = {
    'date': '12.20.2021 22:21:05',
    'tz': 'EST',
    'target_tz': 'Asia/Barnaul'
}
testConvert(data)
data = {
    'date': '09.01.2024 22:21:05',
    'tz': 'EST',
    'target_tz': 'Europe/Moscow'
}
testConvert(data)

data = {
    'first_date': '12.06.2024 22:21:05',
    'first_tz': 'EST',
    'second_date': '12:30pm 2024-12-30',
    'second_tz': 'Asia/Barnaul'
}
testDiff(data)
data = {
    'first_date': '01.06.2021 22:21:05',
    'first_tz': 'EST',
    'second_date': '3:33pm 2022-10-06',
    'second_tz': 'Europe/Moscow'
}
testDiff(data)

