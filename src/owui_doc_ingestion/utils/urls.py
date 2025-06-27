from urllib.parse import urlparse, quote

# From https://stackoverflow.com/questions/52359488/update-add-username-in-url-in-python
def set_url_username_password(url, username, password):
    """
    Sets the URL, username, and password for authentication or configuration purposes.

    This function allows you to assign the provided URL, username, and password. It can be used
    in contexts where credentials and endpoint configuration are required, ensuring proper
    assignment for further operations.

    :param url: The target URL to configure.
    :type url: str
    :param username: The username for authentication.
    :type username: str
    :param password: The password for authentication.
    :type password: str
    :return: None
    """
    _username = quote(username)
    _password = quote(password)
    _url = urlparse(url)
    _netloc = _url.netloc.split('@')[-1]
    _url = _url._replace(netloc=f'{_username}:{_password}@{_netloc}')
    return _url.geturl()