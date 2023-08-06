'''
Created by auto_sdk on 2020.09.14
'''
from aliexpress.top.api.base import RestApi
class AliexpressAffiliateProductQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.category_ids = None
		self.delivery_days = None
		self.fields = None
		self.keywords = None
		self.max_sale_price = None
		self.min_sale_price = None
		self.page_no = None
		self.page_size = None
		self.platform_product_type = None
		self.ship_to_country = None
		self.sort = None
		self.target_currency = None
		self.target_language = None
		self.tracking_id = None

	def getapiname(self):
		return 'aliexpress.affiliate.product.query'
