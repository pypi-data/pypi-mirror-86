import requests
import socket

class Erlamsa:
    CONNTYPE_HTTP = 0
    # CONNTYPE_TCP = 1

    url = 'http://127.0.0.1:17771'
    conntype = CONNTYPE_HTTP
    timeout = 5
    token = None
    session = None
    s = None

    def __init__(self, uri, token = None, timeout = 5):
        self.token = token

        self.url = uri
        self.timeout = timeout

        self.s = requests.Session()

        self.s.headers.update({'content-type': 'application/octet-stream'})

    def __create_headers(self, token, session, seed, mutations, patterns, blockscale):
        opts = {}

        if token != None:
            opts.update({'erlamsa-token': token})
        if session != None:
            opts.update({'erlamsa-session': session})
        if seed != None:
            opts.update({'erlamsa-seed': seed})
        if mutations != None:
            opts.update({'erlamsa-mutations': mutations})
        if patterns != None:
            opts.update({'erlamsa-patterns': patterns})
        if blockscale != None:
            opts.update({'erlamsa-blockscale': blockscale})

        return opts

    def call(self, data, seed = None, mutations = None, patterns = None, blockscale = None):
        try:
            token = self.token

            if self.session != None:
                token = None

            headers = self.__create_headers(token, self.session, seed, mutations, patterns, blockscale)

            r = self.s.post(self.url + '/erlamsa/erlamsa_esi:fuzz', timeout = self.timeout, data = data, headers = headers)
            
            fuzzed_string = r.text

            if r.status_code == 200:
                if r.headers['erlamsa-status'] == "401":
                    if self.session == None:
                        raise ErlamsaNotAuthorized("Invalid token!")
                    else:
                        self.session = None
                        return (False, data)
                if r.headers['erlamsa-status'] == "500":
                    raise ErlamsaInvalidParams("Invalid parameters")
                else:
                    if r.headers.get('erlamsa-session'):
                        self.session = r.headers['erlamsa-session']
                    return (True, fuzzed_string)
            else:
                return (False, data)

        except socket.timeout:
            return (False, data)

class Error(Exception):
    pass

class ErlamsaNotAuthorized(Error):
    def __init__(self, message):
        self.message = message

class ErlamsaInvalidParams(Error):
    def __init__(self, message):
        self.message = message