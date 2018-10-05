import responses


class AdamMock:
    """
    Helper to Mock an ADAM Rest server.
    """

    def __init__(self, uri: str):
        self.server_uri = uri

    def add_user_groups(self, user: str, *groups):
        responses.add(
            url=f'{self.server_uri}/users/{user}',
            method=responses.GET,
            status=200,
            json=[{'memberOf': groups}]
        )

    def replace_user_groups(self, user: str, *groups):
        responses.replace(
            url=f'{self.server_uri}/users/{user}',
            method_or_response=responses.GET,
            status=200,
            json=[{'memberOf': groups}]
        )
