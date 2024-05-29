from cgi import parse


def simple_app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        print(environ['REQUEST_METHOD'], environ['PATH_INFO'], "Parametrs:", environ['QUERY_STRING'])
    elif environ['REQUEST_METHOD'] == 'POST':
        print(environ['REQUEST_METHOD'], environ['PATH_INFO'], "body:", (environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))).decode())
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ''

application = simple_app