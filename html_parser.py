import os,time,string
import sys
from pyquery import PyQuery as pq
import re
class html_parser:
    def __init__(self, html_text):
        self.html_text = html_text
        return
    def get_holdings(self):
        holding_list = []
        jp = pq(self.html_text)
        tmp = jp("#tab1 tbody tr")
        for i in tmp:
            #print pq(i).find("td").text()
            #print pq(i).children().eq(0).text()
            one_record = {}
            one_record["stock_code"] = pq(i).children().eq(0).text()
            one_record["stock_name"] = pq(i).children().eq(1).text()
            one_record["amount"] = pq(i).children().eq(3).text()
            one_record["cost_price"] = pq(i).children().eq(5).text()
            one_record["total_value"] = pq(i).children().eq(7).text()
            one_record["profit_value"] = pq(i).children().eq(8).text()
            one_record["profit_ratio"] = pq(i).children().eq(9).text()
            holding_list.append(one_record)
        return holding_list

    def get_account(self):
        tmp_info = []
        jp = pq(self.html_text)
        tmp = jp("#tabAccount tr")
        for i in tmp:
            #print pq(i).find("td").text()
            #print pq(i).children().eq(0).text()
            one_record = {}
            reg = re.compile(u'.*?(\d+\.\d*)')

            match = reg.search(pq(i).children().eq(0).text())
            if match:
                one_record["balance"] = float(match.group(1))
            else:
                one_record["balance"] = 0
                print "html parse error"

            match = reg.search(pq(i).children().eq(1).text())
            if match:
                one_record["availble"] = float(match.group(1))
            else:
                one_record["availble"] = 0
                print "html parse error"

            tmp_info.append(one_record)

        return tmp_info[0]

    def get_onging_orders(self):
        ongoing_list = []
        jp = pq(self.html_text)
        tmp = jp("#tab1 tbody tr")
        for i in tmp:
            #print pq(i).find("td").text()
            print pq(i).children().eq(3).text()
            one_record = {}
            one_record["stock_code"] = pq(i).children().eq(3).text()
            one_record["order_id"] = pq(i).children().eq(9).text()
            one_record["amount_done"] = pq(i).children().eq(10).text()
            ongoing_list.append(one_record)
        return ongoing_list

#f = open(r"d:\a.txt", "r")
#tmp_buff = f.read()
#f.close()

#html_parse = html_parser()
#html_parse.get_holdings(tmp_buff)
