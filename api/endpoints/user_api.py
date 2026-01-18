from api.client.api_client import ApiClient


class UserAPI(ApiClient):

    def get_users(self):
        return self.get("/users")

    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")

    def create_user(self, payload):
        return self.post("/users", payload)

    def update_user(self, user_id, payload):
        return self.put(f"/users/{user_id}", payload)

    def delete_user(self, user_id):
        return self.delete(f"/users/{user_id}")
