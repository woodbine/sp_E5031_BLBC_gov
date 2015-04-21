# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import urllib
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5031_BLBC_gov"
url = "https://www.barnet.gov.uk/citizen-home/council-and-democracy/finance-and-funding/financial-statements-budgets-and-variance-reports/expenditure-over-gbp-500"

# Set up functions
def convert_mth_strings(mth_string):
    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07',
                     'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    # loop through the months in our dictionary
    for k, v in month_numbers.items():
        #  then replace the word with the number
        mth_string = mth_string.replace(k, v)
    return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('div', {'class': 'document-link'})

for block in blocks:

    link = block.a['href']
    parsed_link = urlparse.urlsplit(link.encode('utf8'))
    parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
    encoded_link = parsed_link.geturl()
    pageUrl = encoded_link.replace("/citizen-home", "https://www.barnet.gov.uk/citizen-home")

    html2 = urllib2.urlopen(pageUrl)
    soup2 = BeautifulSoup(html2)
    ts = soup2.find('div', {'class': 'text-section'})
    fileBlocks = ts.findAll('li')

    for fileBlock in fileBlocks:
        fileUrl = fileBlock.a['href']
        fileUrl = fileUrl.replace("/dam", "https://www.barnet.gov.uk/dam")

        if '.csv' in fileUrl:
            # create the right strings for the new filename
            title = fileBlock.a.contents[0]
            title = title.upper()
            csvYr = title.split(' ')[-1]
            csvMth = title.split(' ')[-2][:3]
            csvMth = convert_mth_strings(csvMth);
            filename = entity_id + "_" + csvYr + "_" + csvMth
            todays_date = str(datetime.now())
            scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date})

            print filename
