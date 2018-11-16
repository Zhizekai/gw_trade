# coding:utf-8
from openft.open_quant_context import *
import logging

####### init log ################
logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='if_statics.log',
                filemode='a')



#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################



# Examples for use the python functions
#
def _example_stock_quote(quote_ctx):
    stock_code_list = ["US.AAPL", "HK.00700", "SZ.000001"]

    # subscribe "QUOTE"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "QUOTE")
        if ret_status != RET_OK:
            logging.info("%s %s: %s" % (stk_code, "QUOTE", ret_data))
            exit()

    ret_status, ret_data = quote_ctx.query_subscription()

    if ret_status == RET_ERROR:
        logging.info(ret_status)
        exit()

    logging.info(ret_data)

    ret_status, ret_data = quote_ctx.get_stock_quote(stock_code_list)
    if ret_status == RET_ERROR:
        logging.info(ret_data)
        exit()
    quote_table = ret_data

    logging.info("QUOTE_TABLE")
    logging.info(quote_table)


def _example_cur_kline(quote_ctx):
    # subscribe Kline
    stock_code_list = ["US.AAPL", "HK.00700", "SZ.000001"]
    sub_type_list = ["K_1M", "K_5M", "K_15M", "K_30M", "K_60M", "K_DAY", "K_WEEK", "K_MON"]

    for code in stock_code_list:
        for sub_type in sub_type_list:
            ret_status, ret_data = quote_ctx.subscribe(code, sub_type)
            if ret_status != RET_OK:
                logging.info("%s %s: %s" % (code, sub_type, ret_data))
                exit()

    ret_status, ret_data = quote_ctx.query_subscription()

    if ret_status == RET_ERROR:
        logging.info(ret_data)
        exit()

    logging.info(ret_data)

    for code in stock_code_list:
        for ktype in ["K_DAY", "K_1M", "K_5M"]:
            ret_code, ret_data = quote_ctx.get_cur_kline(code, 5, ktype)
            if ret_code == RET_ERROR:
                logging.info(code, ktype, ret_data)
                exit()
            kline_table = ret_data
            logging.info("%s KLINE %s" % (code, ktype))
            logging.info(kline_table)
            logging.info("\n\n")


def _example_rt_ticker(quote_ctx):
    stock_code_list = ["US.AAPL", "HK.00700", "SZ.000001", "SH.601318"]

    # subscribe "TICKER"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "TICKER")
        if ret_status != RET_OK:
            logging.info("%s %s: %s" % (stk_code, "TICKER", ret_data))
            exit()

    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.get_rt_ticker(stk_code, 10)
        if ret_status == RET_ERROR:
            logging.info(stk_code, ret_data)
            exit()
        logging.info("%s TICKER" % stk_code)
        logging.info(ret_data)
        logging.info("\n\n")


def _example_order_book(quote_ctx):
    stock_code_list = ["US.AAPL", "HK.00700", "SZ.000001", "SH.601318"]

    # subscribe "ORDER_BOOK"
    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.subscribe(stk_code, "ORDER_BOOK")
        if ret_status != RET_OK:
            logging.info("%s %s: %s" % (stk_code, "ORDER_BOOK", ret_data))
            exit()

    for stk_code in stock_code_list:
        ret_status, ret_data = quote_ctx.get_order_book(stk_code)
        if ret_status == RET_ERROR:
            logging.info(stk_code, ret_data)
            exit()
        logging.info("%s ORDER_BOOK" % stk_code)
        logging.info(ret_data)
        logging.info("\n\n")


def _example_get_trade_days(quote_ctx):
    ret_status, ret_data = quote_ctx.get_trading_days("US", "2017-01-01", "2017-01-18")
    if ret_status == RET_ERROR:
        logging.info(ret_data)
        exit()
    logging.info("TRADING DAYS")
    for x in ret_data:
        logging.info(x)


def _example_stock_basic(quote_ctx):
    ret_status, ret_data = quote_ctx.get_stock_basicinfo("US", "STOCK")
    if ret_status == RET_ERROR:
        logging.info(ret_data)
        exit()
    logging.info("stock_basic")
    logging.info(ret_data)


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            logging.warning("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        #logging.info("StockQuoteTest %s ", content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            logging.warning("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        #logging.info("OrderBookTest   %s ", content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            logging.warning("CurKlineTest: error, msg: %s" % content)
            return RET_ERROR, content
        #logging.info("CurKlineTest %s", content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            logging.warning("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        #logging.info("TickerTest  %s ", content)
        return RET_OK, content





if __name__ == "__main__":
    stock_list = ["HK.00700", "SZ.000001", "SH.603868", "HK.60904"]

    quote_context = OpenQuoteContext(host='127.0.0.1', async_port=11111)
    quote_context.set_handler(StockQuoteTest())
    quote_context.set_handler(OrderBookTest())
    quote_context.set_handler(CurKlineTest())
    quote_context.set_handler(TickerTest())
    quote_context.start()
    logging.info("starting")

    '''
    _example_stock_quote(quote_context)
    _example_cur_kline(quote_context)
    _example_rt_ticker(quote_context)
    _example_order_book(quote_context)
    _example_get_trade_days(quote_context)
    _example_stock_basic(quote_context)
    '''

    while True:

        for stock in stock_list:
            quote_context.unsubscribe(stock, "QUOTE")
            quote_context.unsubscribe(stock, "TICKER")
            quote_context.unsubscribe(stock, "K_1M")
            quote_context.unsubscribe(stock, "ORDER_BOOK")
            quote_context.subscribe(stock, "QUOTE", push=True)
            quote_context.subscribe(stock, "TICKER", push=True)
            quote_context.subscribe(stock, "K_1M", push=True)
            quote_context.subscribe(stock, "ORDER_BOOK", push=True)

        print(quote_context.query_subscription())
        time.sleep(1*60)