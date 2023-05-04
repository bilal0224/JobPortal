"""Scans the company's website for URLs"""

import json
from bs4 import BeautifulSoup
from utils import simple_connector, Status, href_formatter
from pathlib import Path


class CompanyScanner:
    def __init__(self, company_name, company_url, headers=False):
        self.company_name = company_name
        self.company_url = company_url[:-1]
        self.headers = headers

        self.visited_links = set()
        self.all_links = set({self.company_url})
        self.forms = set()

    def __export_data(self, status=Status.OK):
        """Export the fetched URLs and forms

        Args:
            status (self, optional): Defaults to Status.OK.
        """
        if status.name == 'FAILURE':
            print('PANIC SAVE')
        print('\nExporting data\n')
        Path(f'scraped_data/{self.company_name}').mkdir(parents=True, exist_ok=True)

        print('Exporting forms')
        with open(f'scraped_data/{self.company_name}/{self.company_name}.html', 'w') as form_file:
            [form_file.write(tag.prettify()) for tag in list(self.forms)]

        print('Exporting links')
        with open(f'scraped_data/{self.company_name}/{self.company_name}.json', 'w') as links_file:
            json.dump(list(self.visited_links), links_file)

        print('\nDone!\n')
        return

    def __fetch_next_url(self):
        """Fetch the next URL to visit. Pops the next url and adds it to self.visited_links.

        Returns:
            Union[Boolean, String]: False if no url is available. URL if it exists.
        """
        if len(self.all_links) == 0:
            return False
        else:
            next_url = self.all_links.pop()
            self.visited_links.add(next_url)
            return next_url

    def __hrefs_cleanup(self, soup):
        """Fetches all the internal hrefs.

        Args:
            soup (bs4.BeautifulSoup): BeautifulSoup object.

        Returns:
            List[String]: List of internal URLs.
        """
        anchors = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]
        anchors = [href_formatter(a) for a in anchors
                   if ('#' not in a and a.startswith('/'))]
        anchors = [self.company_url + a if a[0] == '/' else a for a in anchors]

        return anchors

    def __fetch_forms(self, soup):
        """Fetches the forms and updates self.forms

        Args:
            soup (bs4.BeautifulSoup): BeautifulSoup object
        """
        forms = soup.find_all('form')
        self.forms.update(forms)

    def __populate_urls_and_forms(self):
        """Main Central function that runs the scraping process. Makes the BeautifulSoup and calls the other helper methods.

        Returns:
            Status: Current status of the scraper,
        """
        link = self.__fetch_next_url()
        if link == False:
            print('No more URLs to visit')
            return Status.OK
        else:
            try:
                if self.headers:
                    soup = BeautifulSoup(
                        simple_connector(link, headers=self.headers), 'html.parser'
                    )
                else:
                    soup = BeautifulSoup(simple_connector(link), 'html.parser')

                self.all_links.update(self.__hrefs_cleanup(soup))
                self.all_links = self.all_links - self.visited_links
                self.__fetch_forms(soup)
                return Status.NEXT
            except Exception as e:
                print('Exception')
                print(e)
                self.__export_data(status=Status.FAILURE)

                return Status.NEXT

    def __scan(self):
        """Starts the scanner.

        Returns:
            Status: Status of the scraper.
        """
        status = self.__populate_urls_and_forms()
        if status.name == 'NEXT':
            return status.NEXT
        elif status.name == 'OK':
            self.__export_data()
            return Status.OK
        else:
            return Status.FAILURE

    def run(self):
        """Entry point to the scrapper."""
        status = Status.NEXT
        while status.name == 'NEXT':
            print(f'\nTotal Links Count: {len(self.all_links)}')
            print(f'Visited Links Count: {len(self.visited_links)}\n')

            status = self.__scan()
