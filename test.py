

import json


def _read_from_file(fname):
    try:
        # to load json file without errors or exception , I added encoding='utf-8'
        with open(fname, 'r',encoding='utf-8') as infile:
            res = infile.read()
            # return json.loads(res)
            return res
    except Exception as ex_:
        print(ex_)
        return {}

def _write_to_file(fname, _data):
    try:
        with open(fname, 'w',encoding='utf-8') as out_file:
            out_file.write(_data)
            out_file.close()
    except:
        print('could not save this file')



# data_ = json.loads(_read_from_file(r'.\ASINs\B07MW4BR8D.json'))

import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--days', required=True,  help="Check mapped inventory that is x days old", default=None)
parser.add_argument('-e', '--event', required=False, action="store", dest="event_id",
                    help="Check mapped inventory for a specific event", default=None)
parser.add_argument('-b', '--broker', required=False, action="store", dest="broker_id",
                    help="Check mapped inventory for a broker", default=None)
parser.add_argument('-k', '--keyword', required=False, action="store", dest="event_keyword",
                    help="Check mapped inventory for a specific event keyword", default=None)
parser.add_argument('-p', '--product', required=False, action="store", dest="product_id",
                    help="Check mapped inventory for a specific product", default=None)
parser.add_argument('-m', '--metadata', required=False, action="store", dest="metadata",
                    help="Check mapped inventory for specific metadata, good for debugging past tix", default=None)
parser.add_argument('-u', '--update', required=False, action="store_true", dest="make_updates",
                    help="Update the event for a product if there is a difference, default No", default=False)
args = parser.parse_args()

days = args.days
event_id = args.event_id
broker_id = args.broker_id
event_keyword = args.event_keyword
product_id = args.product_id
metadata = args.metadata
make_updates = args.make_updates

no_change_counter = 0
change_counter = 0

req_arg = bool(days) + bool(event_id) + bool(broker_id) + bool(product_id) + bool(event_keyword) + bool(metadata)
if not req_arg:
    print("Need to specify days, broker id, event id, event keyword or past tickets full metadata")
    parser.print_help()
    sys.exit()
elif req_arg != 1:
    print("More than one option specified. Need to specify only one required option")
    parser.print_help()
    sys.exit()



print('Hi')
