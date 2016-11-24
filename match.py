from operator import itemgetter, attrgetter, methodcaller
from point import Order, data

ask_order = []
bid_order = []

#b1 = Order(10, 107, 0, 'rb1701', 1, 1)
#b2 = Order(2, 101, 0, 'rb1701', 2, 1)
#b3 = Order(1, 102, 0, 'rb1701', 3, 1)
#b4 = Order(5, 110, 0, 'rb1701', 4, 1)
#b5 = Order(6, 108, 0, 'rb1701', 5, 1)
#b6 = Order(5, 109, 0, 'rb1701', 6, 1)
#b7 = Order(1, 108, 0, 'rb1701', 7, 1)

#a1 = Order(10, 105, 0, 'rb1701', 11, -1)
#a2 = Order(2, 112, 0, 'rb1701', 12, -1)
#a3 = Order(1, 100, 0, 'rb1701', 13, -1)
#a4 = Order(5, 108, 0, 'rb1701', 14, -1)
#a5 = Order(6, 107, 0, 'rb1701', 15, -1)
#a6 = Order(5, 109, 0, 'rb1701', 16, -1)
#a7 = Order(6, 102, 0, 'rb1701', 17, -1)

#neworder = {a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6,b6,a7,b7}


class trade_order:
    def __init__(self, identifycode, trade_price, position):
        self.identifycode = identifycode
        self.trade_price = trade_price
        self.position = position

def match(withdraw_order, new_order):
    global ask_order, bid_order

    for w in withdraw_order:    #remove withdraw order from list
        for a, b in ask_order, bid_order:
            if w == a.identifycode:
                ask_order.remove(a)
            elif w == b.identifycode:
                bid_order.remove(b)
    
    for n in new_order:         #insert new order
        if n.position == 1:
            bid_order.append(n)
        else:
            ask_order.append(n)
        
    ask_order = sorted(ask_order, key=attrgetter('price'))
    bid_order = sorted(bid_order, key=attrgetter('price'), reverse=True)


   # for element in ask_order:
   #     element.output()
   # print '\n'
   # for element in bid_order:
   #     element.output()

    Volume = 0
    Turnover = 0

    ptr_a1 = 0
    ptr_a2 = 0
    ptr_b1 = 0
    ptr_b2 = 0
    
    trade_list = []
    last_trade_ptr = [0,0,0,0]
    trade_price = 0
    flag = True
    while(flag):
        if(ask_order[ptr_a1].price <= bid_order[ptr_b1].price):
            trade_price = (ask_order[ptr_a1].price + bid_order[ptr_b1].price) / 2
            trade_list.append(trade_order(ask_order[ptr_a1].identifycode, trade_price, ask_order[ptr_a1].position))
            trade_list.append(trade_order(bid_order[ptr_b1].identifycode, trade_price, bid_order[ptr_b1].position))
            Volume += 2
            Turnover += trade_price * 2
        
            last_trade_ptr[0] = ptr_a1
            last_trade_ptr[1] = ptr_a2
            last_trade_ptr[2] = ptr_b1
            last_trade_ptr[3] = ptr_b2
            
            ptr_a2 += 1
            ptr_b2 += 1

            if(ptr_a2 == ask_order[ptr_a1].volume):
                ptr_a1 += 1
                ptr_a2 = 0
            if(ptr_b2 == bid_order[ptr_b1].volume):
                ptr_b1 += 1
                ptr_b2 = 0
            if ptr_a1 >= len(ask_order) or ptr_b1 >= len(bid_order):
                flag = False
        else:
            flag = False
    
    Lastprice = trade_price
    

  #  print 'trade_list size is: ', len(trade_list), '\n'
  #  for element in trade_list:
  #      print 'trade identify id is: ', element.identifycode, 'trade price is: ', element.trade_price, 'position is: ', element.position
    
  #  print '\n Lastprice: ', Lastprice

    Askprice1 = 0
    Bidprice1 = 0
    Askvolume1 = 0
    Bidvolume1 = 0
    Askprice2 = 0
    Bidprice2 = 0
    Askvolume2 = 0
    Bidvolume2 = 0

    if(ptr_a1 < len(ask_order)):
        Askprice1 = ask_order[ptr_a1].price
    else:
        Askprice1 = 0

    if(ptr_b1 < len(bid_order)):
        Bidprice1 = bid_order[ptr_b1].price
    else:
        Bidprice1 = 0
    
    flag = True     #Askvolume1
    while(flag):
        if(ptr_a1 < len(ask_order)):
            if(ptr_a2 < ask_order[ptr_a1].volume and ask_order[ptr_a1].price == Askprice1):
                Askvolume1 += 1
                ptr_a2 += 1
            else:
                flag = False
        else:
            flag = False
        if(ptr_a2 == ask_order[ptr_a1].volume):
            ptr_a1 += 1
            ptr_a2 = 0
        if(ptr_a1 >= len(ask_order)):
            flag = False
    
    flag = True         #Bidvolume1
    while(flag):
        if(ptr_b1 < len(bid_order)):
            if(ptr_b2 < bid_order[ptr_b1].volume and bid_order[ptr_b1].price == Bidprice1):
                Bidvolume1 += 1
                ptr_b2 += 1
            else:
                flag = False
        else:
            flag = False
        if(ptr_b2 == bid_order[ptr_b1].volume):
            ptr_b1 += 1
            ptr_b2 = 0
        if(ptr_b1 >= len(bid_order)):
            flag = False
    
    if(ptr_a1 < len(ask_order)):
        Askprice2 = ask_order[ptr_a1].price
    else:
        Askprice2 = 0

    if(ptr_b1 < len(bid_order)):
        Bidprice2 = bid_order[ptr_b1].price
    else:
        Bidprice2 = 0
    
    flag = True         #Askvolume2
    while(flag):
        if(ptr_a1 < len(ask_order)):
            if(ptr_a2 < ask_order[ptr_a1].volume and ask_order[ptr_a1].price == Askprice2):
                Askvolume2 += 1
                ptr_a2 += 1
            else:
                flag = False
        else:
            flag = False
        if(ptr_a2 == ask_order[ptr_a1].volume):
            ptr_a1 += 1
            ptr_a2 = 0
        if(ptr_a1 >= len(ask_order)):
            flag = False
    
    flag = True             #Bidvolume2
    while(flag):
        if(ptr_b1 < len(bid_order)):
            if(ptr_b2 < bid_order[ptr_b1].volume and bid_order[ptr_b1].price == Bidprice2):
                Bidvolume2 += 1
                ptr_b2 += 1
            else:
                flag = False
        else:
            flag = False
        if(ptr_b2 == bid_order[ptr_b1].volume):
            ptr_b1 += 1
            ptr_b2 = 0
        if(ptr_b1 >= len(bid_order)):
            flag = False
    

   # print '\nAskprice1: ', Askprice1, 'Bidprice1: ', Bidprice1, 'Askprice2: ', Askprice2, 'Bidprice2: ', Bidprice2

   # print '\nAskvolume1: ', Askvolume1, 'Bidvolume1: ', Bidvolume1, 'Askvolume2: ', Askvolume2, 'Bidvolume1: ', Bidvolume2

    TradingDay = '20161101'
    InstrumentID = 'rb1701'
    UpdateTime = '9:00:00'
    UpdateMillisec = 0
    Askprice3 = 0
    Bidprice3 = 0
    Askvolume3 = 0
    Bidvolume3 = 0
    Askprice4 = 0
    Bidprice4 = 0
    Askvolume4 = 0
    Bidvolume4 = 0
    Askprice5 = 0
    Bidprice5 = 0
    Askvolume5 = 0
    Bidvolume5 = 0

    ret_data = data(InstrumentID, TradingDay, UpdateTime, UpdateMillisec, Lastprice, Volume, Turnover, 
    Askprice5, Askprice4, Askprice3, Askprice2, Askprice1, Bidprice1, Bidprice2, Bidprice3, Bidprice4,
    Bidprice5, Askvolume5, Askvolume4, Askvolume3, Askvolume2, Askvolume1, Bidvolume1, Bidvolume2, 
    Bidvolume3, Bidvolume4, Bidvolume5)

    for element in trade_list:
        if(element.position == -1):
            for i in range(len(ask_order)):
                if(element.identifycode == ask_order[i].identifycode):
                    ask_order[i].volume -= 1
                    break
        else:
            for i in range(len(bid_order)):
                if(element.identifycode == bid_order[i].identifycode):
                    bid_order[i].volume -= 1
                    break
    
    tmp = []
    for element in ask_order:
        if element.volume != 0:
            tmp.append(element)
    ask_order = tmp

    tmp = []
    for element in bid_order:
        if element.volume != 0:
            tmp.append(element)
    bid_order = tmp
    
   # for element in ask_order:
   #     element.output()
   # print '\n'
   # for element in bid_order:
   #     element.output()

    ret = (trade_list, ret_data)

    return ret




    


        
