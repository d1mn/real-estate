import asyncio
import logging

from collections import Counter, defaultdict
from optparse import OptionParser

from .socrata_client import SocrataClient


log = logging.getLogger(__name__)


async def run_top_fetcher(client):
    log.info("start")
    sales = await client.get_all_real_estate_sales()
    log.info("received %d objects", len(sales))

    top_price_ratio = get_top_sales_ratio_town_by_year(sales)
    for year in sorted(top_price_ratio.keys()):
        log.info("Top sales ratio in %s year: %s" % (year, top_price_ratio[year]))

    top_volume = get_top_volume_by_year(sales)
    for year in sorted(top_volume.keys()):
        log.info("Top volume in %s year: %s" % (year, top_volume[year]))

    log.info("finish")


def get_top_sales_ratio_town_by_year(sales):
    assessedvalues = defaultdict(Counter)
    saleamounts = defaultdict(Counter)
    for sale in sales:
        assessedvalues[sale.daterecorded.year][sale.town] += sale.assessedvalue
        saleamounts[sale.daterecorded.year][sale.town] += sale.saleamount

    ratios = defaultdict(Counter)
    for year in assessedvalues.keys():
        for town in assessedvalues[year]:
            ratios[year][town] = assessedvalues[year][town] / saleamounts[year][town]

    top = defaultdict(list)
    for year in ratios.keys():
        top[year] = ratios[year].most_common(10)
    return top


def get_top_volume_by_year(sales):
    sales_volume = defaultdict(Counter)
    for sale in sales:
        sales_volume[sale.daterecorded.year][sale.town] += 1

    top = defaultdict(list)
    for year in sales_volume.keys():
        top[year] = sales_volume[year].most_common(10)

    return top


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s")
    parser = OptionParser()
    parser.add_option(
        "-k",
        "--socrata-api-key-id",
        dest="socrata_api_key_id",
        default="",
        type="str",
        help="Socrata API KEY ID. Get from https://data.ct.gov/profile/edit/developer_settings")
    parser.add_option(
        "-s",
        "--socrata-api-key-secret",
        dest="socrata_api_key_secret",
        default="",
        type="str",
        help="Socrata API KEY SECRET. Get from https://data.ct.gov/profile/edit/developer_settings")

    (options, _) = parser.parse_args()

    client = SocrataClient(options.socrata_api_key_id, options.socrata_api_key_secret)
    asyncio.run(run_top_fetcher(client))


if __name__ == "__main__":
    main()
