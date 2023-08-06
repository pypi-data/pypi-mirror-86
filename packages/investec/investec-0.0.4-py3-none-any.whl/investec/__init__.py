
class AbstractAuth:

    def __init__(self, token):
        self.token = token

        self.header = None
        self.host = "openapi.investec.com"
        self.domain = "za"
        self.api = "pb"
        self.version = "v1"
        self.accounts = "accounts"
        self.balance = "accounts{accountId}/balance"
