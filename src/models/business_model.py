from dataclasses import dataclass, asdict, field
from datetime import date
import pandas as pd


@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None


@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    date_actual = date.today()
    date_actual = date_actual.strftime('%d-%m-%Y')

    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep='')

    def save_to_excel(self, filename):
        self.dataframe().to_excel(f'./files/excel/{filename}-{self.date_actual}.xlsx', index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f'./files/excel/{filename}-{self.date_actual}.csv', index=False)
