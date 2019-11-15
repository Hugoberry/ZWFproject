# -*- coding: utf-8 -*-
import json

import redis
import scrapy
from scrapy_redis.spiders import RedisSpider
from urllib.parse import quote
from AppleAPPRedis.items import AppleappItem
from main import num

keyword_key = 'keyword_key_%s' % num
empty_word = 'null'


class AppleSpider(RedisSpider):
    name = 'apple_%s' % num
    allowed_domains = ['apple.com']
    redis_key = 'apple:start_urls'
    start_urls = ['https://itunes.apple.com/search?term=QQ&country=CN&media=software']

    def __init__(self):
        super(AppleSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                item = AppleappItem()
                item['kw'] = kw
                new_url = 'https://itunes.apple.com/search?term={}&country=CN&media=software'.format(quote(kw.replace(' ', '')))
                yield scrapy.Request(url=new_url, callback=self.parse_detail, meta={'item': item})
            except TypeError:
                break

    def parse_detail(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        resultCount = json_text['resultCount']
        if resultCount == '0':
            item = response.meta['item']
            item['resultCount'] = resultCount
            item['screenshotUrls'] = empty_word
            item['ipadScreenshotUrls'] = empty_word
            item['appletvScreenshotUrls'] = empty_word
            item['artworkUrl60'] = empty_word
            item['artworkUrl512'] = empty_word
            item['artworkUrl100'] = empty_word
            item['artistViewUrl'] = empty_word
            item['isGameCenterEnabled'] = empty_word
            item['kind'] = empty_word
            item['features'] = empty_word
            item['supportedDevices'] = empty_word
            item['advisories'] = empty_word
            item['averageUserRatingForCurrentVersion'] = empty_word
            item['trackCensoredName'] = empty_word
            item['languageCodesISO2A'] = empty_word
            item['fileSizeBytes'] = empty_word
            item['contentAdvisoryRating'] = empty_word
            item['userRatingCountForCurrentVersion'] = empty_word
            item['trackViewUrl'] = empty_word
            item['trackContentRating'] = empty_word
            item['genreIds'] = empty_word
            item['releaseDate'] = empty_word
            item['primaryGenreName'] = empty_word
            item['sellerName'] = empty_word
            item['releaseNotes'] = empty_word
            item['primaryGenreId'] = empty_word
            item['currentVersionReleaseDate'] = empty_word
            item['minimumOsVersion'] = empty_word
            item['currency'] = empty_word
            item['wrapperType'] = empty_word
            item['version'] = empty_word
            item['description'] = empty_word
            item['artistId'] = empty_word
            item['artistName'] = empty_word
            item['genres'] = empty_word
            item['price'] = empty_word
            item['bundleId'] = empty_word
            item['formattedPrice'] = empty_word
            item['isVppDeviceBasedLicensingEnabled'] = empty_word
            item['trackName'] = empty_word
            item['trackId'] = empty_word
            item['averageUserRating'] = empty_word
            item['userRatingCount'] = empty_word

        for data in json_text['results']:
            item = response.meta['item']
            item['resultCount'] = resultCount

            if 'screenshotUrls' in data:
                item['screenshotUrls'] = str(data['screenshotUrls'])
            else:
                item['screenshotUrls'] = empty_word

            if 'ipadScreenshotUrls' in data:
                item['ipadScreenshotUrls'] = str(data['ipadScreenshotUrls'])
            else:
                item['ipadScreenshotUrls'] = empty_word

            if 'appletvScreenshotUrls' in data:
                item['appletvScreenshotUrls'] = str(data['appletvScreenshotUrls'])
            else:
                item['appletvScreenshotUrls'] = empty_word

            if 'artworkUrl60' in data:
                item['artworkUrl60'] = str(data['artworkUrl60'])
            else:
                item['artworkUrl60'] = empty_word

            if 'artworkUrl512' in data:
                item['artworkUrl512'] = str(data['artworkUrl512'])
            else:
                item['artworkUrl512'] = empty_word

            if 'artworkUrl100' in data:
                item['artworkUrl100'] = str(data['artworkUrl100'])
            else:
                item['artworkUrl100'] = empty_word

            if 'artistViewUrl' in data:
                item['artistViewUrl'] = str(data['artistViewUrl'])
            else:
                item['artistViewUrl'] = empty_word

            if 'isGameCenterEnabled' in data:
                item['isGameCenterEnabled'] = str(data['isGameCenterEnabled'])
            else:
                item['isGameCenterEnabled'] = empty_word

            if 'kind' in data:
                item['kind'] = str(data['kind'])
            else:
                item['kind'] = empty_word

            if 'features' in data:
                item['features'] = str(data['features'])
            else:
                item['features'] = empty_word

            if 'supportedDevices' in data:
                item['supportedDevices'] = str(data['supportedDevices'])
            else:
                item['supportedDevices'] = empty_word

            if 'advisories' in data:
                item['advisories'] = str(data['advisories'])
            else:
                item['advisories'] = empty_word

            if 'averageUserRatingForCurrentVersion' in data:
                item['averageUserRatingForCurrentVersion'] = str(data['averageUserRatingForCurrentVersion'])
            else:
                item['averageUserRatingForCurrentVersion'] = empty_word

            if 'trackCensoredName' in data:
                item['trackCensoredName'] = str(data['trackCensoredName'])
            else:
                item['trackCensoredName'] = empty_word

            if 'languageCodesISO2A' in data:
                item['languageCodesISO2A'] = str(data['languageCodesISO2A'])
            else:
                item['languageCodesISO2A'] = empty_word

            if 'fileSizeBytes' in data:
                item['fileSizeBytes'] = str(data['fileSizeBytes'])
            else:
                item['fileSizeBytes'] = empty_word

            if 'contentAdvisoryRating' in data:
                item['contentAdvisoryRating'] = str(data['contentAdvisoryRating'])
            else:
                item['contentAdvisoryRating'] = empty_word

            if 'userRatingCountForCurrentVersion' in data:
                item['userRatingCountForCurrentVersion'] = str(data['userRatingCountForCurrentVersion'])
            else:
                item['userRatingCountForCurrentVersion'] = empty_word

            if 'trackViewUrl' in data:
                item['trackViewUrl'] = str(data['trackViewUrl'])
            else:
                item['trackViewUrl'] = empty_word

            if 'trackContentRating' in data:
                item['trackContentRating'] = str(data['trackContentRating'])
            else:
                item['trackContentRating'] = empty_word

            if 'genreIds' in data:
                item['genreIds'] = str(data['genreIds'])
            else:
                item['genreIds'] = empty_word

            if 'releaseDate' in data:
                item['releaseDate'] = str(data['releaseDate'])
            else:
                item['releaseDate'] = empty_word

            if 'primaryGenreName' in data:
                item['primaryGenreName'] = str(data['primaryGenreName'])
            else:
                item['primaryGenreName'] = empty_word

            if 'sellerName' in data:
                item['sellerName'] = str(data['sellerName'])
            else:
                item['sellerName'] = empty_word

            if 'releaseNotes' in data:
                item['releaseNotes'] = str(data['releaseNotes'])
            else:
                item['releaseNotes'] = empty_word

            if 'primaryGenreId' in data:
                item['primaryGenreId'] = str(data['primaryGenreId'])
            else:
                item['primaryGenreId'] = empty_word

            if 'currentVersionReleaseDate' in data:
                item['currentVersionReleaseDate'] = str(data['currentVersionReleaseDate'])
            else:
                item['currentVersionReleaseDate'] = empty_word

            if 'minimumOsVersion' in data:
                item['minimumOsVersion'] = str(data['minimumOsVersion'])
            else:
                item['minimumOsVersion'] = empty_word

            if 'currency' in data:
                item['currency'] = str(data['currency'])
            else:
                item['currency'] = empty_word

            if 'wrapperType' in data:
                item['wrapperType'] = str(data['wrapperType'])
            else:
                item['wrapperType'] = empty_word

            if 'version' in data:
                item['version'] = str(data['version'])
            else:
                item['version'] = empty_word

            if 'description' in data:
                item['description'] = str(data['description'])
            else:
                item['description'] = empty_word

            if 'artistId' in data:
                item['artistId'] = str(data['artistId'])
            else:
                item['artistId'] = empty_word

            if 'artistName' in data:
                item['artistName'] = str(data['artistName'])
            else:
                item['artistName'] = empty_word

            if 'genres' in data:
                item['genres'] = str(data['genres'])
            else:
                item['genres'] = empty_word

            if 'price' in data:
                item['price'] = str(data['price'])
            else:
                item['price'] = empty_word

            if 'bundleId' in data:
                item['bundleId'] = str(data['bundleId'])
            else:
                item['bundleId'] = empty_word

            if 'formattedPrice' in data:
                item['formattedPrice'] = str(data['formattedPrice'])
            else:
                item['formattedPrice'] = empty_word

            if 'isVppDeviceBasedLicensingEnabled' in data:
                item['isVppDeviceBasedLicensingEnabled'] = str(data['isVppDeviceBasedLicensingEnabled'])
            else:
                item['isVppDeviceBasedLicensingEnabled'] = empty_word

            if 'trackName' in data:
                item['trackName'] = str(data['trackName'])
            else:
                item['trackName'] = empty_word

            if 'trackId' in data:
                item['trackId'] = str(data['trackId'])
            else:
                item['trackId'] = empty_word

            if 'averageUserRating' in data:
                item['averageUserRating'] = str(data['averageUserRating'])
            else:
                item['averageUserRating'] = empty_word

            if 'userRatingCount' in data:
                item['userRatingCount'] = str(data['userRatingCount'])
            else:
                item['userRatingCount'] = empty_word

            yield item
