# -*- coding: utf8 -*-
# Copyright (c) 2017-2018 Investoday company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from jrtzcloudsdkcore.abstract_model import AbstractModel


class DescribeEstBscRequest(AbstractModel):
    """DescribeEstBsc 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.OperType = None
        self.SecCd = None
        self.IndId = None
        self.RptYr = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.OperType = params.get("OperType")
        self.SecCd = params.get("SecCd")
        self.IndId = params.get("IndId")
        self.RptYr = params.get("RptYr")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")

class DescribeGrdBscRequest(AbstractModel):
    """DescribeGrdBsc 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.OperType = None
        self.SecCd = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.OperType = params.get("OperType")
        self.SecCd = params.get("SecCd")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")



class DescribeIndFrcstHistRequest(AbstractModel):
    """DescribeIndFrcstHist 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.IndId = None
        self.OperType = None
        self.RptYr = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None
        self.RptRang = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.IndId = params.get("IndId")
        self.OperType = params.get("OperType")
        self.RptYr = params.get("RptYr")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")
        self.RptRang = params.get("RptRang")


class DescribeIduClsRefRequest(AbstractModel):
    """DescribeIduClsRef 请求参数结构体
    """

    def __init__(self):
        self.IduCl = None
        self.IduId = None
        self.QueryTyp = None
        self.IduNm = None
        self.Fields = None

    def _deserialize(self, params):
        self.IduCl = params.get("IduCl")
        self.IduId = params.get("IduId")
        self.QueryTyp = params.get("QueryTyp")
        self.IduNm = params.get("IduNm")
        self.Fields = params.get("Fields")


class DescribeResOrgRefRequest(AbstractModel):
    """DescribeResOrgRef 请求参数结构体
    """

    def __init__(self):
        self.OrgNm = None
        self.OrgCl = None
        self.QueryTyp = None
        self.Fields = None

    def _deserialize(self, params):
        self.OrgNm = params.get("OrgNm")
        self.OrgCl = params.get("OrgCl")
        self.QueryTyp = params.get("QueryTyp")
        self.Fields = params.get("Fields")


class DescribeAnaRankEstIduRequest(AbstractModel):
    """DescribeAnaRankEstIdu 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.IduCl = None
        self.IduId = None
        self.AnaNm = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.IduCl = params.get("IduCl")
        self.IduId = params.get("IduId")
        self.AnaNm = params.get("AnaNm")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeAnaRankGrdRequest(AbstractModel):
    """DescribeAnaRankEstIdu 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.IduCl = None
        self.IduId = None
        self.AnaNm = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.IduCl = params.get("IduCl")
        self.IduId = params.get("IduId")
        self.AnaNm = params.get("AnaNm")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndFrcstAnaemRequest(AbstractModel):
    """DescribeIndFrcstAnaem 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.OperType = None
        self.RptRang = None
        self.RptYr = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.OperType = params.get("OperType")
        self.RptRang = params.get("RptRang")
        self.RptYr = params.get("RptYr")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndFrcstIduemRequest(AbstractModel):
    """DescribeIndFrcstIduem 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.IduCl = None
        self.IduId = None
        self.RptYr = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.IduCl = params.get("IduCl")
        self.IduId = params.get("IduId")
        self.RptYr = params.get("RptYr")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndFrcstTianyanRequest(AbstractModel):
    """DescribeIndFrcstTianyan 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.OperType = None
        self.RptRang = None
        self.RptYr = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.OperType = params.get("OperType")
        self.RptRang = params.get("RptRang")
        self.RptYr = params.get("RptYr")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndRankEqIduRequest(AbstractModel):
    """DescribeIndRankEqIdu 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.OperType = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.OperType = params.get("OperType")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndRankPmRequest(AbstractModel):
    """DescribeIndRankPm 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.OperType = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.OperType = params.get("OperType")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeIndRankRvIduRequest(AbstractModel):
    """DescribeIndRankRvIdu 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.SecCd = None
        self.OperType = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.SecCd = params.get("SecCd")
        self.OperType = params.get("OperType")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")


class DescribeResOrgRankRequest(AbstractModel):
    """DescribeResOrgRank 请求参数结构体
    """

    def __init__(self):
        self.BeginDate = None
        self.EndDate = None
        self.OrgCl = None
        self.Fields = None
        self.PageNo = None
        self.PageSize = None

    def _deserialize(self, params):
        self.BeginDate = params.get("BeginDate")
        self.EndDate = params.get("EndDate")
        self.OrgCl = params.get("OrgCl")
        self.Fields = params.get("Fields")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")



class DescribeConsensusResponse(AbstractModel):
    """公共返回响应体"""

    def __init__(self):
        self.RequestId = None
        self.Fields = None
        self.Data = None
        self.Total = None
        self.PageNo = None
        self.PageSize = None
        self.Pages = None
        self.HasNextPage = None
        self.NextPage = None
        self.LastPage = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")
        self.Fields = params.get("Fields")
        self.Data = params.get("Data")
        self.Total = params.get("Total")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")
        self.Pages = params.get("Pages")
        self.HasNextPage = params.get("HasNextPage")
        self.NextPage = params.get("NextPage")
        self.LastPage = params.get("LastPage")
