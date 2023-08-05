# coding: utf-8

"""
    Mainnet Cash

    A developer friendly bitcoin cash wallet api  This API is currently in active development, breaking changes may be made prior to official release of version 1.  **Important:** This library is in active development   # noqa: E501

    The version of the OpenAPI document: 0.0.2
    Contact: hello@mainnet.cash
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import mainnet
from mainnet.models.send_max_response import SendMaxResponse  # noqa: E501
from mainnet.rest import ApiException

class TestSendMaxResponse(unittest.TestCase):
    """SendMaxResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SendMaxResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mainnet.models.send_max_response.SendMaxResponse()  # noqa: E501
        if include_optional :
            return SendMaxResponse(
                tx_id = '1e6442a0d3548bb4f917721184ac1cb163ddf324e2c09f55c46ff0ba521cb89f', 
                balance = mainnet.models.zero_balance_response.ZeroBalanceResponse(
                    bch = 0, 
                    sat = 0, 
                    usd = 0, )
            )
        else :
            return SendMaxResponse(
        )

    def testSendMaxResponse(self):
        """Test SendMaxResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
