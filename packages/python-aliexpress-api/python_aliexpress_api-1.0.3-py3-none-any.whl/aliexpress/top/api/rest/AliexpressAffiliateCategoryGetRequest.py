'''
Created by auto_sdk on 2020.03.09
'''
from aliexpress.top.api.base import RestApi
class AliexpressAffiliateCategoryGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None

	def getapiname(self):
		return 'aliexpress.affiliate.category.get'
