from responses import RequestsMock


class AdamMock:
    """
    Helper to Mock an ADAM Rest server.
    """

    def __init__(self, uri: str):
        """

        :param uri: ADAM Rest server URI.
        """
        self.server_uri = uri
        self.mock = RequestsMock()

    def set_user_groups(self, user: str, *groups) -> 'AdamMock':
        """
        Mock user groups.

        :param user: Name of the user (GAIA identifier)
        :param groups: group identifiers
        """
        already_mocked = [m for m in self.mock._matches if m.url == f'{self.server_uri}/users/{user}']
        if already_mocked:
            self.mock.replace(
                url=f'{self.server_uri}/users/{user}',
                method_or_response=RequestsMock.GET,
                status=200,
                json=[{'memberOf': groups}]
            )
        else:
            self.mock.add(
                url=f'{self.server_uri}/users/{user}',
                method=RequestsMock.GET,
                status=200,
                json=[{'memberOf': groups}]
            )

        return self


def mock_user_groups(uri: str, user: str, *groups) -> RequestsMock:
    return AdamMock(uri).set_user_groups(user, *groups).mock
