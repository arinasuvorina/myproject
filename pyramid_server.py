from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

def index(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    file = open('index.html','r')
    return [file.read().encode()]

def aboutme(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    file = open('about/aboutme.html','r')
    return [file.read().encode()]

class Change(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        page = self.app(environ, start_response)[0].decode()
        numberOfBodyT = page.find('<body>')
        numberOfClBodyT = page.find('</body>')
        if (numberOfBodyT != -1 and numberOfClBodyT != -1):
            up, down = page.split('<body>')
            page = up + '<body>\n' + "\t\t\t<div class='top'>Middleware TOP</div>\n" + down
            up, down = page.split('</body>')
            page = up + "\t\t<div class='bottom'>Middleware BOTTOM</div>\n" + '\t</body>' + down
        else:
            page = "<div class='top'>Middleware TOP</div>" + page + "<div class='bottom'>Middleware BOTTOM</div>"
        return page.encode()


config = Configurator()

config.add_route('index2', '/')
config.add_view(index, route_name = 'index2')

config.add_route('index', '/index.html')
config.add_view(index, route_name = 'index')

config.add_route('aboutme', '/about/aboutme.html')
config.add_view(aboutme, route_name = 'aboutme')

app = config.make_wsgi_app()
my_app = Change(app)

server = make_server('0.0.0.0', 8000, my_app)
server.serve_forever()
