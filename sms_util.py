# -*- coding: utf-8 -*-
import sys
import uuid

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkcore.request import CommonRequest

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

    def send_sms_err_msg(self, ret_code, ret_msg):
        params = "{\"err_code\":\"" + ret_code + "\",\"err_msg\":\"" + ret_msg + "\"}"
        ret = self.send_sms(self.phone_num, self.app_name, self.sms_tem_id, params)
        return ret

    def send_sms(self, phone_numbers, sign_name, template_code, template_param=None):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone_numbers)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', template_param)

        try:
            response = self.acs_client.do_action_with_exception(request)
            logging.info("send sms result: response = %s", response)
        except ServerException as e:
            logging.warning("send sms fail: response = %s", str(e))
            return -5
        except ClientException as e:
            logging.warning("send sms fail: response = %s", str(e))
            return -10

        return 0

if __name__ == '__main__':
    sms_util_ins = sms_util()
    sms_util_ins.init()
    ret = sms_util_ins.send_sms_err_msg("test", "test msg")
    if ret != 0:
        print("sms send msg fail: iret=", ret)
   
    
    

