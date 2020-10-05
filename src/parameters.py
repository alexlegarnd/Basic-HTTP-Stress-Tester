

class Options:

    def __init__(self):
        self.host = ""
        self.allow_ssl = False
        self.port = 80
        self.path = "/"
        self.thread_number = 5
        self.timeout = 10
        self.one_by_one = False
        self.ignore_available_threads = False
        self.self_signed = False
        self.headers = {}

        