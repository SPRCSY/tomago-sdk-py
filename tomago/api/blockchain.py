"""
Copyright ArxanFintech Technology Ltd. 2018 All Rights Reserved.

根据Apache许可证2.0版（“许可证”）获得许可;
除非符合许可，否则您不得使用此文件。
您可以在以下位置获取许可证副本：

                 http://www.apache.org/licenses/LICENSE-2.0

除非适用法律要求或书面同意，否则根据许可证分发的软件按“原样”分发，不附带任何明示或暗示的担保或条件。
有关管理许可下的权限和限制的特定语言，请参阅许可证.
"""

import json
from rest.api.common import APIKEYHEADER, ROUTETAG
from common import VERSION

class BlockChain(object):
    """区块链客户端实现."""

    def __init__(self, client):
        """用Client初始化区块链客户端."""

        self.__route_tag = "tomago"
        self.__path = "blockchain"
        self.__client = client


    def __set_header(self, header):
        """设置钱包客户端header"""

        if APIKEYHEADER not in header:
            header[APIKEYHEADER] = self.__client.get_apikey()
        if ROUTETAG not in header:
            header[ROUTETAG] = self.__route_tag

        return header


    def __set_params(self, header, req_path, url_params={}, body={}):
        header = self.__set_header(header)
        if req_path:
            request_url = "/".join([
                    self.__client.get_ip(),
                    self.__route_tag,
                    VERSION,
                    self.__path,
                    req_path 
                    ])
        else:
            request_url = "/".join([
                    self.__client.get_ip(),
                    self.__route_tag,
                    VERSION,
                    self.__path,
                    ])
        if url_params:
            params = "&".join("{}={}".format(x, url_params[x]) \
                    for x in url_params)
            request_url = "?".join([request_url, params])

        self.__client.set_url(request_url)
        req_params = {
                "body": body,
                "headers": header
                }
        return req_params


    def invoke(self, header, body):
        """激活一条区块链."""

        req_path = "blockchain/invoke"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )


    def query(self, header, body):
        """对区块链状态进行状态询问"""

        req_path = "blockchain/query"
        method = self.__client.do_post
        req_params = self.__set_params(
                header,
                req_path,
                body=body
                )
        return self.__client.do_request(
                req_params,
                method
                )


    def query_txn(self, header, txnid):
        """查询一条区块链中的交易状态。"""

        req_path = "blockchain/query/" + txnid 
        method = self.__client.do_get
        req_params = self.__set_params(
                header,
                req_path
                )
        return self.__client.do_request(
                req_params,
                method
                )

