
import aiohttp
import asyncio
import datetime
import logging

try:
    import pandas
except ImportError:
    pandas = None

from collections import namedtuple

from ..client import BaseClient
from ..errors import *
from ..rate_limit import insight_rate_limiter, demo_rate_limiter


logger = logging.getLogger('aionasa.insight')


class InSight(BaseClient):
    """
    Client for NASA Insight Mars weather data.

    In-depth documentation for this API can be found at https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

    Parameters for InSight API:
        - version: The version of this API. Locked to 1.0 currently.
        - feedtype: The format of what is returned. Currently the default is JSON and only JSON works.
    """

    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=insight_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def get(self, feedtype='json', as_json=False):
        """
        Retrieves Mars weather data from the last seven available days.

        :param feedtype: The format of what is returned. Currently the default is JSON and only JSON works.
        :param as_json: Bool indicating whether to return a dict containing the raw returned json data instead of the normal named tuple.
        :return: A pandas DataFrame containing data returned by the API.
        """

        request = f"https://api.nasa.gov/insight_weather/?ver=1.0&feedtype={feedtype}&api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not a success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:

            if not pandas:
                raise PandasNotFound("Package 'pandas' could not be imported. DataFrame data format cannot be used.")

            sol_keys = json.pop('sol_keys')
            validity_checks = json.pop('validity_checks')
            data = {'sol': [], 'AT': [], 'HWS': [], 'PRE': [], 'WD': [], 'Season': [], 'First_UTC': [], 'Last_UTC': [], 'validity_checks': []}
            for sol, sol_data in json.items():
                data['sol'].append(sol)
                for col_name, value in sol_data.items():
                    data[col_name].append(value)
                sol_validity_checks = validity_checks.get(sol)
                if sol_validity_checks:
                    data['validity_checks'].append(sol_validity_checks)
                else:
                    data['validity_checks'].append({})
            
            table = pandas.DataFrame(data)
            return table



