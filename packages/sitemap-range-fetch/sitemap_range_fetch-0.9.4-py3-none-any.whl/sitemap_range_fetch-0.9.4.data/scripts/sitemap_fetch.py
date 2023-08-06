#!python
import argparse
import re
import json
import datetime as dt
from lxml import etree
from datetime import datetime, timedelta
from json import JSONEncoder
from sitemap_range.sitemap_range import SitemapRange

class datetime_encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (dt.date, dt.datetime)):
                return obj.isoformat()

def valid_basic_url(url):
    if not re.match(r"^https?:\/\/",url):
        raise argparse.ArgumentTypeError('url does not start with a protocol')
    return url

def valid_format(f):
    if f not in ["json","xml"]:
        raise argparse.ArgumentTypeError('format is invalid (only xml and json are recognized by this tool)')
    return f

def xml_serialize(d):
    root = etree.Element("articles")
    for article in d:
        node_article = etree.Element("article", url=article["url"], dt=article["dt"].isoformat())
        root.append(node_article)
    return root

parser = argparse.ArgumentParser(description='Tool for extracting articles from news websites')
parser.add_argument('--site', dest='site', action='store', required=True, type=valid_basic_url,
        help='the url for the website')
parser.add_argument('--format', dest='format', action='store', default="json", type=valid_format,
        help='the url for the website')
parser.add_argument('--daysago', dest='daysago', action='store', default=2, type=int,
        help='defines the oldest date of an article that will be selected (default: 2 days ago)')
parser.add_argument('--notz', dest='notz', action='store_true',
        help='strip the timezone from the dates before selection (processing is more fault-tolerant)')
parser.add_argument('--advanced', dest='advanced', action='store_true',
        help='use a more fault-tolerant parser')

args   = parser.parse_args()
start_ = datetime.now() - timedelta(days=args.daysago)
end_   = datetime.now()

opts = {}
opts["notz"] = args.notz
opts["parsing_method"] = "advanced" if args.advanced else "basic"

o = SitemapRange(args.site)
in_range = o.get_articles_in_range(start=start_,end=end_,opts=opts)

if args.format == "json":
    print(json.dumps(in_range,sort_keys=True, indent=4, cls=datetime_encoder))
elif args.format == "xml":
    print(etree.tostring(xml_serialize(in_range), pretty_print=True).decode('utf-8'))

