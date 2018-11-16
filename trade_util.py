#!/usr/bin/python
# coding=utf-8
import urllib
#import urllib2
#import cookielib
import os,time,string
import sys
import re
import random
from trade_url import *
import configparser
# from crack_vc import crack_vc
from stock_util import *
from html_parser import *
from crack_bmp import *
import logging

import futuquant as ft

class gw_ret_code:
    # 150906130资金不足
    # 150906135股数不够
    # 长城的出错都是这个鸟样 alert("-990297020[-990297020]，出错了就反馈空的订单号，看看是不是自己定义一些exception来搞
    NOT_ENOUGH_MONEY = 1
    NOT_ENOUGH_STOCK = 2
    SETTLEMENT_TIME = 3 #999003088
    NOT_DEAL_TIME =4 #990297020
    NOT_RIGHT_ORDER_ID = 5 #990268040订单号不对
    NOT_CORRECT_PRICE = 6  #990265060价位不对
    PASSWORD_ERROR = 7 #980023096 账号或者密码不对
    SHENGOU_LIMIT = 8 #申购数量超过可申购额度
    REPEATED_SHENGOU = 9  #"-150906090新股配售同一只证券代码不允许重复委托!"
    EXCEED_ZHANGTING = 10 #-990265050[-990265050]委托价格超过涨停价格

    LOGIN_FAIL = 100 #login fail
    OTHER_ERROR = 999

class auto_trade:
    def __init__(self, config_file):
        self.account = ""
        self.passwd_encrypted = ""
        self.secuids = None
        self.stock_code = ""
        self.order_type = ""
        self.price = ""
        self.amount = ""
        self.read_config(config_file)
        self.gw_trade = trade_url()

    def read_config(self, config_file):
        #读取配置文件
        cf = configparser.ConfigParser()
        try:
            cf.read(config_file)
            self.account = cf.get("common", "account")
            self.passwd_encrypted = cf.get("common", "passwd_encrypted") #加密后的密码
            #print("passwd_encrypted="+self.passwd_encrypted)
            secuids_sh = cf.get("common", "secuids_sh")  #上海的股东代码
            secuids_sz = cf.get("common", "secuids_sz") #深圳的股东代码
            self.secuids = {
                        1: secuids_sh,
                        0: secuids_sz
                    }
        except Exception as e:
            #logging.warning()
            return

    # 登录后获得cookie
    def prepare(self):
        ###preprea for login
        (ret, result) = self.gw_trade.prepare("https://trade.cgws.com/cgi-bin/user/Login?function=tradeLogout")
        if ret != 0:
            logging.warn("get verified code fail: ret=%d" % ret)
            return -5
        #get verify code
        #urllib.urlretrieve("https://trade.cgws.com/cgi-bin/img/validateimg", "d://1.jpg", None)
        (ret, tmp_buff) = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/img/validateimg", "rand=" + str(random.random()))
        if ret != 0:
            logging.warn("get verified code fail: ret=%d" % ret)
            return -10
        #tmp_buff = gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/img/validateimg", "")0
        verify_pic = open('d://1.jpg', 'wb')
        verify_pic.write(tmp_buff)
        verify_pic.close()
        #verify_code = crack_vc().get_vcode(r"d:\1.jpg", r"d:\vcode")
        crack_bmp1 = crack_bmp()
        verify_code = crack_bmp1.decode_from_file("d://1.jpg")
        #pasre verify code,just input by you
        #verify_code = raw_input('Enter verify code : ')
        #print verify_code

        ##################login######################
        post_data={
        'ticket': verify_code,
        'retUrl':'',
        'password': self.passwd_encrypted,
        'mac': '',
        'password_Controls': 'normal',
        'type':'Z',
        'fundAccount': self.account,
        'isSaveAccount':'1',
        'normalpassword':'',
        }
        (ret, result) = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/user/Login", post_data)
        if ret != 0:
            return -15

        # 判断是否出错
        #print(result.decode("gbk", "ignore"))
        reg = re.compile('.*PublicKey.*')
        match = reg.search(result.decode("gbk", "ignore"))
        if match:
            return -20
        '''
            if match.group(1) == "980023096":
                print("login  error: msg=%s" % (match.group(1)))
                return gw_ret_code.PASSWORD_ERROR
            else:
                print("login error: msg=%s" % (match.group(1)))
                return gw_ret_code.OTHER_ERROR
        '''
        #保存cookie

        return 0
        ############ get main page cookie ##############

    #买卖
    #输入参数：
    def buy_sell(self, order_type,  stock_code, price, amount):
        ret = self.prepare()
        if ret != 0:
            return  gw_ret_code.LOGIN_FAIL, "登录失败"

        print("Action of ", stock_code , ": Order_type=", order_type , ", price=" , price , ", amount=" , amount)
        ############ post buy order #######################
        stock_ut = stock_util()
        market_id = stock_ut.get_market(stock_code)
        up_limit = stock_ut.get_up_limit(price)
        down_limit = stock_ut.get_down_limit(price)
        print(market_id)
        secuid = self.secuids[market_id]
        maxBuy = 0
        post_data = {
        "type": order_type,
        "market": market_id,
        "up_limit": up_limit,
        "down_limit": down_limit,
        "stktype": "0",
        "secuid": secuid,
        "stkcode": stock_code,
        "stockName":"",
        "price": price,
        "fundavl": "1.00",
        "maxBuy": maxBuy,
        "amount": amount
        }
        (ret, result) = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockBusiness", post_data)
        if ret != 0:
            logging.warn("post to url fail: ret=%d" % ret)
            return -10;

        #print(result.decode('gbk', "ignore"))
        #判断是否出错
        reg = re.compile('.*alert.*\[-(\d{6,})\]')
        print(result.decode('gbk', "ignore"))
        match = reg.search(result.decode('gbk', "ignore"))
        if match: #正常的买卖
            if match.group(1) == "150906130":
                return gw_ret_code.NOT_ENOUGH_MONEY, "资金不足"
            elif match.group(1) == "150906135":
                return gw_ret_code.NOT_ENOUGH_STOCK, "可卖股数不够"
            elif match.group(1) == "999003088":
                return gw_ret_code.SETTLEMENT_TIME, "结算时段，不能交易"
            elif match.group(1) == "990297020":
                return gw_ret_code.NOT_DEAL_TIME, "非交易时段"
            elif match.group(1) == "990265060":
                return gw_ret_code.NOT_CORRECT_PRICE, "价位不对"
            elif match.group(1) == "990265050":
                return gw_ret_code.EXCEED_ZHANGTING, "委托价格超过涨停价格"
            else:
                print("not deal error: msg=%s" % (match.group(1)))
                return gw_ret_code.OTHER_ERROR, "其他错误"
        else: #判断是否新股申购
            #没有返回码，特殊处理
            reg1 = re.compile('.*alert.*新股申购数量超出.*\[(\d{3,})\]')
            print(result.decode('gbk', "ignore"))
            match = reg1.search(result.decode('gbk', "ignore"))
            if match:
                return gw_ret_code.SHENGOU_LIMIT, match.group(1)

            #有返回码
            reg = re.compile('.*alert.*-(\d{6,}).*')
            #print(result.decode('gbk', "ignore"))
            match = reg.search(result.decode('gbk', "ignore"))
            if match:
                if match.group(1) == "150906090":
                    return gw_ret_code.REPEATED_SHENGOU, "新股配售同一只证券代码不允许重复委托"
                else:
                    print("deal ipo  error: msg=%s" % (match.group(1)))
                    return gw_ret_code.OTHER_ERROR, "其他错误"

        #解析出合同编号，如果出错，那么返回""
        print(result.decode("gbk", "ignore"))
        reg = re.compile('alert.*(\d{4})')
        match = reg.search(result.decode("gbk", "ignore"))
        if match:
            return 0, match.group(1)
        else:
            return -5, "不晓得的错误"

    def cancel_order(self, order_id):
        ret = self.prepare()
        if ret != 0:
            return  gw_ret_code.LOGIN_FAIL, "登录失败"
        ##print "Action of " + stock_code + ": Order_type=" + order_type + ", price=" + price + ", amount=" + amount
        ############ post buy order #######################
        post_data={
        "id": order_id
        }
        (ret, result) = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockCancel", post_data)
        if ret != 0:
            logging.warn("get to url fail: ret=%d" % ret)
            return -5, None
        #print result
        # 判断是否出错
        reg = re.compile('.*alert.*\[-(\d{6,})\]')
        match = reg.search(result.decode("gbk", "ignore"))
        if match:
            if match.group(1) == "990268040":
                return gw_ret_code.NOT_RIGHT_ORDER_ID, "订单号不正确"
            else:
                return gw_ret_code.OTHER_ERROR, "其他错误"

        return 0, None

    def query_account(self):
        ret = self.prepare()
        if ret != 0:
            return  gw_ret_code.LOGIN_FAIL, "登录失败"

        (ret, result) = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/EntrustQuery?function=MyAccount", "")
        if ret != 0:
            logging.warn("get to url fail: ret=%d" % ret)
            return -5, None
        html_parse_inst = html_parser(result)
        return 0, html_parse_inst.get_account()

    def query_holdings(self):
        ret = self.prepare()
        if ret != 0:
            print("login fail: ret=%d" % ret)
            return  gw_ret_code.LOGIN_FAIL, "登录失败"

        (ret, result) = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/EntrustQuery?function=MyStock&stktype=0", "")
        #print(result.decode("gbk", "ignore"))
        if ret != 0:
            logging.warn("get to url fail: ret=%d" % ret)
            return -5, None
        html_parse_inst = html_parser(result)
        return 0, html_parse_inst.get_holdings()

    def sell_all_at_market_price(self):
        (ret, result) = self.query_holdings()
        if ret == 0:
            logging.info("Query holdings OK: result=%s" % result)
        else:
            logging.warn("query holdings fail: ret=%d, result=%s" % (ret, result))
            return -5, None

        #sell all holdings at market prices
        quote_context = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
        for one_holding in result:
            if int(one_holding["amount"]) == 0:
                continue
            #subscript
            stock_code_w_prifix = stock_util.add_prifix(one_holding["stock_code"])
            ret_status, ret_data = quote_context.subscribe(stock_code_w_prifix, "QUOTE")
            if ret_status != RET_OK:
                print("%s %s: %s" % (stock_code_w_prifix, "QUOTE", ret_data))
                continue

            #query quote
            code_list = []
            code_list.append(stock_code_w_prifix)
            ret_status, ret_data = quote_context.get_stock_quote(code_list)
            if ret_status == RET_ERROR:
                logging.info("get_stock_quote:stock_code=%s, msg=%s" % (code_list, ret_data))
                continue

            now_price = ret_data["last_price"][0]
            sell_price = round(now_price*0.99, 2)

            (ret, result) = self.buy_sell("S", one_holding["stock_code"], sell_price, one_holding["amount"])
            if ret == 0:
                logging.info("Deal OK: order_id=%s" % result)
            else:
                logging.warn("Buy Or Sell Fail: ret=%d, ret_msg=%s" % (ret, result))
                continue

        return 0, None

    ################# query ongoing order ####################
    def query_ongoing_order(self):
        ret = self.prepare()
        if ret != 0:
            return  gw_ret_code.LOGIN_FAIL, "登录失败"
        print("........... query ongoing order ................")
        (ret, result) = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockCancel", "")
        if ret != 0:
            logging.warn("get to url fail: ret=%d" % ret)
            return -5, None
        html_parse_inst = html_parser(result)
        print("........... query order finish .................")
        return 0, html_parse_inst.get_onging_orders()









