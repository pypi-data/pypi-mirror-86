import sys
import re
import requests
from io import StringIO
from datetime import datetime, timedelta
from lxml.html.soupparser import convert_tree
from bs4 import BeautifulSoup
from lxml import etree
"""

This class extracts articles from sitemaps using time constraints.

The algorithm is composed of the following steps:
1) fetch all "Sitemap:" entries found in robots.txt
2) the entry can be of type sitemapindex or urlset
3.1) if it's an urlset, go over all articles in it, and select
     those within the time range.
3.2) if it's of type sitemapindex, select those in the timerange
4) for the sitemaps that were found in 3.2, fetch them and get the
   articles that are within the given timerange

So steps 3.2 and 4 are handling a simple-nested hierarchy (we're only
handling one level of nesting).

Along the way, a visited_url dictionary is kept updated to skip any
duplicate urls (example: two different tag sitemaps have the same url).

Sitemap hierarchy example:

. robots.txt
.. sitemapindex
... urlset
... urlset
.. sitemapindex
... urlset
.. sitemapindex
... urlset
... urlset
... urlset
.. urlset
.. urlset

Refer to [1] for more details on the sitemap protocol.

[1] https://www.sitemaps.org/protocol.html#sitemapIndex_sitemap

"""
class SitemapRange:

    def __init__(self, domain):
        self.domain = domain

    def get_page(self, url, raw=True):
        r = requests.get(url)
        if raw:
            return r.content
        else:
            return r.text

    def in_range(self,dt,start,end,opts):
        if dt:
            if "notz" in opts and opts["notz"]:
                dt = dt.replace(tzinfo=None)
            if dt >= start and dt <= end:
                return True
        return False

    def get_sitemap_urls(self):
        robots_txt = self.get_page(self.domain + "/robots.txt", raw=False)
        for line in robots_txt.split("\n"):
            g = re.match(r"^Sitemap: (.*)$", line)
            if g and len(g.groups()) > 0:
                sitemap_url = (g.groups())[0]
                yield sitemap_url

    def parse_page(self, url, opts):
        if "parsing_method" not in opts or opts["parsing_method"] == "basic":
            xml = self.get_page(url)
            parse_tree = etree.XML(xml)
            return parse_tree
        elif opts["parsing_method"] == "advanced":
            xml = self.get_page(url)
            soup = BeautifulSoup(xml, "xml")
            parse_tree = (convert_tree(soup))[0]
            parse_tree.getroottree = (lambda : parse_tree)
            return parse_tree

    def handle_sitemapindex(self, parse_tree, start, end, opts):
        if parse_tree is not None:
            for x in parse_tree.getroottree().xpath('.//*[name() = "sitemap"]'):
                y = x.xpath('.//*[name() = "loc"]/text()')
                z = x.xpath('.//*[name() = "lastmod"]/text()')
                if len(z) > 0:
                    z = z[0]
                    if z[-1] == 'Z':
                        z = z[:-1]

                    dt = None
                    try:
                        dt = datetime.fromisoformat(z)
                    except Exception as e:
                        print("ERROR5 " + str(e),file=sys.stderr)
                        continue

                    if self.in_range(dt,start,end,opts):
                        yield({"url": y[0], "dt": dt})

    def handle_urlset(self, parse_tree, start, end, opts):
        if parse_tree is not None:
            for x in parse_tree.getroottree().xpath('.//*[name() = "url"]'):
                y = x.xpath('.//*[name() = "loc"]/text()')
                z1 = x.xpath('.//*[name() = "news:news"]/*[name() = "news:publication_date"]/text()')
                z2 = x.xpath('.//*[name() = "lastmod"]/text()')

                z = None
                if z1 is not None and len(z1) > 0:
                    z = z1
                elif z2 is not None and len(z2) > 0:
                    z = z2

                if z is not None and len(z) > 0:
                    z = z[0]
                    if z[-1] == 'Z':
                        z = z[:-1]

                    dt = None
                    try:
                        dt = datetime.fromisoformat(z)
                    except Exception as e:
                        print("ERROR6 " + str(e),file=sys.stderr)
                        continue

                    if self.in_range(dt,start,end,opts):
                        yield({"url": y[0], "dt": dt})

    def get_articles_in_range(self, start=datetime.now(), end=datetime.now(), opts=None):
        # 1st pass
        articles = []
        sitemaps = []
        visited_url = {}
        for u in self.get_sitemap_urls():
            if u in visited_url: continue
            visited_url[u] = 1

            print("Processing sitemap:"+u, file=sys.stderr)
            parse_tree = None
            try:
                parse_tree = self.parse_page(u,opts)
            except etree.XMLSyntaxError as e:
                print("ERROR1 : " + str(e), file=sys.stderr)
            except Exception as e:
                print("ERROR2 : " + str(e), file=sys.stderr)

            if parse_tree is not None:
                root_tag = parse_tree.tag
                root_tag = re.sub(r"^[^}]+}","",root_tag)
                if root_tag == "sitemapindex":
                    for o in self.handle_sitemapindex(parse_tree, start, end, opts):
                        sitemaps.append(o)
                elif root_tag == "urlset":
                    for o in self.handle_urlset(parse_tree, start, end, opts):
                        articles.append(o)
        # 2nd pass
        for sm in sitemaps:
            if sm["url"] in visited_url: continue
            visited_url[sm["url"]] = 1

            print("Processing sitemap:"+sm["url"], file=sys.stderr)
            parse_tree = None
            try:
                parse_tree = self.parse_page(sm["url"],opts)
            except etree.XMLSyntaxError as e:
                print("ERROR3 : " + str(e), file=sys.stderr)
            except Exception as e:
                print("ERROR4 : " + str(e), file=sys.stderr)

            if parse_tree is not None:
                for o in self.handle_urlset(parse_tree, start, end, opts):
                    articles.append(o)
        
        return articles

