# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT

from comm_util import *
"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

class sms_util:
    def __init__(self):
        self.access_key_id = ""
        self.access_key_secret = ""
        self.phone_num = ""
        self.app_name = ""
        self.sms_tem_id = ""

    def read_config(self, config_file):
        # 读取配置文件
        cf = configparser.ConfigParser()
        try:
            cf.read(config_file)
            self.access_key_id = cf.get("aliyun", "AccessKeyId")
            self.access_key_secret = cf.get("aliyun", "AccessKeySecret")
            self.phone_num = cf.get("monitor", "phone_num")
            self.app_name = cf.get("monitor", "app_name")
            self.sms_tem_id = cf.get("monitor", "sms_tem_id")

        except Exception as e:
            logging.warning("read config fail")
            return -10

        return 0

    def init(self):
        ret = self.read_config("config.ini")
        if ret != 0:
            logging.warning("read config fail: ret=%d", ret)
            return -20
        self.acs_client = AcsClient(self.access_key_id, self.access_key_secret, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def send_sms_err_msg(self, ret_code, ret_msg):
        __business_id = uuid.uuid1()
        params = "{\"err_code\":\"" + ret_code + "\",\"err_msg\":\"" + ret_msg + "\"}"
        #print(self.phone_num)
        try:
            self.send_sms(__business_id, self.phone_num, self.app_name, self.sms_tem_id, params)
        except Exception as e:
            logging.warning("send msg fail: %s", str(e))
            return -10

    def send_sms(self, business_id, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理

        return smsResponse

if __name__ == '__main__':
    sms_util_ins = sms_util()
    sms_util_ins.init()
    sms_util_ins.send_sms_err_msg("test", "test msg")
   
    
    

