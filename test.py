

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



data_ = json.loads(_read_from_file(r'.\ASINs\B07MW4BR8D.json'))

print('Hi')


