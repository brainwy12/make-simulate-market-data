import point
import match
def init_point(tick):
    point_1_1 = point.trader_class_1(10000,1.0/50000,1)
    point_1_2 = point.trader_class_1(1000,1.0/50000,10)
    point_1_3 = point.trader_class_1(100,1.0/50000,100)
    point_2_1 = []
    point_3 = []
    point_4 =[]
    point_5 = []
    
    print "type 1 init done ,type 2 begin"
    for i in range(0,20):
        tem = point.trader_class_2(1,0.5,1)
        tem.update_change(tick)
        point_2_1.append(tem)

    for i in range(0,20):
        tem = point.trader_class_2(10,0.5,1)
        tem.update_change(tick)
        point_2_1.append(tem)

    for i in range(0,20):
        tem = point.trader_class_2(100,0.5,1)
        tem.update_change(tick)
        point_2_1.append(tem)
    print "type 2_1 init done ,type 2_2 begin"
    for i in range(0,10):
        tem = point.trader_class_2(1,0.5,-1,0.04,0.06,0.001,0.003,0.001,0.003)
        tem.update_change(tick)
        point_2_1.append(tem)
    for i in range(0,10):
        tem = point.trader_class_2(10,0.5,-1,0.04,0.06,0.001,0.003,0.001,0.003)
        tem.update_change(tick)
        point_2_1.append(tem)
    for i in range(0,10):
        tem = point.trader_class_2(100,0.5,-1,0.04,0.06,0.001,0.003,0.001,0.003)
        tem.update_change(tick)
        point_2_1.append(tem)
    
    print "type 2_2 init done ,type 3 begin"
    for i in range(0,10):
        tem = point.trader_class_3()
        point_3.append(tem)
    print "type 3 init done ,type 4 begin"
    for i in range(0,5):
        tem = point.trader_class_4()
        tem.get_volume(tick)
        point_4.append(tem)
    print "type 4 init done ,type 5 begin"
    for i in range(0,100):
        tem = point.trader_class_5()
        tem.get_volume(tick)
        point_5.append(tem)
    return point_1_1,point_1_2,point_1_3,point_2_1,point_3,point_4,point_5

def run_point_1_open(point_1,volume,orderlist,pointlist_1_2,tick):
    num = point_1.tradenum()
    point_1.update_n(-1*num)
    for i in range(0,num):
        tem = point.trader_class_1_2(volume)
        tem.get_price(tick)
        order = tem.send_order(tick)
        orderlist.append(order)
        pointlist_1_2.append(tem)

def run_point_1_close(pointlist,orderlist,tick):
    for i in pointlist:
        if i.close_position == True and i.wait_position == 0:
            i.get_price(tick)
            order = i.send_order(tick)
            orderlist.append(order)

def run_point_2(pointlist,orderlist,tick):
    for i in pointlist:
        if i.wait_position == 0 and i.close_judge(tick) == True:
            order = i.send_order(tick)
            orderlist.append(order)
        if i.in_position == i.wait_position == 0 and i.open_judge(tick) == True:
            orderlist.append(i.send_order(tick))
 
def run_point_3(pointlist,orderlist,tick,cancel_list):
    for i in pointlist:
        i.change_state(tick)
        if i.state == 0:
            if i.open_judge(tick) == True:
                if i.get_price == True:
                    orderlist.append(i.send_order(tick))
        elif i.state == 1 or i.state == -1:
            if i.get_price(tick) == True:
                cancel_list.append(i.cancel_order(tick))
                orderlist.append(i.send_order(tick))

def run_point_4(pointlist,orderlist,tick):
    for i in pointlist:
        if i.open_judge == True:
            i.get_price(tick)
            orderlist.append(i.send_order(tick))

def run_point_5(pointlist,orderlist,tick):
    for i in pointlist:
        if i.open_judge == True:
            i.get_price(tick)
            orderlist.append(i.send_order(tick))

def receive_tradeorder(tradelist,point_1_1,point_1_2,point_1_3,pointlist_1,point_2,point_3,point_4,point_5):
    for trade in tradelist:
        code = trade.identifycode
        for i in pointlist_1:
            if code == i.identifycode:
                if i.receive_order(trade):
                    if i.volume == point_1_1.volume:
                        point_1_1.update_n(1)
                    elif i.volume == point_1_2.volume:
                        point_1_2.update_n(1)
                    elif i.volume == point_1_3.volume:
                        point_1_3.update_n(1)
                    del i
        for i in point_2:
            if code == i.identifycode:
                i.receive_order(trade)
        for i in point_3:
            if code == i.identifycode:
                i.receive_order(trade)
        for i in point_4:
            if code == i.identifycode:
                i.receive_order(trade)
        for i in point_4:
            if code == i.identifycode:
                i.receive_order(trade)







def main():
    point.readcsvfile('rb1701.csv')
    tick = len(point.sim_data)-1
    makedata_num = 100000
    #init point 
    point_2 = []
    point_3 = []
    point_4 =[]
    point_5 = []
    pointlist_1 = []
    print "begin init"
    point_1_1,point_1_2,point_1_3,point_2,point_3,point_4,point_5 = init_point(tick)

    #run point
    for i in range(0,makedata_num):
        print "in the loop ", i, " times"
        orderlist = []
        cancel_list = []
        trade_list = []
        run_point_1_close(pointlist_1,orderlist,tick)
        run_point_1_open(point_1_1,point_1_1.volume,orderlist,pointlist_1,tick)
        run_point_1_open(point_1_2,point_1_2.volume,orderlist,pointlist_1,tick)
        run_point_1_open(point_1_2,point_1_2.volume,orderlist,pointlist_1,tick)
        print "type 1 done"
        run_point_2(point_2,orderlist,tick)
        run_point_3(point_3,orderlist,tick,cancel_list)
        run_point_4(point_4,orderlist,tick)
        print "type 4 done"
        run_point_5(point_5,orderlist,tick)
        trade_back = match.match(cancel_list,orderlist)
        trade_list = trade_back[0]
        new_data = trade_back[1]
        receive_tradeorder(tradelist,point_1_1,point_1_2,point_1_3,pointlist_1,point_2,point_3,point_4,point_5)
        point.sim_data.append(new_data)
        tick+=1
        print new_data
        raw_input("pause")


    for i in range(5,100000):
        print "the tick num is ", i
        num = point_1_1.tradenum()
        point_1_1.update_n(-1*num)
        for j in range(0,num):
            tem = point.trader_class_1_2()
            tem.get_price()
            order1 = tem.send_order()
            print order1.output()
        if num > 0:
            raw_input('pause')

main()