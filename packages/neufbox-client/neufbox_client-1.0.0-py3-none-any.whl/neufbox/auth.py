"""
Auth module
"""


def username_password(username, password):
    """Authenticate with username/password"""
    def get(method):
        if method in ('passwd', 'all'):
            return (username, password)
        raise RuntimeError("username_password does not support 'button' authentication method")

    return get
