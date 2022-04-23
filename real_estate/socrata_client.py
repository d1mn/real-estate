from typing import List


class RealEstateSale:
    def __init__(self):
        pass


class SocrataClient:
    def __init__(self, key_id: str, key_secret: str):
        self._key_id = key_id
        self._key_secret = key_secret

    # https://dev.socrata.com/foundry/data.ct.gov/5mzw-sjtu
    def get_all_real_estate_sales(self) -> List[RealEstateSale]:
        print(self._key_id)
        print(self._key_secret)

        return []
