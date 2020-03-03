from werkzeug.wrappers import Request, Response, ResponseStream
import requests

class middleware():
    '''
    Simple WSGI middleware
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        auth_token = request.headers.environ['HTTP_AUTHORIZATION']
        
        if(requests.get('http://oauth.infralabs.cs.ui.ac.id/oauth/resource', 
            headers={'Authorization': auth_token}).status_code == 200):
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        return res(environ, start_response)