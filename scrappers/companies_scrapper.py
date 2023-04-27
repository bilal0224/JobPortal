"""
Extract company names and links from themanifest.com
"""

import json
from bs4 import BeautifulSoup
from enum import Enum
from utils import simple_connector
from urllib.parse import urlparse


class Status(Enum):
    FAILURE = 0
    OK = 1
    NEXT = 2


class CompaniesScrapper:
    def __init__(self):
        self.base_url = "https://themanifest.com/pk/software-development/companies?page="
        self.current_page = -1
        self.total_pages = 19

    def __conn(self):
        """Establishes the connection with the page, and returns a tuple: (Status, Message or HTML)

        Returns:
            (<enum Status>, String): Status Code with string (which is a simple message or HTML)
        """
        next_page = self.__next_page()
        if next_page == False:
            return (Status.OK, "Scraping Done!")
        else:
            try:
                html = simple_connector(next_page)
                return (Status.NEXT, html)
            except Exception as e:
                breakpoint()
                return (Status.FAILURE, "Error!")

    def __next_page(self):
        """Moves onto the next page's URL

        Returns:
            Union[Boolean, String]: Boolean (False) if no more pages are available. String (URL) otherwise.
        """
        if self.current_page < 20:
            self.current_page += 1
            return self.base_url + str(self.current_page)
        else:
            return False

    def __fetch_data(self, company_card):
        """Fetches the

        Args:
            company_card (bs4.element.Tag): The company card that includes all the company's info.

        Returns:
            (String, String): A tuple containing the company's title and URL.
        """
        company_card = company_card.select('a[class="track-website-visit"]')[0]
        company_name = company_card.get_text().strip()
        company_link = urlparse(company_card["href"])
        company_link = '{uri.scheme}://{uri.netloc}/'.format(uri=company_link)
        return (company_name, company_link)

    def __save_companies(self, companies):
        """Save companies in json format.

        Args:
            companies (dict): Dictionary of all the companies
        """
        with open("companies.json", "w") as output_file:
            json.dump(companies, output_file)

    def run(self):
        """Runner
        """
        companies_dict = {}
        status = Status.NEXT
        while status.name == 'NEXT':
            (status, html) = self.__conn()
            soup = BeautifulSoup(html, "html.parser")

            company_cards = soup.find_all("li", class_="provider-card")
            company_tuples = list(map(self.__fetch_data, company_cards))

            companies_dict.update(dict(company_tuples))
        self.__save_companies(companies_dict)


scrapper = CompaniesScrapper()
scrapper.run()
