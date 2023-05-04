from company_urls_scanner import CompanyScanner
from utils import HEADERS
import json

def read_company_names_and_urls():
    f = open('companies.json')
    data = json.load(f)
    f.close()

    return data

def entry():
    for company_name, company_url in read_company_names_and_urls().items():
        try:
            print(f'\n\n\nCompany Name: {company_name} || Company URL: {company_url}\n\n\n')
            company_scanner = CompanyScanner(company_name=company_name, company_url=company_url, headers=HEADERS.header_one)
            company_scanner.run()
            del company_scanner
        except Exception as e:
            print('Exception in big_scrapper_script.py')
            print(e)

entry()
