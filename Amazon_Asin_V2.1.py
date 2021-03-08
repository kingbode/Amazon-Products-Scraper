from AmazonFunctionsV5 import load_Procut_Page, remove_Nagging_Window, get_Product_Profile, \
    get_All_Product_Reviews, get_All_PrdocutQuestions, _save_Data_to_JSON , _check_ASIN_Existance, initialize_WebDriver, \
    check_P_I, _save_Data_to_XLSX

from Amazon_Product import Amazon_Product

import time

import argparse

import sys

# print(sys.executable)
# print(sys.path)
#===================================================================
# Handling Application Arguments !!
#===================================================================

args = None

parser = argparse.ArgumentParser(description='to get Amazon Product Data, Reviews and Question')
#-q 10 -r 10 -a B07MW4BR8D -v 1
parser.add_argument('-a', '--ASIN', required=True, type=str,help='Please enter Amazon ASIN number, -a B07MW4BR8D , Required Parameter', default=None)
parser.add_argument('-r', '--ReviewsCount', required=False, type=int,help='Please enter number of Reviews Pages to collect , Optional Parameter ,if not set, the tool will collect all Product Reviews', default=None)
parser.add_argument('-q', '--QuestionsCount',required=False, type=int,help='Please enter Maximum of Questions Pages to collect , Optional Parameter ,if not set, the tool will collect all Product Questions', default=None)
parser.add_argument('-v', '--HideBrowser',required=False, type=int,help='to Hide the Browser, "0" means to Hide , while "1" means to display it, Optional Parameter ,if not set, the Browser will be invisibile', default=None)
parser.add_argument('-json', '--json',required=False, type=int,help='to output the data in JSON format', default=None)



try:
    args = parser.parse_args()

    # print(args)
    # parser.exit(1)

except:
    # here , it means no arguments were entered, so display the Help and exit !!
    print('===================================================================')
    print('Example: >python Amazon_Asin_V2.1.py -q 2 -r 2 -a B07MW4BR8D -v 1')
    print('in this Example, we collect two pages of Reveiws and two pages of Questions for the Produc that has ASIN = B07MW4BR8D')
    print('and the Browser will be invisible')
    print('\nand no need to put parameters in order !!')
    print('===================================================================')
    parser.print_help()
    parser.exit(1)




#===================================================================
# ASIN Search Website
# https://amazon-asin.com/asincheck/?product_id=BO7GKK5FQT

#===================================================================
# Declaring variables
#===================================================================

timeout = 5

#  Arguments example : -A B07MW4BR8D -R 10 -Q 10
# -A B07MW4BR8D
# ASIN_ = 'B07W8YTDDR' #'B07MW4BR8D'  #'B082B597Y6' #'B07KNHQ8NZ' # this is a sample ASIN

# ASIN_ = input('Please Input Amazon Product ASIN : ')
ASIN_ = args.ASIN

if(check_P_I(args.ReviewsCount)):
    Reviews_limit = args.ReviewsCount
else:
    Reviews_limit = None

if(check_P_I(args.QuestionsCount)):
    Question_limit = args.QuestionsCount
else:
    Question_limit = None

if(args.HideBrowser == None):
    _to_HideBrowser=True
else:
    if(check_P_I(args.HideBrowser)):
        _to_HideBrowser = bool(args.HideBrowser)
    else:
        _to_HideBrowser = True


if(check_P_I(args.json)):
    _to_JSON = bool(args.json)



Amazon_URL_ = 'https://www.amazon.com'

ASIN_baseURL_ = 'https://www.amazon.com/dp/'


full_URL = ASIN_baseURL_ + ASIN_

_ASIN_Validity = False

Rating_ = '★★★★★'

totalNumberOfReviews = 0

Positive_Reviews_Count = 0

Critical_Reviews_Count = 0

Amazon_Product_Data = []

Reviews_List = []

Questions_List = []

Amazon_Product_ = Amazon_Product()

# Chrome_Driver_Path = r'.\chromedriver.exe'

headers_ = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}


#==========================================================================================================
# Process time measuring
start_time = time.time()
#==========================================================================================================
#==========================================================================================================
#=============================================== Main Application =========================================
#==========================================================================================================

# 0- Checking ASIN Validity:

_ASIN_Validity = _check_ASIN_Existance(full_URL)



# 1- Initialize Web Driver:

if _ASIN_Validity:
    print('- Valid Product ASIN is being processed')

    driver_ = initialize_WebDriver(_to_HideBrowser)

    # driver.get(URL_)
    # driver_ = initialize_WebDriver(Chrome_Driver_Path)

    #==========================================================================================================
    # 2- Visiting main Link of a given ASIN
    #==========================================================================================================

    load_Procut_Page(full_URL,driver_)

    #==========================================================================================================
    # 3- bypassing nagging popup window for local country
    #==========================================================================================================

    remove_Nagging_Window(driver_)

    #===========================================================================
    # Now use the Main Product Page to get all the Fields of Amazon_Product Object
    # meaning all URLs required to visit , to save time going back and forth, or trying to find them using Selenium
    #===========================================================================
    # 4- Get Amazon Product Profile
    #===========================================================================

    Amazon_Product_ = get_Product_Profile(driver_,ASIN_)


    Amazon_Product_Data.append({'Amazon Product Profile':Amazon_Product_.__dict__})
    #===========================================================================
    #Starting Scrapping
    #===========================================================================

    #===========================================================================
    # 5- Loading the Page of All Reviews of the Product !!!
    #===========================================================================

    Reviews_List = get_All_Product_Reviews(driver_,Amazon_Product_,Reviews_limit)

    #===========================================================================
    # Saving All Reviews details about the Product in Amazon_Product_Data !!!
    #===========================================================================

    Amazon_Product_Data.append({'Amazon Product Reviews':Reviews_List})
    #===========================================================================

    #===========================================================================
    # 6- Loading the Page of All Questions about the Product !!!
    #===========================================================================

    Questions_List = get_All_PrdocutQuestions(driver_,Amazon_Product_,Question_limit)

    #==============================================================================

    #===========================================================================
    # Saving All Questions details about the Product in Amazon_Product_Data !!!
    #===========================================================================

    Amazon_Product_Data.append({'Amazon Product Questions':Questions_List})

    #===========================================================================

    #===========================================================================
    # output the data as json file
    #===========================================================================
    if(_to_JSON):
        _save_Data_to_JSON('.\ASINs\\' + ASIN_+ '.json', Amazon_Product_Data)

    # ===========================================================================
    # output the data as XLSX file
    # ===========================================================================
    if (Amazon_Product_Data):
        _save_Data_to_XLSX('.\ASINs\\' + ASIN_ + '.xlsx', Amazon_Product_Data)

    # ===========================================================================
    # here we get how much time is taken to execute this process

    driver_.close()

    print("--- %s seconds ---" % (time.time() - start_time))


else:
    print('- Product ASIN seems to be invalid or no longer exists in Amazon database')

    print('hi')

