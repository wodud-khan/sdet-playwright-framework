class UserFactory:
    @staticmethod
    def valid_user():
        return {
            "username": "standard_user",
            "password": "secret_sauce"
        }

    @staticmethod
    def invalid_user():
        return {
            "username": "invalid_user",
            "password": "wrong_password"
        }
