#!/usr/bin/python
# coding:utf-8
from sqlalchemy import Column, String, Integer, Float, TIMESTAMP,  create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
import pymysql
import time

#class cond_order_def:
#    DIRECTION_UP = 1
#    DIRECTION_UP
order_direction_def = {"up":"U", "down":"D"}
order_state_def = {"todo":0, "done":1, "cancel":2}
order_action_def = {"B":"B", "S":"S"}

Base = declarative_base()
Base = declarative_base()
class cond_order(Base):
    __tablename__ = "cond_order"
    order_id = Column(Integer, primary_key=True)
    stock_code = Column(String(20))
    direction = Column(String)
    action = Column(String)
    amount = Column(Integer)
    deal_price = Column(Integer)
    compare_price = Column(Integer)
    begin_in_day  = Column(Integer)
    end_in_day =  Column(Integer)
    state = Column(Integer)
    insert_time = Column(TIMESTAMP)
    update_time = Column(TIMESTAMP)
class db_util:
    def __init__(self):
        self.session = None
        self.user = ""
        self.password = ""
        self.read_config("config.ini")
    def read_config(self, config_file):
        # 读取配置文件
        cf = configparser.ConfigParser()
        try:
            cf.read(config_file)
            self.user = cf.get("mysql", "user")
            self.password  = cf.get("mysql", "password")

        except Exception as e:
            print("Read config error")
            return

    def get_db_session(self):
        mysql_uri_str = 'mysql+pymysql://' + self.user + ':' + self.password + '@localhost:3306/orderdb?charset=utf8'
        engine = create_engine(mysql_uri_str, echo=False)
        db_session = sessionmaker(bind=engine)
        return db_session

    def init_db(self):
        Session = self.get_db_session()
        self.session = Session()

    def close_db(self):
        self.session.close()

    def get_todo_orders(self, stock_code=None):
        if stock_code != None:
            order_list = self.session.query(cond_order).filter(cond_order.stock_code == stock_code, cond_order.state == order_state_def["todo"]).all()
        else:
            order_list = self.session.query(cond_order).filter(cond_order.state == order_state_def["todo"]).all()

        return order_list

    def rmi_get_todo_orders(self, stock_code=None):
        order_list = self.get_todo_orders(stock_code)
        ret_order_list = []
        for row in order_list:
            tmp = {}
            tmp["order_id"] = row.order_id
            tmp["stock_code"] = row.stock_code
            tmp["direction"] = row.direction
            tmp["action"] = row.action
            tmp["amount"] = row.amount
            tmp["deal_price"] = row.deal_price
            tmp["compare_price"] = row.compare_price
            tmp["begin_in_day"] = row.begin_in_day
            tmp["end_in_day"] = row.end_in_day
            tmp["state"] = row.state
            tmp["insert_time"] = row.insert_time
            tmp["order_id"] = row.order_id
            tmp["update_time"] = row.update_time
            ret_order_list.append(tmp)
        return ret_order_list

    def get_all_orders(self, stock_code=None):
        #查找普通止损单
        if stock_code != None:
            order_list = self.session.query(cond_order).filter(cond_order.stock_code == stock_code).all()
        else:
            order_list = self.session.query(cond_order).all()
        return order_list

    def rmi_get_all_orders(self, stock_code=None):
        order_list = self.get_all_orders(stock_code)
        ret_order_list = []
        for row in order_list:
            tmp = {}
            tmp["order_id"] = row.order_id
            tmp["stock_code"] = row.stock_code
            tmp["direction"] = row.direction
            tmp["action"] = row.action
            tmp["amount"] = row.amount
            tmp["deal_price"] = row.deal_price
            tmp["compare_price"] = row.compare_price
            tmp["begin_in_day"] = row.begin_in_day
            tmp["end_in_day"] = row.end_in_day
            tmp["state"] = row.state
            tmp["insert_time"] = row.insert_time
            tmp["order_id"] = row.order_id
            tmp["update_time"] = row.update_time
            ret_order_list.append(tmp)
        return ret_order_list

    def get_cond_order_bystock(self, stock_code):
        order_list = self.session.query(cond_order).filter(cond_order.stock_code==stock_code).all()
        return order_list

    def add_condition_order(self, stock_code, direction, compare_price, action, deal_price,  amount,  begin_in_day, end_in_day):
        #insert into db
        print("stock_code=", stock_code, ", direction=", direction, ", action=", action,  ", amount=",  amount, ",deal_price=", deal_price, "compare_price=", compare_price, ", begin_in_day=", begin_in_day, ", end_in_day=", end_in_day)
        new_order = cond_order(order_id=0, stock_code=stock_code, direction=direction, action=action,  amount=amount, deal_price=deal_price, compare_price=compare_price,
                               begin_in_day=begin_in_day, end_in_day=end_in_day, state=0, insert_time=func.now())
        self.session.add(new_order)
        #print new_order.stock_code
        ret = self.session.commit()
        return 1

    def update_cond_order(self, order_id, state):
        self.session.query(cond_order).filter(cond_order.order_id == order_id).update({cond_order.state: state})
        ret = self.session.commit()
        return ret

    def cancel_cond_order(self, order_id):
        self.update_cond_order(order_id, order_state_def["cancel"])


#db_util1 = db_util()
#db_util1.init_db()

#while True:
#    order_list = db_util1.get_todo_orders()
#    for row in order_list:
        #print(row.__dict__)
#        print(row.__dict__)
#    print "*************************************"
#    time.sleep(5)
#db_util1.add_condition_order("600036", 1, 17,  'B', 100,  17, 1430, 1500)
#db_util1.update_cond_order(3, 0)
