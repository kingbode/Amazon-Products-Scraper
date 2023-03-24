Amazon-Products
=============================

take Amazon Product ASIN and retrieve , Product Profile , Reviews and Questions

Introduction:
=============================

this project takes Amazon Product ASIN ( something like Product reference for Amazon),

and get all details about the product Reviews and Questions about it from the customers

Amazon_Asin_V1.0.py:
=============================

I could read all the product reviews ( Positive and Critical ) ones, using selenium

I created Review Items

I created Product Items

=============================

Amazon_Asin_V1.2.py
=============================

I will use direct links extracted rather than extracting them using selenim actions, for Positive and Critical Reviews

=============================

Amazon_Asin_V1.4.py
=============================

I fixed the json format output by adding .dict for each object before appending to the Data_ variable that will be used later to output the json file.

=============================

Amazon_Asin_V1.5.py
=============================

I could get from main page extract all links for Reviews pages , and Question pages ( actually it is a fixed URL for questions)

then use these links to go for each page and fetch the data for each scope

rather than doing automation from main page to get the links then click on them, I think this is faster !!

I work now on fetching questions !!.............. Done

=============================

Amazon_Asin_V1.6.py
=============================

I will enhance the code and remove un-necessary lines
in Amazon_Asin_V1.7.py

=============================


Amazon_Asin_V1.7.py
=============================
created class for Amzon Function to be called from Amazon_Asin_V1.7.py

=============================


Amazon_Asin_V1.8.py
=============================

created class for Amzon FunctionV3 to be called from Amazon_Asin_V1.8.py

updated finding elements as per Amazon updates

=============================


Amazon_Asin_V1.9.py
=============================

created class for Amzon FunctionV4 to be called from Amazon_Asin_V1.9.py

Added Product Price in Amazon Product Class "Amazon_Product.py"

Added command line to get ASIN number as an input form the command line

Added ASIN availability checker

=============================


Amazon_Asin_V2.0.py
=============================

Created class for Amzon FunctionV5 to be called from Amazon_Asin_V2.0.py

Added command line parameters as below:

Added Parameter to Enter ASIN inthe command line, example -a B07MW4BR8D

Added Parameter to specify number of customers' Reviews pages to collect (option), example:  -r 3

Added Parameter to specify number of customers' Questions pages to collect (option), example:  -q 3

Added Parameter to hide the Browser or display it while fetching the data, example:  -v 1  (to display the Browser) , -v 0 (to hide the Browser)

no need to put parameters in order !!

Example: python Amazon_Asin_V2.0.py -q 2 -r 2 -a B07MW4BR8D -v 1

in this Example, we collect two pages of Reveiws and two pages of Questions for the Produc that has ASIN = B07MW4BR8D
and the Brwoser will be visible , as default is to be invisible

usage: Amazon_Asin_V2.0.py [-h] -a ASIN [-r REVIEWSCOUNT] [-q QUESTIONSCOUNT] [-v HIDEBROWSER]

to get Amazon Product Data, Reviews and Question

optional arguments:

  -h, --help            show this help message and exit

  -a ASIN, --ASIN ASIN  Please enter Amazon ASIN number, -a B07MW4BR8D , Required Parameter

  -r REVIEWSCOUNT, --ReviewsCount REVIEWSCOUNT

	Please enter number of Reviews Pages to collect , Optional Parameter ,if not set, the tool will collect all Product Reviews

  -q QUESTIONSCOUNT, --QuestionsCount QUESTIONSCOUNT

	Please enter Maximum of Questions Pages to collect , Optional Parameter ,if not set, the tool will collect all Product Questions

  -v VIEWBROWSER, --VIEWBROWSER VIEWBROWSER

	to View the Browser, "1" means to View , while "0" means to hide it, as it is default value, and no need to set it to hide it !!



=============================


Amazon_Asin_V2.1.py
=============================

Added the option to output the data in xlsx format as default and json as optional outcome if specified in the command line as -json 1

Demo Video :

https://youtu.be/pbgajFBFbSU 

=============================
