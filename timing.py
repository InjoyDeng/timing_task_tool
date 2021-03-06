#coding=utf-8
import commands, time, threading, sys

exchange_succeed = False    #兑换成功
stockout = False            #商品已兑完
now_time_string = ""
stop_exchange_timestamp = sys.maxint
request_count = 0           #请求次数

start_task_timestamp = 0.0  #任务开始时间
avg_request = 0.0

start_time_string = sys.argv[1]     #开始时间
thread_number = int(sys.argv[2])    #线程数

class exchange (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global exchange_succeed
        global stockout
        global request_count
        global avg_request

        while time.time() < stop_exchange_timestamp and exchange_succeed == False and stockout == False:
            result = commands.getoutput("")
            
            if exchange_succeed == False and stockout == False:
                request_count += 1
                end_timestamp = time.clock()
                avg_request = request_count / (end_timestamp - start_task_timestamp)

            if result.find('"success":true') != -1 or exchange_succeed:
                exchange_succeed = True
            elif result.find('本时间段内商品已兑完') != -1 or stockout:
                stockout = True
            elif result.find('下个整点') == -1 and result.find('服务器繁忙') == -1:
                print time.strftime("%H:%M:%S", time.localtime()) + "\t" + result[result.find("{"): result.find("}") + 1]

while 1:
    now_time_string = time.strftime("%H:%M:%S", time.localtime())

    if now_time_string.find(start_time_string) != -1:

        print(now_time_string + " 任务开始：")

        stop_exchange_timestamp = time.time() + 3
        for i in range(thread_number):
            if stockout or exchange_succeed:
                print "任务已经结束，终止任务创建"
                break
            else:
                exchange().start()

        start_timestamp = time.clock()
        while time.time() < stop_exchange_timestamp + 10:
            if stockout or exchange_succeed:
                time.sleep(5)   #等待所有请求完成
                break
            else:
                time.sleep(0.2)

        if exchange_succeed:
            print "兑换成功"
        elif stockout:
            print "兑换失败，已被兑完"
        print "发送有效请求 " + str(request_count) + " 个，平均每秒 " + str(avg_request) + " 个"

        stockout = False    #重置
        exchange_succeed = False    #重置
        request_count = 0
        
        print "=========================================\n"

    else:
        time.sleep(1)
