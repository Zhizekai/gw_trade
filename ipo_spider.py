#!/usr/bin/python
# coding=utf-8
import os
import sys
import time
from datetime import datetime
import urllib
import urllib.parse
import urllib.request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import traceback
import socket
import logging
import logging.handlers
import importlib,sys

#from langconv import *

user_agent = "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1" \
             "(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
unknow_ipo_time = 4200000000

def attr_report(attr_id):
    return

class CnIpoSpider:
    #初始化网页信息，
    def __init__(self):
        self.list_url = "http://data.10jqka.com.cn/ipo/xgsgyzq/"
        self.detail_url = "http://data.10jqka.com.cn/ipo/xgxx/newstock/%s/"
        self.ipo_list = []
    def get_today_ipo(self):
        today_ipos = []
        now_date_str = time.strftime("%Y-%m-%d")
        for one_ipo in self.ipo_list:
            if one_ipo["apply_date_parsed"] == now_date_str:
                today_ipos.append(one_ipo)

        return today_ipos

    def crawl_list(self):                    #爬网页
        try:
            attr_report(446069)
            req = urllib.request.Request(
                url=self.list_url,
            )
            req.add_header('User-agent', user_agent)   #将访问请求改成浏览器访问

            # print req.headers
            # print req.data
            try:
                resp = urllib.request.urlopen(req, timeout=3)
            except urllib.HTTPError as e:
                logging.warning("server process request error: err_code=%s", e.code)
                return -5, None
            except urllib.URLError as e:
                logging.warning("reach server error: reason=%s", e.reason)
                return -10, None
            except Exception as e:
                logging.warning("other exception: msg=%s", e.message)
                return -100, None

            html_text = resp.read().decode("gbk")   #访问结果内容  怎么知道是gbk编码？
            resp.close()                            #关闭访问

            soup = BeautifulSoup(html_text, "lxml")    #解析网页
            trows = soup.find("table", attrs={"id": "maintable"}).find("tbody").find_all("tr")  #find(name, attrs, recursive, text, **kwargs)  name 标签 找到表格里每行的内容
            for trow in trows:
                attr_report(446070)
                ipo = {}
                tds = trow.find_all("td")
                ipo["code"] = tds[0].find("a").string   # 代码
                ipo["name"] = tds[1].find("a").string   # 名称
                #ipo["tc_name"] = Converter('zh-hant').convert(ipo["name"])#将简体转繁体  zh-hans繁体转简体
                ipo["apply_code"] = tds[2].string.strip()    # 申购代码
                ipo["publish_shares"] = tds[3].string + u"万股" #发行总数
                ipo["online_publish_shares"] = tds[4].string + u"万股" #网上发新数

                #申购上限，万股
                if tds[5].find("span", attrs={"class": "yugu"}):
                    ipo["apply_limit_str"] = u"预估 " + tds[5].contents[1].string + u"万股"
                    ipo["apply_limit"] = float(tds[5].contents[1].string)*10000
                else:
                    ipo["apply_limit_str"] = tds[5].string + u"万股"
                    ipo["apply_limit"] = float(tds[5].string) * 10000

                #需要多少钱
                if tds[6].find("span", attrs={"class": "yugu"}):

                    ipo["apply_limit_mv"] = u"预估 " + tds[6].contents[1].string + u"万元"
                else:
                    ipo["apply_limit_mv"] = tds[6].string + u"万元"

                #发行价格
                if tds[7].find("span", attrs={"class": "yugu"}):
                    #ipo["ipo_price"] = u"预估 " + tds[7].contents[2].string.replace('\r', '').replace('\n', '').replace('\t', '')
                    ipo["ipo_price"] = u"预估 " + tds[7].contents[1].string
                else:
                    ipo["ipo_price"] = tds[7].string.replace('\r', '').replace('\n', '').replace('\t', '')
                
                ipo["pe"] = tds[8].string
                ipo["industry_pe"] = tds[9].string
                #申购日期
                ipo["apply_date"] = tds[10].string
                ipo['apply_date_parsed'] = self._parse_date(ipo['apply_date'])

                if tds[11].find("span", attrs={"class": "yugu"}):
                    ipo["lucky_ratio"] = u"预估 " + tds[11].contents[1].string
                else:
                    ipo["lucky_ratio"] = tds[11].string

                ipo['lucky_date'] = self._parse_lucky_date(tds[12])
                ipo['lucky_date_parsed'] = self._parse_date(ipo['lucky_date'])
                ipo["lucky_codes"] = self._parse_lucky_codes(tds[12])
                ipo["pay_date"] = tds[13].string
                ipo['pay_date_parsed'] = self._parse_date(ipo['pay_date'])
                ipo["ipo_date"] = tds[14].string
                ipo['ipo_date_parsed'] = self._parse_date(ipo['ipo_date'])

                self.ipo_list.append(ipo)
                logging.info("code:{0}, name:{1}, ipo_date:{2}".format(ipo["code"], ipo["name"], ipo["ipo_date"]))
                attr_report(441842)
        except Exception as e:
            attr_report(441843)
            logging.warning('cn crawl list ex: {0}, {1}'.format(e, traceback.format_exc()))

    @staticmethod
    def _parse_lucky_date(tag):
        attr_report(446071)
        try:
            if tag.find("a").string == u"查看":
                return ""
            return tag.find("a").string
        except Exception as e:
            attr_report(446072)
            logging.warning('cn _parse_lucky_date ex: {0}, {1}'.format(e, traceback.format_exc()))
            return ""

    @staticmethod
    def _parse_lucky_codes(tag):
        attr_report(446073)
        try:
            if tag.find("a").string != u"查看":
                attr_report(446074)
                return ""
            
            zq_tags = tag.find("div", attrs={"class": "cont"}).find_all("div", attrs={"class": "clearfix"})
            lucky_codes = ""
            for zq_tag in zq_tags:
                x = zq_tag.find_all("span")
                lucky_codes += x[0].string+x[1].string+'\n'
            attr_report(446075)
            return lucky_codes
        except Exception as e:
            attr_report(441844)
            logging.warning('cn _parse_lucky_codes ex: {0}, {1}'.format(e, traceback.format_exc()))
            return ""
    
    def crawl_detail(self):           #爬另一个网页信息，并判断
        for ipo in self.ipo_list:
            attr_report(446076)
            url = self.detail_url % ipo["code"]
            req = urllib.request.Request(
                url=url,
            )
            req.add_header('User-agent', user_agent)
            
            retry_cnt = 0
            while retry_cnt < 3:
                try:
                    try:
                        resp = urllib.request.urlopen(req, timeout=3)
                    except urllib.HTTPError as e:
                        logging.warning("server process request error: err_code=%s", e.code)
                        return -5, None
                    except urllib.URLError as e:
                        logging.warning("reach server error: reason=%s", e.reason)
                        return -10, None
                    except Exception as e:
                        logging.warning("other exception: msg=%s", e.message)
                        return -100, None

                    html_text = resp.read().decode("gbk")
                    resp.close()
                    if self._parse_detail(html_text, ipo):
                        break
                    else:
                        retry_cnt += 1
                except Exception as e:
                    retry_cnt += 1
                    logging.warning('cn craw {0} detail ex:{1}, {2}'.format(ipo["code"], e, traceback.format_exc()))
            if retry_cnt >= 3:
                attr_report(441846)
                logging.info("cn craw {0} detail fail".format(ipo["code"]))
            else:
                attr_report(441845)

    @staticmethod
    def _parse_detail(html_text, ipo):
        try:
            attr_report(446077)
            soup = BeautifulSoup(html_text, "lxml")
            tbodys = soup.find_all("tbody")
            detail_info = {}
            
            tbody = tbodys[0]
            detail_info["code"] = tbody.find("td", text=u"股票代码").find_next_sibling().string
            detail_info["name"] = tbody.find("td", text=u"股票简称").find_next_sibling().string
            detail_info["market"] = tbody.find("td", text=u"上市地点").find_next_sibling().string
            if detail_info["market"] == u"上海证券交易所":
                detail_info["futu_code"] = "1"+detail_info["code"]
                detail_info["futu_market_code"] = "30"
            elif detail_info["market"] == u"深圳证券交易所":
                detail_info["futu_code"] = "2"+detail_info["code"]
                detail_info["futu_market_code"] = "31"
            else:
                logging.warning("invalid market {0} of {1}".format(detail_info["market"], ipo["code"]))
                attr_report(441978)
                return False
            
            try:
                tbody = tbodys[1]
                ipo_date = tbody.find("td", text=u"上市日期").find_next_sibling().string
                if ipo_date is not None and len(detail_info["ipo_date"]) >= 10:
                    detail_info["ipo_date"] = ipo_date
                    detail_info['ipo_date_parsed'] = detail_info['ipo_date'][0:10]
            except Exception as e:
                attr_report(446078)
                logging.warning("parse {0} ipo date ex: {1}, {2}".format(detail_info["code"], e, traceback.format_exc()))

            if detail_info["code"] != ipo["code"] or detail_info["name"] != ipo["name"]:
                logging.info("parse detail failed. code:{0}-{1}, name:{0}-{1}"
                            .format(ipo["code"], detail_info["code"], ipo["name"], detail_info["name"]))
                attr_report(446079)
                return False
            ipo.update(detail_info)

            if ipo['ipo_date_parsed'] is not None and len(ipo['ipo_date_parsed']) >= 10:
                ipo["ipo_time"] = time.mktime(time.strptime(ipo["ipo_date_parsed"][0:10], '%Y-%m-%d'))
            else:
                ipo["ipo_time"] = unknow_ipo_time

            logging.info("detail, code:{0}".format(detail_info["code"]))
            attr_report(446080)
            return True
        except Exception as e:
            logging.warning("cn _parse_detail({0}) ex: {1}, {2}".format(ipo["code"], e, traceback.format_exc()))
            attr_report(446078)
            return False

    @staticmethod
    def _parse_date(str_date):
        attr_report(446081)
        if str_date is None or len(str_date) < 5:
            attr_report(446082)
            logging.warning('date {0} invalid'.format(str_date))
            return ""
        mon = int(str_date[0:2])
        now = time.localtime()
        this_mon = now.tm_mon
        if this_mon >= mon:
            if mon + 12 - this_mon <= 3:
                return "{0}-{1}".format(now.tm_year+1, str_date[0:5])
            else:
                return "{0}-{1}".format(now.tm_year, str_date[0:5])
        else:
            if mon - this_mon <= 3:
                return "{0}-{1}".format(now.tm_year, str_date[0:5])
            else:
                return "{0}-{1}".format(now.tm_year-1, str_date[0:5])

def run():
    try:
        init_logging('./log/ipo_spider.log')
        cn_spider = CnIpoSpider()
        cn_spider.crawl_list()
        #cn_spider.crawl_detail()
        today_ipos = cn_spider.get_today_ipo()
        if len(today_ipos) == 0:
            print("今天没有IPO")
        else:
            print("今天有IPO")
            print(today_ipos)

    except Exception as e:
        logging.warning('ex:{0}, {1}'.format(e, traceback.format_exc()))
        return False


if __name__ == '__main__':
    importlib.reload(sys)
    run()
