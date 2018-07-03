# -*- coding: utf-8 -*-
"""
yunpian api
"""

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from urllib import parse


# #薪酬合计
# totalsalaryresult = ""
# # 三险一金合计
# totlainsuranceandfund=""
# #绩效工资
# performancepay=""
# # 应发薪酬
# totalpayamount=""
# # 实发薪酬
# finalpayingamount=""

class YunPianMsg():
    def __init__(self,apikey,tplid):
        self.apikey = apikey
        self.tplid = tplid
        self.clnt = YunpianClient(self.apikey)

    def yunpianmsg(self,**kwargs):

        for arg,value in kwargs.items():
            #print (arg,value)
            if arg == "mobile":
                mobile = value
            elif arg == "name":
                name = value
            elif arg == "basesalaryresult":
                basesalaryresult = value
            elif arg == "addbasesalarythismonth":
                addbasesalarythismonth = value
            elif arg == "welfareresult":
                welfareresult = value
            elif arg == "totalsalaryresult":
                totalsalaryresult = value
            elif arg == "endowmentinsurance":
                endowmentinsurance = value
            elif arg == "medicalinsurance":
                medicalinsurance = value
            elif arg == "unemploymentinsurance":
                unemploymentinsurance = value
            elif arg == "housingprovidentfund":
                housingprovidentfund = value
            elif arg == "companyfund":
                companyfund = value
            elif arg == "totlainsuranceandfund":
                totlainsuranceandfund = value
            elif arg == "totalpayamount":
                totalpayamount = value
            elif arg == "personaltax":
                personaltax = value
            elif arg == "finalpayingamount":
                finalpayingamount = value
            else:
                pass

        smsvalue = {"#name#":name,"#basesalaryresult#":basesalaryresult,
                    "#addbasesalarythismonth#":addbasesalarythismonth,"#welfareresult#":welfareresult,
                    "#totalsalaryresult#":totalsalaryresult,"#endowmentinsurance#":endowmentinsurance,
                    "#medicalinsurance#":medicalinsurance,"#unemploymentinsurance#":unemploymentinsurance,
                    "#housingprovidentfund#": housingprovidentfund,"#companyfund#":companyfund,
                    "#totlainsuranceandfund#": totlainsuranceandfund,"#totalpayamount#":totalpayamount,
                    "#personaltax#": personaltax,"#finalpayingamount#":finalpayingamount
                    }
        tpl_value = parse.urlencode(smsvalue)
        param = {YC.MOBILE:mobile,YC.TPL_ID:self.tplid,YC.TPL_VALUE:tpl_value}
        r = self.clnt.sms().tpl_single_send(param)
        return r.code()
# if __name__=="__main__":
#     ym = YunPianMsg(APIKEY,TPLID)
#
#     fsitem = {"mobile":"13329502095","name":"李晓龙","totalsalaryresult":"5300.21",
#     "totlainsuranceandfund":"897","performancepay":"10000","totalpayamount":"6700",
#     "finalpayingamount":"5678.32"}
#     cd = ym.yunpianmsg(**fsitem)
#     print(cd)
    
