class SmsConfig:
    def __init__(self, user: any):
        self.user = user

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __getitem__(self, key):
        return self.__dict__[key]
