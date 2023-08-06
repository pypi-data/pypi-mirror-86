class MarketmanError(Exception):
    """Base Marketman API exception"""

    message = 'Unknown error occurred for {url}. Response content: {content}'

    def __init__(self, url, status, resource_name, content):
        """Initialize the SalesforceError exception
        MarketmanError is the base class of exceptions in python-marketman
        Args:
            url: Marketman URL that was called
            status: Status code of the error response
            resource_name: Name of the Marketman resource being queried
            content: content of the response
        """
        # TODO exceptions don't seem to be using parent constructors at all.
        # this should be fixed.
        # pylint: disable=super-init-not-called
        self.url = url
        self.status = status
        self.resource_name = resource_name
        self.content = content


class MarketmanAuthenticationFailed(MarketmanError):
    """
    Thrown to indicate that authentication with Marketman failed.
    """

    def __init__(self, code, message):
        # TODO exceptions don't seem to be using parent constructors at all.
        # this should be fixed.
        # pylint: disable=super-init-not-called
        self.code = code
        self.message = message

    def __str__(self):
        return '{code}: {message}'.format(code=self.code, message=self.message)
