

import json
import argparse
import sys
import pandas as pd
from AmazonFunctionsV5 import _Json_to_CSV_Questions, _Json_to_CSV_Reviews

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



def _dicts_to_list(_dicts_list):

    _tmp_list = []
    # add columns as a first list
    _tmp_list.append(list(_dicts_list[0].keys()))

    for _dict in _dicts_list:
        _tmp_list.append(list(_dict.values()))

    return _tmp_list

def initiateArguments():

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



data_ = json.loads(_read_from_file(r'.\ASINs\B07MW4BR8D.json'))


Product_Profile = {}
Product_Reviews = {}
Product_Questions = {}

Product_Profile = data_[0][0]['Amazon Product Profile']
Product_Reviews = data_[0][1]['Amazon Product Reviews']
Product_Questions = data_[0][2]['Amazon Product Questions']
# Add your data in list, which may contain a dictionary with the name of the
# columns as the key
# df1 = pd.DataFrame({'Product_Profile': Product_Profile})
df1 = pd.DataFrame({'Product_Profile': Product_Profile})
# df2 = pd.DataFrame({'Product_Reviews': Product_Reviews[0]})
df2 = pd.DataFrame({'Product_Reviews': Product_Reviews[0]})
# df3 = pd.DataFrame({'Product_Questions': Product_Questions})
df3 = pd.DataFrame({'Product_Questions': Product_Questions})


tmp_2 = _dicts_to_list(Product_Reviews)
tmp_3 = _dicts_to_list(Product_Questions)

df4 = pd.DataFrame(tmp_2)
df5 = pd.DataFrame(tmp_3)

# Create a new excel workbook
writer = pd.ExcelWriter('Product.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='Product_Profile')
df4.to_excel(writer, sheet_name='Product_Reviews',index=False,header=False)
df5.to_excel(writer, sheet_name='Product_Questions',index=False,header=False)

print(df4)
# _Json_to_CSV_Questions(Product_Questions)
# _Json_to_CSV_Reviews(Product_Reviews)
writer.save()
print('Hi')