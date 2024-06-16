from wsgiref.simple_server import make_server
import json
from datetime import datetime
import pytz


def LAb1App(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    status = ''
    headers = ''
    response_body = ''

    if method == 'GET':
        tz_name = path[1:]

        time = datetime.now(pytz.timezone(tz_name if tz_name else 'GMT'))

        response_body = time.strftime("%Y-%m-%d %H:%M:%S")
        status = '200 OK'
        headers = [('Content-type', 'text/html')]

    elif method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        if path == '/api/v1/convert':
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)

            date = datetime.strptime(data['date'], "%m.%d.%Y %H:%M:%S")
            tz = pytz.timezone(data['tz'])
            target_tz = pytz.timezone(data['target_tz'])

            convertedTime = tz.localize(date).astimezone(target_tz)

            response_body = convertedTime.strftime("%Y-%m-%d %H:%M:%S")
            status = '200 OK'
            headers = [('Content-type', 'application/json')]

        elif path == '/api/v1/datediff':
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)

            first_date = datetime.strptime(data['first_date'], "%m.%d.%Y %H:%M:%S")
            second_date = datetime.strptime(data['second_date'], "%I:%M%p %Y-%m-%d")
            first_tz = pytz.timezone(data['first_tz'])
            second_tz = pytz.timezone(data['second_tz'])

            first = first_tz.localize(first_date)
            second = second_tz.localize(second_date)

            seconds = abs((first - second).total_seconds())

            response_body = str(seconds)
            status = '200 OK'
            headers = [('Content-type', 'application/json')]

    else:
        status = '404 Not Found'
        response_body = 'Not Found'
        headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response_body.encode('utf-8')]


server = make_server('', 8000, LAb1App)
print("Запуск сервера")
server.serve_forever()