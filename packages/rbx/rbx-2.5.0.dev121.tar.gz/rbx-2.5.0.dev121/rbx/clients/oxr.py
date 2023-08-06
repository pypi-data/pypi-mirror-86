import logging

import requests
from requests.exceptions import ConnectionError, Timeout

logger = logging.getLogger(__name__)


class OXRClient:
    """A simple HTTP client to retrieve currency exchange rates.

    See https://docs.openexchangerates.org/docs/latest-json for the implementation doc.
    """
    LATEST_ENDPOINT = 'https://openexchangerates.org/api/latest.json'
    TIMEOUT = 5

    def __init__(self, app_id):
        self.app_id = app_id

    def latest(self, currencies):
        """Get the latest exchange rates available from the Open Exchange Rates API.

        Note that all rates are based on USD and this base currency is also given in the rates
        object by default.

        Usage:
        >>> client = OXRClient(app_id='92db86.........')
        >>> client.latest(['GBP', 'EUR'])
        {'EUR': 0.876002, 'GBP': 0.788209, 'USD': 1}

        """
        return self._get(url=self.LATEST_ENDPOINT, currencies=currencies)

    def _get(self, url, currencies):
        """Get currency exchange rates.

        The default base currency of the Open Exchange Rates API is US Dollars (USD).
        """
        if not currencies:
            logger.error('At least 1 currency is required.')
            return {}

        params = {
            'app_id': self.app_id,
            'symbols': ','.join(currencies),
            'timeout': self.TIMEOUT,
        }

        try:
            response = requests.get(url, params=params)
        except (ConnectionError, Timeout):
            logger.error('Error connecting to OXR', extra={
                'params': params,
                'url': url,
            })
            return {}

        if response.status_code >= 400 and response.status_code < 500:
            logger.error(response.json()['description'], extra={
                'params': params,
                'response': response.json(),
                'url': url,
            })
            return {}

        if response.status_code != 200:
            logger.error(response.text, extra={
                'params': params,
                'response': response.json(),
                'url': url,
            })
            return {}

        return response.json()['rates']
