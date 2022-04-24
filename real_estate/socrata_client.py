from datetime import datetime
import logging

import aiohttp
from collections import namedtuple
from dateutil import parser
from typing import List

from .util import retry


log = logging.getLogger(__name__)


RealEstateSale = namedtuple(
    "RealEstateSale",
    [
        "serialnumber", "listyear", "daterecorded", "town",
        "assessedvalue", "saleamount", "salesratio",
    ],
)


class SocrataClient:
    REAL_ESTATE_SALES_ENDPOINT = "https://data.ct.gov/resource/5mzw-sjtu.json"

    def __init__(self, key_id: str, key_secret: str):
        self._key_id = key_id
        self._key_secret = key_secret

    async def get_real_estate_sales(self, limit: int, offset: int) -> List[RealEstateSale]:
        params = [
            ("$limit", limit),
            ("$offset", offset),
        ]
        sales = []
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self._key_id, self._key_secret),
                                         headers={"User-Agent": "curl/7.77.0"}) as session:
            async with session.get(self.REAL_ESTATE_SALES_ENDPOINT, params=params) as resp:
                if resp.status >= 400:
                    raise Exception("request failed with status code: %d" % resp.status)
                json_data = await resp.json()

                for item in json_data:
                    if "daterecorded" not in item:
                        log.warn("field 'daterecorded' is found in sale: %s" % item)
                        continue

                    sales.append(RealEstateSale(
                        item["serialnumber"],
                        item["listyear"],
                        parser.parse(item["daterecorded"]),
                        item["town"],
                        float(item["assessedvalue"]),
                        float(item["saleamount"]),
                        float(item["salesratio"]),
                    ))
        return sales

    async def get_all_real_estate_sales(self) -> List[RealEstateSale]:
        all_sales = []
        limit = 100000
        page = 0
        while True:
            sales = await retry(self.get_real_estate_sales, (limit, page * limit), times=3, sleep_ms=50)
            if len(sales) == 0:
                break
            all_sales += [*sales]
            page += 1

        return all_sales
