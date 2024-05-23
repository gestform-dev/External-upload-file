class EmailConfig:
    def __init__(self, user: any, filename:any = None, document_error: any = None):
        self.user = user
        self.filename = filename
        self.deposit_date = None
        self.link = None
        self.document_error = document_error
        self.company = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __getitem__(self, key):
        return self.__dict__[key]
