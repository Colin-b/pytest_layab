import responses


class AdamMock:
    """
    Helper to Mock an ADAM Rest server.
    """

    def __init__(self, uri: str):
        """
        Create a Mock that should be used for every test case.

        :param uri: ADAM Rest server URI.
        """
        self.server_uri = uri

    def set_user_groups(self, user: str, *groups) -> 'AdamMock':
        """
        Mock user groups.
        Note that you need to decorate your test case with @responses.activate

        :param user: Name of the user (GAIA identifier)
        :param groups: group identifiers
        """
        already_mocked = [m for m in responses.mock._matches if m.url == f'{self.server_uri}/users/{user}']
        if already_mocked:
            responses.replace(
                url=f'{self.server_uri}/users/{user}',
                method_or_response=responses.GET,
                status=200,
                json=[{'memberOf': groups}]
            )
        else:
            responses.add(
                url=f'{self.server_uri}/users/{user}',
                method=responses.GET,
                status=200,
                json=[{'memberOf': groups}]
            )

        return self


def mock_user_groups(uri: str, user: str, *groups) -> None:
    """
    Mock user groups.

    This function is a helper to avoid creation of an AdamMock class, but if you need to mock
    more than one call you should consider usage of AdamMock class.

    Note that you need to decorate your test case with @responses.activate

    :param uri: ADAM Rest server URI.
    :param user: Name of the user (GAIA identifier)
    :param groups: group identifiers
    """
    AdamMock(uri).set_user_groups(user, *groups)
