

class Options:

    def __init__(self):
        self.host = ""
        self.allow_ssl = False
        self.port = 80
        self.path = "/"
        self.request_number = 5
        self.limit = 1500
        self.timeout = 10
        self.one_by_one = False
        self.no_limit = False
        self.self_signed = False
        self.headers = {}

        