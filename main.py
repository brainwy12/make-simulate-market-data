import point

def main():
    point.readcsvfile('rb1701.csv')
    point_1_1 = point.trader_class_1(10000,1.0/50000,1)
    class1_2 = []
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