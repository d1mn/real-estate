import logging
from optparse import OptionParser

from .socrata_client import SocrataClient


log = logging.getLogger(__name__)


def run_top_fetcher(client):
    log.info("start")
    sales = client.get_all_real_estate_sales()
    log.info('received %d objects', len(sales))
    log.info("finish")


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
    run_top_fetcher(client)


if __name__ == "__main__":
    main()
