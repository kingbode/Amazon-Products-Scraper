

class Amazon_Product(object):


    def __init__(self, Product_ASIN=None, Product_Title=None, Product_URL=None, Product_All_Reviews_URL=None,
                 Product_Positive_Reviews_URL=None, Product_Critical_Reviews_URL=None,
                 Product_No_Of_Postivie_Reviewes=None, Product_No_Of_Critical_Reviewes=None, Product_Questions_URL=None
                 ):
        self.Product_ASIN = Product_ASIN
        self.Product_Title = Product_Title
        self.Product_URL = Product_URL

        self.Product_All_Reviews_URL = Product_All_Reviews_URL
        self.Product_Positive_Reviews_URL = Product_Positive_Reviews_URL
        self.Product_Critical_Reviews_URL = Product_Critical_Reviews_URL
        self.Product_No_Of_Postivie_Reviewes = Product_No_Of_Postivie_Reviewes
        self.Product_No_Of_Critical_Reviewes = Product_No_Of_Critical_Reviewes

        self.Product_Questions_URL = Product_Questions_URL







