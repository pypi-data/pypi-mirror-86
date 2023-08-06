About
=====

This module provides the **SitemapRange** class and a tool to allow usage
command-line usage **sitemap_fetch.py**.

The class **SitemapRange** is meant as a generic building block for creating
news aggregating applications where the datasources are [spec-compliant](https://www.sitemaps.org/protocol.html) news websites.

There are some fault-tolerance features included to deal with some inconsistencies in sitemaps.

Install
=======

To install from pypi:

    pip install --user sitemap-range-fetch


Usage
=====

Fetching all news articles on [cnn.com](http://cnn.com) in the past 6 days, and format the result as [JSON](https://en.wikipedia.org/wiki/JSON):

    sitemap_fetch.py --site "https://cnn.com" --format json --daysago 6

More custom filtering can be done by using the **SitemapRange** class can be used

Details
=======

This module is provided as is under [MIT License](https://opensource.org/licenses/MIT).
For extensions, customizations or business inquiries you can [get in touch here](mailto:business@garage-coding.com).
