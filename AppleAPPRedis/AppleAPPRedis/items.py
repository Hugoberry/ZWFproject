# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppleappItem(scrapy.Item):
    kw = scrapy.Field()
    resultCount = scrapy.Field()
    screenshotUrls = scrapy.Field()
    ipadScreenshotUrls = scrapy.Field()
    appletvScreenshotUrls = scrapy.Field()
    artworkUrl60 = scrapy.Field()
    artworkUrl512 = scrapy.Field()
    artworkUrl100 = scrapy.Field()
    artistViewUrl = scrapy.Field()
    isGameCenterEnabled = scrapy.Field()
    kind = scrapy.Field()
    features = scrapy.Field()
    supportedDevices = scrapy.Field()
    advisories = scrapy.Field()
    averageUserRatingForCurrentVersion = scrapy.Field()
    trackCensoredName = scrapy.Field()
    languageCodesISO2A = scrapy.Field()
    fileSizeBytes = scrapy.Field()
    contentAdvisoryRating = scrapy.Field()
    userRatingCountForCurrentVersion = scrapy.Field()
    trackViewUrl = scrapy.Field()
    trackContentRating = scrapy.Field()
    genreIds = scrapy.Field()
    releaseDate = scrapy.Field()
    primaryGenreName = scrapy.Field()
    sellerName = scrapy.Field()
    releaseNotes = scrapy.Field()
    primaryGenreId = scrapy.Field()
    currentVersionReleaseDate = scrapy.Field()
    minimumOsVersion = scrapy.Field()
    currency = scrapy.Field()
    wrapperType = scrapy.Field()
    version = scrapy.Field()
    description = scrapy.Field()
    artistId = scrapy.Field()
    artistName = scrapy.Field()
    genres = scrapy.Field()
    price = scrapy.Field()
    bundleId = scrapy.Field()
    formattedPrice = scrapy.Field()
    isVppDeviceBasedLicensingEnabled = scrapy.Field()
    trackName = scrapy.Field()
    trackId = scrapy.Field()
    averageUserRating = scrapy.Field()
    userRatingCount = scrapy.Field()
