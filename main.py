# coding=utf-8
import os,time,string
import sys
import argparse
from trade_util import *
import logging
from ipo_spider import *
import comm_util
from sms_util import *


def main():
    ######## init parse #############
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--action_type", choices=['B', 'S', 'Q', 'A', 'G', 'C', 'N', 'P'], help="B: Buy; S: Sell; Q: Query Holdings; A: Query Account Info; G: Query Ongoings; C: Cancel Order; N: Buy New Stock; P: Sell All at MP")
    parser.add_argument("cmd_args", nargs='*', help="[Buy Stock. Usage: -B stock_code price amount. e.g. -tB 159915  2 100]" \
                                                    "  [Sell Stock. Usage: -S  stock_code price amount. e.g. -tS 159915 2 100]" \
                                                    "  [Query Account Info. Usage: -tA]" \
                                                    "  [Query Holding Stock. Usage: -tQ]" \
                                                    "  [Query OnGoing Order. Usage: -tG]" \
                                                    "  [Cancel OnGoing Order. Usage: -tC order_id. order_id can be acquired from the result of -tG cmd]" \
                                                    "  [Buy New Stock. Usage: -tN]" \
                                                    "  [Sell ALL Stock At Market Price. Usage: -tP")
    args = parser.parse_args()
    #print(args.action_type, args.cmd_args)

    at_inst = auto_trade("config.ini")
    sms_util_ins = sms_util()
    sms_util_ins.init()

    if (args.action_type == "B" or args.action_type == "S"):
        (ret, result) = at_inst.buy_sell(args.action_type, args.cmd_args[0], args.cmd_args[1],args.cmd_args[2])
        if ret == 0:
            logging.info("Deal OK: order_id=%s" % result)
        else:
            logging.warning("Buy Or Sell Fail: ret=%d, ret_msg=%s" % (ret, result))
        #ongoing_list = at_inst.query_ongoing_order()
        #time.sleep(10)
        #for  record in ongoing_list:
        #    at_inst.cancel_order(record["order_id"])

    elif (args.action_type == "P"):
        (ret, result) = at_inst.sell_all_at_market_price()
        if ret == 0:
            logging.info("Clear all postion OK: result=%s" % result)
        else:
            logging.warning("Clear all postion fail: ret=%d, result=%s" % (ret, result))

    elif (args.action_type == "N"):
        cn_spider = CnIpoSpider()
        ret = cn_spider.crawl_list()
        if ret != 0:
            sms_util_ins.send_sms_err_msg(ret, "get ipo list fail")
            return
        # cn_spider.crawl_detail()
        today_ipos = cn_spider.get_today_ipo()

        if len(today_ipos) == 0:
            logging.info("今天没有IPO")
            return
        else:
            logging.info("今天有IPO")
            logging.info(today_ipos)
        logging.info("进行申购")
        for one_ipo in today_ipos:
            (ret, result) = at_inst.buy_sell("B", one_ipo["apply_code"], one_ipo["ipo_price"], one_ipo["apply_limit"])
            if ret == 0:
                logging.info("Deal OK: order_id=%s" % result)
            elif ret == gw_ret_code.SHENGOU_LIMIT:
                (ret1, result1) = at_inst.buy_sell("B", one_ipo["apply_code"], one_ipo["ipo_price"], int(result))
                if ret1 == 0:
                    logging.info("Deal OK: order_id=%s" % result1)
                else:
                    logging.warning("Buy Or Sell Fail: ret=%d, ret_msg=%s" % (ret, result1))
                    sms_util_ins.send_sms_err_msg(ret, "Buy Or Sell Fail")
            else:
                logging.warning("Buy Or Sell Fail: ret=%d, ret_msg=%s" % (ret, result))

    elif (args.action_type == "Q"):
        (ret, result) = at_inst.query_holdings()
        if ret == 0:
            logging.info("Query holdings OK: result=%s" % result)
        else:
            logging.warning("query order fail: ret=%d, result=%s" % (ret, result))
    elif (args.action_type == "A"):
        (ret, result) = at_inst.query_account()
        if ret == 0:
            logging.info("Query account OK: result=%s" % result)
        else:
            logging.warning("query account fail: ret=%d" % ret)
    elif (args.action_type == "G"):
        (ret, result) = at_inst.query_ongoing_order()
        if ret == 0:
            logging.info("Query Ongoing Order OK: result=%s" % result)
        else:
            logging.warn("query ongoing order fail: ret=%d" % ret)

    elif (args.action_type == "C"):
        (ret, result) = at_inst.cancel_order(args.cmd_args[0])
        if ret == 0:
            logging.info("Cancel Order OK: order_id=%s" % args.cmd_args[0])
        else:
            logging.warning("query cancel order fail: ret=%d, msg=%s" % (ret, result))
    else:
        print("No Such Action. Please input: python main.py -h ")
    #except Exception, e:
    #    print "Process Error: e=" + e.message
    #    exit(1)
    #raw_input()

if __name__ == "__main__":
    main()



