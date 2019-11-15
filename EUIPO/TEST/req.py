# -*- coding: utf-8 -*-

import requests
import time
import csv

url = r'https://euipo.europa.eu/copla//trademark/data/withOppoRelations/'

tmnumber = []

outputfile = open('euiposcrape.csv', 'w', newline='')
outputwriter = csv.writer(outputfile)
outputwriter.writerow(['tmnumber', 'application date', 'registration date',
                       'expiry date', 'application type', 'nature', 'status',
                       'publication date', 'publication number', 'goods', 'owner'])

for tm in tmnumber:

    tmnumber = appdate = regdate = expirydate = apptype = \
        nature = status = firstpubdate = firstpubno = goods = owneraddress = ''

    try:
        json = requests.get(url + tm).json()
    except requests.ConnectionError:
        print('Could not scrape data for ' + tm + '. ' + 'Connection failed.')
        continue

    try:
        message = json['message']
        if message == '404 Not Found':
            print('Could not scrape data for ' + tm + '. ' + \
                  'Search on EUIPO returned no results.')
            continue
    except KeyError:
        pass

    try:
        tmdict = json['entity']
    except KeyError:
        pass

    print('Scraping data for ', tm)
    # Scraping trademark number.
    try:
        tmnumber = tmdict['number']
    except KeyError:
        pass
    # Scraping application date.
    try:
        appdate = time.strftime('%d/%m/%Y', time.gmtime(tmdict['filingdate'] / 1000))
    except (KeyError, ValueError):
        pass
    # Scraping registration date.
    try:
        regdate = time.strftime('%d/%m/%Y', time.gmtime(tmdict['regdate'] / 1000))
    except (KeyError, ValueError):
        pass
    # Scraping trademark expiry date.
    try:
        expirydate = time.strftime('%d/%m/%Y', time.gmtime(tmdict['expirydate'] / 1000))
    except (KeyError, ValueError):
        pass
    # Scraping application type data.
    try:
        apptype = tmdict['feature']
    except KeyError:
        pass
    # Scraping nature of application info.
    try:
        nature = tmdict['kind']
    except KeyError:
        pass
    # Scraping status data.
    try:
        status = tmdict['status']
    except KeyError:
        pass

    # Retrieving details of first publication
    try:
        firstpublist = [next((item for item in tmdict['publications'] if item['section'] == 'A.1'), 'False')]
        if firstpublist != 'False':
            firstpubno = firstpublist[0]['bulletinNumber']

            firstpubdate = time.strftime('%d/%m/%Y', time.gmtime(firstpublist[0]['date'] / 1000))

    except (TypeError, ValueError, KeyError):
        pass
    # Retrieving goods and services data.
    try:
        allgoods = tmdict['gs']['defaultValue']['values']
    except KeyError:
        pass

    goodslist = []

    # Scraping goods data.
    try:
        allgoods = tmdict['gs']['defaultValue']['values']
        for i in allgoods:
            goodslist.append(str(i['number']) + ': ' + i['value'])

        goods = "\n".join(goodslist)

        # Retrieving owner address data.
        owneraddress = tmdict['applicants'][0]['address']['postalAddress']
    except (TypeError, ValueError, KeyError):
        pass

    outputwriter.writerow([tmnumber, appdate, regdate, expirydate, apptype,
                           nature, status, firstpubdate, firstpubno, goods,
                           owneraddress])

outputfile.close()
