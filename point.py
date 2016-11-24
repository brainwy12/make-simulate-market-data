import random
import math
import csv
sim_data = []
identification_set = set()

def get_identifycode():
    tem = random.randint(0,1000000)
    global identification_set
    if len(identification_set) == 0:
        identification_set.add(tem)
        return tem
    if tem in identification_set:
        get_identifycode()
    else:
        identification_set.add(tem)
        return tem

def erxiangfenbu(n,k,p):
    cnk = math.factorial(n)/(math.factorial(n-k)*math.factorial(k))
    return cnk*pow(p,k)*pow(1-p,n-k)

class price_change:
    update_tick = 50000
    def __init__(self,tick,dur_tick,change_per):
        self.tick = tick
        self.dur_tick = dur_tick
        self.change_per = change_per
    def lower_bound(self):
        if self.tick < self.update_tick:
            start_tick = 0
            end_tick = self.tick
        else :
            tem = int(self.tick/self.update_tick)
            start_tick = (tem-1)*self.update_tick
            end_tick = tem*self.update_tick
        change_list = []
        for i in range(start_tick,end_tick-self.dur_tick):
            price_change = (sim_data[i].Askprice1+sim_data[i].Bidprice1)/2 - (sim_data[i+self.dur_tick].Askprice1+sim_data[i+self.dur_tick].Bidprice1)/2
            change_list.append(abs(price_change))
        change_list = sorted(change_list,reverse = True)
        return change_list[int((end_tick-start_tick-self.dur_tick)*self.change_per)]


class data:
    def __init__(self,InstrumentID,TradingDay,UpdateTime,UpdateMillisec,Lastprice,Volume,Turnover,Askprice5,Askprice4,Askprice3,Askprice2,Askprice1,
        Bidprice1,Bidprice2,Bidprice3,Bidprice4,Bidprice5,Askvolume5,Askvolume4,Askvolume3,Askvolume2,Askvolume1,Bidvolume1,Bidvolume2,Bidvolume3,Bidvolume4,Bidvolume5):
        self.TradingDay = TradingDay
        self.InstrumentID = InstrumentID
        self.UpdateTime = UpdateTime
        self.UpdateMillisec = UpdateMillisec
        self.Lastprice = Lastprice
        self.Volume = Volume
        self.Turnover = Turnover
        self.Askprice1 = Askprice1
        self.Bidprice1 = Bidprice1
        self.Askvolume1 = Askvolume1
        self.Bidvolume1 = Bidvolume1
        self.Askprice2 = Askprice2
        self.Bidprice2 = Bidprice2
        self.Askvolume2 = Askvolume2
        self.Bidvolume2 = Bidvolume2
        self.Askprice3 = Askprice3
        self.Bidprice3 = Bidprice3
        self.Askvolume3 = Askvolume3
        self.Bidvolume3 = Bidvolume3
        self.Askprice4 = Askprice4
        self.Bidprice4 = Bidprice4
        self.Askvolume4 = Askvolume4
        self.Bidvolume4 = Bidvolume4
        self.Askprice5 = Askprice5
        self.Bidprice5 = Bidprice5
        self.Askvolume5 = Askvolume5
        self.Bidvolume5 = Bidvolume5
    
def  readcsvfile(filename):
    filedata = csv.reader(open(filename,'rb'))
    for i,ir in enumerate(filedata):
        if i == 0 :                                  #for data have label in line one
            continue
        tem = data(ir[0],ir[1],ir[2],ir[3],float(ir[4]),int(ir[5]),float(ir[7]),float(ir[9]),float(ir[10]),float(ir[11]),float(ir[12]),float(ir[13])
            ,float(ir[14]),float(ir[15]),float(ir[16]),float(ir[17]),float(ir[18]),float(ir[19]),float(ir[20]),float(ir[21]),float(ir[22]),float(ir[23]),float(ir[24]),float(ir[25]),float(ir[26]),float(ir[27]),float(ir[28]))
        sim_data.append(tem)


class Order:
    trade = False
    def __init__(self,volume,price,time,InstrumentID,identifycode,position):
        self.volume = volume
        self.price = price
        self.time = time
        self.InstrumentID = InstrumentID
        self.identifycode = identifycode
        self.position = position
    def output(self):
        print 'volume is ',self.volume," price is ",self.price," tick is ",self.time,' identifycode is ',self.identifycode," position is ",self.position

class trader_class_1:
    num = 0
    trade_probility = 0
    volume = 0 
    def __init__(self,num,probility,volume):
        self.num = num
        self.trade_probility = probility
        self.volume = volume

    def tradenum(self):
        flag = random.random()
        prob = 0
        lastprob = 0
        for i in range(0,max(int(self.num*self.trade_probility*20),4)):
            prob += erxiangfenbu(self.num,i,self.trade_probility)
            if lastprob < flag and prob > flag :
                if abs(lastprob - flag) > abs(prob-flag):
                    lastprob = prob
                    return i
                else:
                    lastprob = prob
                    if i == 0:
                        return 0
                    else:       
                        return i-1
            lastprob = prob

        return max(int(self.num*self.probility*20),4)
    #add num is positive, minus is negative
    def update_n(self,num):
        self.num += num

    
class trader_class_1_2:
    volume = 0
    price = 0
    close_prob = 0
    ask_prob = 0
    bid_prob = 0
    position = 0    #1 for buy , -1 for sell
    price_tick_prob = 0
    price_tick1_prob = 0
    price_tick2_prob = 0
    identifycode = -1
    wait_volume = 0
    in_volume = 0
    wait_position = 0
    in_position = 0
    in_price = 0
    
    def __init__(self,volume=1,ask_prob=0.5,price_tick_prob=0.25,price_tick1_prob=0.125,price_tick2_prob=0.125,close_prob=1.0/50000):
        self.volume = volume
        self.ask_prob = ask_prob
        self.bid_prob = 1 - ask_prob
        self.price_tick_prob = price_tick_prob
        self.price_tick1_prob = price_tick1_prob
        self.price_tick2_prob = price_tick2_prob
        self.close_prob = close_prob

    def close_position(self):
        tem = random.random
        if tem < self.close_prob:
            return True
        else :
            return False

    def get_price(self,tick):
        tem = random.random()
        temp = random.random()
        if tem < self.ask_prob:
            self.position = -1
            if temp < self.price_tick_prob:
                tick = len(sim_data) - 1
                self.price = sim_data[tick].Askprice1
            elif temp < self.price_tick_prob*2:
                tick = len(sim_data) - 1
                self.price = sim_data[tick].Bidprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob:
                tick = len(sim_data) - 2
                self.price = sim_data[tick].Askprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob*2:
                tick = len(sim_data) - 2
                self.price = sim_data[tick].Bidprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob*2 + self.price_tick2_prob:
                tick = len(sim_data) - 3
                self.price = sim_data[tick].Askprice1
            else:
                tick = len(sim_data) - 3
                self.price = sim_data[tick].Bidprice1
        else:
            self.position = 1
            if temp < self.price_tick_prob:
                tick = len(sim_data) - 1
                self.price = sim_data[tick].Askprice1
            elif temp < self.price_tick_prob*2:
                tick = len(sim_data) - 1
                self.price = sim_data[tick].Bidprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob:
                tick = len(sim_data) - 2
                self.price = sim_data[tick].Askprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob*2:
                tick = len(sim_data) - 2
                self.price = sim_data[tick].Bidprice1
            elif temp < self.price_tick_prob*2 + self.price_tick1_prob*2 + self.price_tick2_prob:
                tick = len(sim_data) - 3
                self.price = sim_data[tick].Askprice1
            else:
                tick = len(sim_data) - 3
                self.price = sim_data[tick].Bidprice1

    def send_order(self,tick):
        
        InstrumentID = sim_data[tick].InstrumentID
        identifycode = get_identifycode()
        if self.in_position*self.position == -1:
            waitorder = Order(min(self.volume,self.in_volume),self.price,tick,InstrumentID,identifycode,self.position)
        else:
            waitorder = Order(self.volume,self.price,tick,InstrumentID,identifycode,self.position)
        self.wait_volume = self.volume
        self.wait_position = self.position
        return waitorder


    def receive_order(self,trade_order):
        self.wait_volume -= trade_order.volume
        if self.wait_volume == 0:
            self.wait_position = 0
        if self.in_volume == 0 or self.in_position * self.wait_position == 1:
            self.in_price = (self.in_price*self.in_volume + trade_order.price * trade_order.volume)/(self.in_volume+trade_order.volume)
            self.in_volume += trade_order.volume
            self.in_position = trade_order.position
        elif self.in_position * self.wait_position == -1:
            self.in_price = (self.in_price*self.in_volume - trade_order.price*trade_order.volume)/(self.in_volume-trade_order.volume)
            self.in_volume -= trade_order.volume

        if self.in_volume == 0 and self.in_position != 0:
            self.in_position = 0
        if self.in_volume == 0 and self.wait_volume == 0:
            return True
        return False
        #true to release , false there are some order to trade

class trader_class_2:
    volume = 0
    price = 0
    observe_tick = 0
    change_per = 0
    zhiying_per = 0
    zhiying_prob = 0
    zhisun_per = 0
    position = 0
    identifycode = -1
    in_volume = 0
    in_position = 0
    in_price = 0
    wait_volume = 0
    wait_position = 0
    trend_overturn = 0 # 1 for trend and -1 for turn
    update_tick = 0
    open_bound = 0.0
    open_price = 0.0
    def __init__(self,volume=1,zhiying_prob=0.5,trend_overturn = 1,change_per_low=0.08,change_per_high=0.12,zhiying_low=0.002,zhiying_high=0.01,zhisun_low=0.01,zhisun_high=0.05):
        self.volume = volume
        self.observe_tick = random.randint(120,360)
        self.change_per = random.uniform(change_per_low,change_per_high)
        self.zhiying_per = random.uniform(zhiying_low,zhiying_high)
        self.zhiying_prob = zhiying_prob
        self.trend_overturn = trend_overturn
        self.zhisun_per = random.uniform(zhisun_low,zhisun_high)

    def update_change(self,tick):
        if tick > self.update_tick:
            change_bound = price_change(tick,self.observe_tick,self.change_per)
            self.open_bound = change_bound.lower_bound()
            self.update_tick += 50000

    def open_judge(self,tick):
        #update_change(self,tick)
        tem = (sim_data[tick].Askprice1+sim_data[tick].Bidprice1)/2-(sim_data[tick-self.observe_tick].Askprice1+sim_data[tick-self.observe_tick].Bidprice1)/2
        if abs(tem) > self.open_bound:
            if tem*trend_overturn > 0: #buy
                self.position = 1
                self.price = sim_data[tick].Askprice1
            else:
                self.position = -1
                self.price = sim_data.Bidprice1
            return True
        else:
            return False

    def close_judge(self,tick):
        if (self.in_position == 1 and ((sim_data[tick].Askprice1+sim_data[tick].Bidprice1)/2 - self.in_price)/self.in_price > self.zhiying_per ) :
            temp = random.random()
            self.position = - 1
            if temp < self.zhiying_prob: #duishoujia
                self.price = sim_data[tick].Bidprice1
            else:
                self.price = sim_data[tick].Askprice1
            return True
        elif (self.in_position == -1 and (self.in_price-(sim_data[tick].Askprice1+sim_data[tick].Bidprice1)/2)/self.in_price > self.zhiying_per):
            temp = random.random()
            self.position = 1
            if temp < self.zhiying_prob:
                self.price = sim_data[tick].Askprice1
            else:
                self.price = sim_data[tick].Bidprice1
            return True
        elif self.in_position == -1 and ((sim_data[tick].Askprice1+sim_data[tick].Bidprice1)/2 - self.in_price)/self.in_price > self.zhisun_per   :
            self.position = 1
            self.price = sim_data[tick].Askprice1
            return True
        elif self.in_position == 1 and (self.in_price - (sim_data[tick].Askprice1+sim_data[tick].Bidprice1)/2)/self.in_price > self.zhisun_per  :
            self.position = -1
            self.price = sim_data[tick].Bidprice1
            return True
        else:
            return False

    def send_order(self,tick):
        InstrumentID = sim_data[tick].InstrumentID
        identifycode = get_identifycode()
        if self.in_position*self.position == -1:
            waitorder = Order(min(self.volume,self.in_volume),self.price,tick,InstrumentID,identifycode,self.position)
        else:
            waitorder = Order(self.volume,self.price,tick,InstrumentID,identifycode,self.position)
        self.wait_volume = self.volume
        self.wait_position = self.position
        return waitorder

    def receive_order(self,trade_order):
        self.wait_volume -= trade_order.volume
        if self.wait_volume == 0:
            self.wait_position = 0
        if self.in_volume == 0 or self.in_position * self.wait_position == 1:
            self.in_price = (self.in_price*self.in_volume + trade_order.price * trade_order.volume)/(self.in_volume+trade_order.volume)
            self.in_volume += trade_order.volume
            self.in_position = trade_order.position
        elif self.in_position * self.wait_position == -1:
            self.in_price = (self.in_price*self.in_volume - trade_order.price*trade_order.volume)/(self.in_volume-trade_order.volume)
            self.in_volume -= trade_order.volume

        if self.in_volume == 0 and self.in_position != 0:
            self.in_position = 0
        if self.in_volume == 0 and self.wait_volume == 0:
            return True
        return False

class trader_class_3:
    volume = 0
    price = 0
    trade_probility = 0
    observe_tick = 0
    open_interval = 0
    close_interval =0
    open_times = 0
    wait_time = 0
    in_volume = 0
    in_position = 0 
    in_price = 0
    wait_volume = 0
    wait_position = 0
    open_tick = 0
    close_tick = 0
    state = 0 # 1 for open and -1 for close
    def __init__(self,volume=10000,trade_probility = 1.0/50000,open_interval = 15,close_interval=15,open_times = 10,wait_time = 360,observe_tick =50000):
        self.volume = volume/open_times
        self.trade_probility = trade_probility
        self.open_interval = open_interval
        self.open_times = open_times
        self.wait_time = wait_time
        self.close_interval = close_interval
        self.observe_tick = observe_tick
    def open_judge(self,tick):
        if self.state == 0:
            tem = random.random()
            if tem < self.trade_probility:
                self.open_tick = tick
                self.state = 1
                if sim_data[tick].Askprice1+sim_data[tick].Bidprice1 > sim_data[tick-observe_tick].Askprice1 + sim_data[tick - observe_tick].Bidprice1:
                    self.position = 1
                else:
                    self.position = -1
                return True
            else :
                return False
        else:
            return False

    def get_price(self,tick):
        if (tick - self.open_tick) % self.open_interval == 0 and (tick-self.open_tick)/self.open_interval < self.open_times and self.state == 1:
            if self.position == 1:
                self.price = sim_data[tick].Askprice1
            elif self.position == -1:
                self.price = sim_data[tick].Bidprice1

            if (tick-self.open_tick)/self.open_interval == self.open_times:
                self.state = -2
                self.close_tick = tick+self.wait_time

            return True
        elif (tick-self.close_tick)%self.close_interval == 0 and self.in_position!=0 and self.state == -1 :
            if self.in_position == 1:
                self.price = sim_data[tick].Bidprice1
            elif self.in_position == -1:
                self.price = sim_data[tick].Askprice1
            self.volume = min(self.volume,self.in_volume)
            return True
        else:
            return False

    def change_state(self,tick):
        if self.state == -2 and self.close_tick <= tick:
            self.state = -1
        elif self.state == -1 and self.in_volume == 0:
            self.state = 0

    def cancel_order(self):
        return self.identifycode

    def send_order(self,tick):
        InstrumentID = sim_data[tick].InstrumentID
        identifycode = get_identifycode()
        if self.in_position*self.position == -1:
            waitorder = Order(min(self.volume,self.in_volume),self.price,tick,InstrumentID,identifycode,self.position)
        else:
            waitorder = Order(self.volume,self.price,tick,InstrumentID,identifycode,self.position)
        self.wait_volume = self.volume
        self.wait_position = self.position
        return waitorder

    def receive_order(self):
        self.wait_volume -= trade_order.volume
        if self.wait_volume == 0:
            self.wait_position = 0
        if self.in_volume == 0 or self.in_position * self.wait_position == 1:
            self.in_price = (self.in_price*self.in_volume + trade_order.price * trade_order.volume)/(self.in_volume+trade_order.volume)
            self.in_volume += trade_order.volume
            self.in_position = trade_order.position
        elif self.in_position * self.wait_position == -1:
            self.in_price = (self.in_price*self.in_volume - trade_order.price*trade_order.volume)/(self.in_volume-trade_order.volume)
            self.in_volume -= trade_order.volume

        if self.in_volume == 0 and self.in_position != 0:
            self.in_position = 0
        if self.in_volume == 0 and self.wait_volume == 0:
            return True
        return False

class trader_class_4:
    volume = 0
    volume_per = 0
    price = 0
    trade_probility = 0 
    thing_prob = 0
    thick_prob = 0
    askprice2_prob = 0 
    bidprice2_prob = 0
    wait_volume = 0
    wait_position = 0
    in_volume = 0
    in_position = 0
    in_price = 0
    observe_tick = 0
    def __init__(self,trade_probility=0.2,thing_prob=0.25,thick_prob=0.5,askprice2_prob=0.125,bidprice2_prob=0.125,observe_tick=50000):
        self.trade_probility = trade_probility
        self.thing_prob = thing_prob
        self.thick_prob = thick_prob
        self.askprice2_prob = askprice2_prob
        self.bidprice2_prob = bidprice2_prob
        self.volume_per = random.uniform(0.2,0.4)
        self.observe_tick = observe_tick

    def get_volume(self,tick):
        start_tick = tick - self.observe_tick
        avg_volume = (sim_data[tick].Volume - sim_data[start_tick].Volume)/self.observe_tick 
        self.volume = int(avg_volume*self.volume_per)


    def open_judge(self,tick):
        tem = random.random()
        if tem < self.trade_probility:
            return True
        else:
            return False

    def get_price(self,tick):
        tem = random.random()
        if tem < self.askprice2_prob:
            self.position = -1
            self.price = sim_data[tick].Askprice2
            
        elif tem < self.askprice2_prob + self.bidprice2_prob:
            self.position = 1
            self.price = sim_data[tick].Bidprice2
            
        elif tem < self.askprice2_prob + self.bidprice2_prob + thing_prob:
            if sim_data[tick].Askvolume1 > sim_data[tick].Bidvolume1:
                self.position = 1
                self.price = sim_data[tick].Bidprice1
            else:
                self.position = -1
                self.price = sim_data[tick].Askprice1
            
        else:
            if sim_data[tick].Askvolume1 > sim_data[tick].Bidvolume1:
                self.position = -1
                self.price = sim_data[tick].Askprice1
            else:
                self.position = 1
                self.price = sim_data[tick].Bidprice1

    def send_order(self,tick):
        InstrumentID = sim_data[tick].InstrumentID
        identifycode = get_identifycode()
        if self.in_position*self.position == -1:
            waitorder = Order(min(self.volume,self.in_volume),self.price,tick,InstrumentID,identifycode,self.position)
        else:
            waitorder = Order(self.volume,self.price,tick,InstrumentID,identifycode,self.position)
        self.wait_volume = self.volume
        self.wait_position = self.position
        return waitorder

    def receive_order(self):
        self.wait_volume -= trade_order.volume
        if self.wait_volume == 0:
            self.wait_position = 0
        if self.in_volume == 0 or self.in_position * self.wait_position == 1:
            self.in_price = (self.in_price*self.in_volume + trade_order.price * trade_order.volume)/(self.in_volume+trade_order.volume)
            self.in_volume += trade_order.volume
            self.in_position = trade_order.position
        elif self.in_position * self.wait_position == -1:
            self.in_price = (self.in_price*self.in_volume - trade_order.price*trade_order.volume)/(self.in_volume-trade_order.volume)
            self.in_volume -= trade_order.volume

        if self.in_volume == 0 and self.in_position != 0:
            self.in_position = 0
        if self.in_volume == 0 and self.wait_volume == 0:
            return True
        return False

class trader_class_5:
    volume_per = 0
    volume = 0
    price = 0
    trade_probility = 0
    wait_volume = 0
    wait_position = 0
    in_volume = 0
    in_position = 0
    in_price = 0
    observe_tick = 50000
    def __init__(self,trade_probility=0.02):
        self.volume_per = random.uniform(0.01,0.02)
        self.trade_probility = trade_probility

    def get_volume(self,tick):
        start_tick = tick - self.observe_tick
        avg_volume = (sim_data[tick].Volume - sim_data[start_tick].Volume)/self.observe_tick 
        self.volume = int(avg_volume*self.volume_per)

    def open_judge(self,tick):
        if sim_data[tick].Askprice1 > sim_data[tick-1].Askprice1:
            self.position = -1
            self.price = sim_data[tick].Askprice1
            return True
        elif sim_data[tick].Bidprice1 < sim_data[tick].Bidprice1:
            self.position = 1
            self.price = sim_data[tick].Bidprice1
            return True
        else:
            return False

    def send_order(self,tick):
        InstrumentID = sim_data[tick].InstrumentID
        identifycode = get_identifycode()
        if self.in_position*self.position == -1:
            waitorder = Order(min(self.volume,self.in_volume),self.price,tick,InstrumentID,identifycode,self.position)
        else:
            waitorder = Order(self.volume,self.price,tick,InstrumentID,identifycode,self.position)
        self.wait_volume = self.volume
        self.wait_position = self.position
        return waitorder

    def receive_order(self):
        self.wait_volume -= trade_order.volume
        if self.wait_volume == 0:
            self.wait_position = 0
        if self.in_volume == 0 or self.in_position * self.wait_position == 1:
            self.in_price = (self.in_price*self.in_volume + trade_order.price * trade_order.volume)/(self.in_volume+trade_order.volume)
            self.in_volume += trade_order.volume
            self.in_position = trade_order.position
        elif self.in_position * self.wait_position == -1:
            self.in_price = (self.in_price*self.in_volume - trade_order.price*trade_order.volume)/(self.in_volume-trade_order.volume)
            self.in_volume -= trade_order.volume

        if self.in_volume == 0 and self.in_position != 0:
            self.in_position = 0
        if self.in_volume == 0 and self.wait_volume == 0:
            return True
        return False



















