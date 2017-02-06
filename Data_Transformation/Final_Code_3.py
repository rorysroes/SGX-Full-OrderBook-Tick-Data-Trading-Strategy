# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 13:50:06 2016

@author: rory
"""

import pandas as pd
import time 
import csv

def order_book_tranform(year,month,day,path,best_price_number,series):
    ## read file
    def read_file(year,month,day,path,series):
        data = []
        if len(str(month)) == 1:
            month_ = '0' + str(month)
        else:
            month_ = str(month)
        if len(str(day)) == 1:
            day_ = '0' + str(day)
        else:
            day_ = str(day)
        datapath = str(path) + str(year) + '.' + str(month_) + '.' + str(day_) + '.csv'
        data = pd.read_csv(datapath)
        data = data[data.Series == series]
        return data.reset_index(drop = True)

    def insert(order_book_data,data_to_insert,ob_position):
        top = order_book_data[0:ob_position]
        bottom = order_book_data[ob_position:]
        return pd.concat((top,data_to_insert,bottom)).reset_index(drop = True)

    def draw_out(order_book_data,ob_position):
        top = order_book_data[0:ob_position]
        bottom = order_book_data[ob_position + 1:]
        return pd.concat((top,bottom)).reset_index(drop = True)

    def order_book_to_csv(order_book_bid,order_book_ask,data,i):
        
        order_book_bid_sum = order_book_bid[['Price','QuantityDifference']].groupby(by = ['Price'],as_index = False,sort = False).sum()
        order_book_ask_sum = order_book_ask[['Price','QuantityDifference']].groupby(by = ['Price'],as_index = False).sum()
        order_book_bid_sum = order_book_bid_sum[order_book_bid_sum.QuantityDifference != 0.0].reset_index(drop = True)
        order_book_ask_sum = order_book_ask_sum[order_book_ask_sum.QuantityDifference != 0.0].reset_index(drop = True)
        order_book_bid_ask = pd.concat([order_book_bid_sum[['Price','QuantityDifference']],order_book_ask_sum[['Price','QuantityDifference']]],axis = 1)    
       
        with open('order_book_'+str(best_price_number)+'_'+str(year)+'_'+str(month)+'_'+str(day)+'.csv','a') as f:
            order_book = csv.writer(f)
            order_book.writerow(["TimeStamp",data.TimeStamp[i-1:i].iloc[0]])
            order_book = csv.writer(f,delimiter=',')
            for i in range(0,min(len(order_book_bid_ask),best_price_number),1):
                order_book.writerow(order_book_bid_ask[i:i+1].values.tolist()[0])
        return order_book_bid_sum,order_book_ask_sum

    data = read_file(year,month,day,path,series)
    
    with open('order_book_' + str(best_price_number) + '_' + str(year) + '_' + str(month) + '_' + str(day) + '.csv', 'wb') as csvfile:
        f = csv.writer(csvfile) 

    data[['QuantityDifference']] = data[['QuantityDifference']].astype(float)
    data['QuantityDifference_'] = data['QuantityDifference']
    data_ask = data[(data.BidOrAsk == 'A')].reset_index(drop=True)
    data_bid = data[(data.BidOrAsk == 'B')].reset_index(drop=True)
    order_book_bid = []
    order_book_ask = []
    x1 = data[(data.BidOrAsk == 'A')].TimeStamp.unique()
    x2 = data[(data.BidOrAsk == 'B')].TimeStamp.unique()
    temp_ask = 0
    temp_bid = 0
    
    def first_order_create(index_,data):
        timestamp = data.TimeStamp.unique()[index_]
        print 'timestamp = %s'%(timestamp) 
        bid = []
        ask = []
        timestamp_ = []
        index_find = data[data['TimeStamp'].str.contains(timestamp)].index[-1]
        y = data[:index_find + 1]
        bid.append(y[(y.BidOrAsk == 'B')][["Price","OrderNumber","QuantityDifference","QuantityDifference_"]]) # bid
        ask.append(y[(y.BidOrAsk == 'A')][["Price","OrderNumber","QuantityDifference","QuantityDifference_"]]) # ask
        a = bid[0].sort(['Price'],ascending = [False])
        b = ask[0].sort(['Price'],ascending = [True])
        order_book_bid = a[a.QuantityDifference != 0].reset_index(drop = True)
        order_book_ask = b[b.QuantityDifference != 0].reset_index(drop = True)
        order_book_bid_sum = order_book_bid[['Price','QuantityDifference']].groupby(by = ['Price'],as_index = False,sort = False).sum()
        order_book_ask_sum = order_book_ask[['Price','QuantityDifference']].groupby(by = ['Price'],as_index = False).sum()
        
        if len(order_book_bid_sum[order_book_bid_sum.QuantityDifference == 0.0]) != 0 and len(order_book_ask_sum[order_book_ask_sum.QuantityDifference == 0.0]) != 0:
            
            print 'Exist Bid Ask Order Book Price = Zero'
            price_bid_zero = order_book_bid_sum[order_book_bid_sum.QuantityDifference == 0.0]['Price'][0]
            price_ask_zero = order_book_ask_sum[order_book_ask_sum.QuantityDifference == 0.0]['Price'][0]
            order_book_bid = order_book_bid[order_book_bid.Price != price_bid_zero]
            order_book_ask = order_book_ask[order_book_ask.Price != price_ask_zero]
        elif len(order_book_bid_sum[order_book_bid_sum.QuantityDifference == 0.0]) != 0 and len(order_book_ask_sum[order_book_ask_sum.QuantityDifference == 0.0]) == 0:
            
            print 'Exist Bid Order Book Price = Zero'
            price_bid_zero = order_book_bid_sum[order_book_bid_sum.QuantityDifference == 0.0]['Price'][0]
            order_book_bid = order_book_bid[order_book_bid.Price != price_bid_zero]

        elif len(order_book_bid_sum[order_book_bid_sum.QuantityDifference == 0.0]) == 0 and len(order_book_ask_sum[order_book_ask_sum.QuantityDifference == 0.0]) != 0:
            
            print 'Exist Ask Order Book Price = Zero'
            price_ask_zero = order_book_ask_sum[order_book_ask_sum.QuantityDifference == 0.0]['Price'][0]
            order_book_ask = order_book_ask[order_book_ask.Price != price_ask_zero]

        order_book_bid_sum = order_book_bid_sum[order_book_bid_sum.QuantityDifference != 0].reset_index(drop = True)
        order_book_ask_sum = order_book_ask_sum[order_book_ask_sum.QuantityDifference != 0].reset_index(drop = True)
        order_book_bid_ask = pd.concat([order_book_bid_sum[['Price','QuantityDifference']],order_book_ask_sum[['Price','QuantityDifference']]],axis = 1)        
        
        return order_book_bid, order_book_ask, order_book_bid_ask, timestamp, y, index_find
    
    def with_first_order_book(best_price_number,year,month,day,timestamp,order_book_bid_ask,index_):
        with open('order_book_'+str(best_price_number)+'_'+str(year)+'_'+str(month)+'_'+str(day)+'.csv','a') as f:  
            order_book = csv.writer(f)
            if index_ == 0:
                order_book.writerow(["Bid","Bid_Quantity","Ask","Ask_Quantity"])
            order_book.writerow(["TimeStamp",timestamp])
            order_book = csv.writer(f,delimiter=',')
            for i in range(0,min(len(order_book_bid_ask),best_price_number),1):
                order_book.writerow(order_book_bid_ask[i:i+1].values.tolist()[0])     
    
    # 建立初始委託簿
    first_order_book_data_lenth = 0
    order_book_bid_time = 0
    order_book_ask_time = 0
    
    for time in range(0,1000,1):
        index_ = time
        order_book_bid, order_book_ask, order_book_bid_ask, timestamp, y, index_find = first_order_create(index_, data)  

        if len(order_book_bid) != 0 and len(order_book_ask) != 0:
            with_first_order_book(best_price_number,year,month,day,timestamp,order_book_bid_ask,index_)  
            break
        elif len(order_book_bid) == 0 and len(order_book_ask) != 0: 
            with_first_order_book(best_price_number,year,month,day,timestamp,order_book_bid_ask,index_)
            temp_ask +=1
        elif len(order_book_bid) != 0 and len(order_book_ask) == 0:
            with_first_order_book(best_price_number,year,month,day,timestamp,order_book_bid_ask,index_)
            temp_bid +=1
            
    print '-------------------------------------------'
    print 'index_find = %s'%(index_find)    
    
    for i in range(index_find + 1, len(data), 1):
        #print '---------------------------------'
        #print data[['Price','QuantityDifference','BidOrAsk','TimeStamp']][i:i+1]
        #print i ,temp_bid, temp_ask
        #print data.TimeStamp[i], x2[temp_bid], x1[temp_ask]
        time_second = int(data[i:i+1].TimeStamp.iloc[0][18]) + int(data[i:i+1].TimeStamp.iloc[0][17])*10 +\
                      int(data[i:i+1].TimeStamp.iloc[0][15])*60 + int(data[i:i+1].TimeStamp.iloc[0][14])*600 +\
                      int(data[i:i+1].TimeStamp.iloc[0][12])*3600 + int(data[i:i+1].TimeStamp.iloc[0][11])*36000

        if time_second > 57600:
            break
        if time_second == 32400 and time_second >= 57300:
            order_book_bid = order_book_bid.sort(['Price'],ascending = [False]).reset_index(drop = True)
            order_book_ask = order_book_ask.sort(['Price'],ascending = [True]).reset_index(drop = True)
            pass 
        
        if data.BidOrAsk[i] == 'A':
            data_ask_Quantity = data.BestQuantity[i]
            if int(data[['QuantityDifference']][i:i+1].values) > 0 :
                if order_book_bid.Price[0] >= data[i:i+1].Price.iloc[0] and time_second < 32400:
                    for k in range(0,len(order_book_bid)):
                        diff = order_book_bid.QuantityDifference_[k] - data[i:i+1].QuantityDifference_.iloc[0] 
                        if order_book_bid.Price[k] >= data[i:i+1].Price.iloc[0] and diff >= 0:
                            order_book_bid.QuantityDifference_[k] = diff
                            data[i:i+1].QuantityDifference_.iloc[0] = 0
                            break
                        elif order_book_bid.Price[k] >= data[i:i+1].Price.iloc[0] and diff < 0: 
                            order_book_bid.QuantityDifference_[k] = 0
                            data[i:i+1].QuantityDifference_.iloc[0] = -diff
                            pass
                        else:
                            break
                if data.TimeStamp[i] == x1[temp_ask]:
                    
                    position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                    order_book_ask = insert(order_book_ask,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)
                    if time_second > 32400 and time_second < 57300: 
                        if position_ == 0 and len(order_book_ask) > 1:   
                            if order_book_ask[position_ + 1:position_ + 1 + 1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:  
                                print 'Some error1(Ask & Q>0 & timestamp not change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:
                                pass
                        elif 0 < position_< (len(order_book_ask)-1):
                            if order_book_ask[position_ + 1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_ask[position_ - 1:position_ - 1 + 1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:
                                print 'Some error1(Ask & Q>0 & timestamp not change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:
                                pass
                        elif position_ == len(order_book_ask)-1:    
                            if order_book_ask[position_ - 1:position_ - 1 + 1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:        
                                print 'Some error1(Ask & Q>0 & timestamp not change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:
                                pass
                        elif position_ == 0 and len(order_book_ask) == 1:
                            pass
                    else:
                        pass
                elif data.TimeStamp[i] != x1[temp_ask]:
                    if temp_ask == 0:
                        temp_ask = temp_ask + 1
                        best_price = data[i:(i+1)]['BestPrice']
                        position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                        order_book_ask = insert(order_book_ask,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)                  

                        if time_second > 32400 and time_second < 57300:
                            if position_ == 0 and len(order_book_ask) > 1:
                                if order_book_ask[position_+1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:
                                    print 'Some error2(Ask & Q>0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])     
                                    break
                                else:
                                    pass
                            elif 0 < position_< len(order_book_ask)-1:
                                if order_book_ask[position_+ 1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_ask[position_-1:position_-1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]: 
                                    print 'Some error2(Ask & Q>0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])    
                                    break
                                else:
                                    pass
                            elif position_ == len(order_book_ask)-1: 
                                if order_book_ask[position_-1:position_-1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]: 
                                    print 'Some error2(Ask & Q>0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])      
                                    break
                                else:
                                    pass
                            elif position_ == 0 and len(order_book_ask) == 1:
                                pass
                        else:
                            pass
                    else:
                        order_book_bid_sum,order_book_ask_sum = order_book_to_csv(order_book_bid,order_book_ask,data,i)
                        if time_second > 32400 and time_second < 57300:
                            if round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) > 0.03 or\
                            round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) < 0:
                                if data[i-1:i].BidOrAsk.iloc[0] == 'A':
                                    if order_book_ask_sum[0:1].values.tolist()[0][1] == data[i-1:i].BestQuantity.iloc[0]:
                                        pass
                                    else:
                                        print 'Best ask quantity is false'
                                        pass
                                        #break 
                                else:
                                    j = i - 1
                                    while j >= 1:
                                        if data[j-1:j].BidOrAsk.iloc[0] == 'A':
                                            if order_book_ask_sum[0:1].values.tolist()[0][1] == data[j-1:j].BestQuantity.iloc[0]:
                                                break
                                        else:
                                            j = j - 1
                                            pass
                            else:
                                pass
                        else:
                            pass
                        position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                        temp_ask = temp_ask + 1
                       
                        order_book_ask = insert(order_book_ask,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)
                        if time_second > 32400 and time_second < 57300:
                            if position_ == 0:
                                 
                                if order_book_ask[position_+1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]: 
                                    print 'Some error3(Ask & Q>0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])     
                                    break
                                else:
                                    pass
                            elif 0 < position_< len(order_book_ask)-1:
                                if order_book_ask[position_+1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]: 
                                    print 'Some error3(Ask & Q>0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])    
                                    break
                                else:
                                    pass
                            elif position_ == len(order_book_ask)-1: 
                                if order_book_ask[position_-1:position_-1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]: 
                                    print 'Some error3(Ask & Q>0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])      
                                    break
                                else:
                                    pass
                            elif position_ == 0 and len(order_book_ask[0]) == 1:
                                pass
                        else:
                            pass
            elif int(data[['QuantityDifference']][i:i+1].values) < 0:    
                if data.TimeStamp[i] == x1[temp_ask]: 
                    order_number_ =  data['OrderNumber'][i:i + 1].iloc[0]
                    position_ = order_book_ask[order_book_ask.OrderNumber == order_number_].index[0]                
                    price_ = data[i:i+1]['Price'].iloc[0]
                    if time_second > 32400 and time_second < 57300:
                        if position_ == 0 and len(order_book_ask) > 1:
                            if order_book_ask[position_+1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:    
                                print 'Some error4(Ask & Q<0 & timestamp not change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:                  
                                pass
                        elif 0 < position_< len(order_book_ask)-1:
                            if order_book_ask[position_+1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:                             
                                print 'Some error4(Ask & Q<0 & timestamp not change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:  
                                pass 
                        elif position_ == len(order_book_ask)-1:
                            if position_ > 0 and order_book_ask[position_-1:position_-1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]: 
                                print 'Some error4(Ask & Q<0 & timestamp not change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])   
                                break
                            elif position_ == 0:
                                pass                        
                            else:                     
                                pass
                        elif position_ == 0 and len(order_book_ask) == 1:    
                            pass
                    else:
                        pass
                    if order_book_ask[(order_book_ask.OrderNumber == order_number_)&(order_book_ask.Price == price_)]['QuantityDifference'].iloc[0] == abs(data[i:i+1]['QuantityDifference'].iloc[0]):
                        order_book_ask = order_book_ask.drop(order_book_ask.index[[position_]]).reset_index(drop = True)                
                    else:
                        order_book_ask['QuantityDifference'][order_book_ask.OrderNumber == order_number_] = order_book_ask['QuantityDifference'][order_book_ask.OrderNumber == order_number_] + data[i:i+1]['QuantityDifference'].iloc[0]

                elif data.TimeStamp[i] != x1[temp_ask]:
                    
                    order_book_bid_sum,order_book_ask_sum = order_book_to_csv(order_book_bid,order_book_ask,data,i)
                    if time_second > 32400 and time_second < 57300:
                        if round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) > 0.03 or\
                        round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) < 0:
                            if data[i-1:i].BidOrAsk.iloc[0] == 'A':
                                if order_book_ask_sum[0:1].values.tolist()[0][1] == data[i-1:i].BestQuantity.iloc[0]:
                                    pass
                                else:
                                    print 'Best ask quantity is false'
                                    #break
                                    pass
                            else:
                                j = i - 1
                                while j >= 1:
                                    if data[j-1:j].BidOrAsk.iloc[0] == 'A':
                                        if order_book_ask_sum[0:1].values.tolist()[0][1] == data[j-1:j].BestQuantity.iloc[0]:
                                            break
                                    else:
                                        j = j - 1
                                        pass
                    else:
                        pass
                    order_number_ =  data['OrderNumber'][i : i + 1].iloc[0]
                    position_ = order_book_ask[order_book_ask.OrderNumber == order_number_].index[0]
                    price_ = data[i:i+1]['Price'].iloc[0]
                    temp_ask = temp_ask + 1
                    if time_second > 32400 and time_second < 57300:
                        if position_ == 0 and len(order_book_ask) > 1:
                            if order_book_ask[position_ + 1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:
                                print 'Some error5(Ask & Q<0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])    
                                break
                            else:
                                pass
                        elif 0 < position_< len(order_book_ask)-1:    
                            if order_book_ask[position_ + 1:position_+1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:                             
                                print 'Some error5(Ask & Q<0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])     
                                break
                            else:
                                pass
                        elif position_ == len(order_book_ask)-1:
                            if position_ > 0 and order_book_ask[position_-1:position_-1 + 1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]: 
                                print 'Some error5(Ask & Q<0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])      
                                break
                            elif position_ == 0:
                                pass                       
                            else:                       
                                pass
                        elif position_ == 0 and len(order_book_ask) == 1:
                            pass      
                    else:
                        pass
                    if order_book_ask[(order_book_ask.OrderNumber == order_number_)&(order_book_ask.Price == price_)]['QuantityDifference'].iloc[0] == abs(data[i:i+1]['QuantityDifference'].iloc[0]):                    
                        order_book_ask = order_book_ask.drop(order_book_ask.index[[position_]]).reset_index(drop = True)
                    else:
                        order_book_ask['QuantityDifference'][order_book_ask.OrderNumber == order_number_] = order_book_ask['QuantityDifference'][order_book_ask.OrderNumber == order_number_] + data[i:i+1]['QuantityDifference'].iloc[0]

        elif data.BidOrAsk[i] == 'B':
            data_bid_Quantity = data.BestQuantity[i]
            if int(data[['QuantityDifference']][i:i+1].values) > 0: 
               
                if order_book_ask.Price[0] <= data[i:i+1].Price.iloc[0] and time_second < 32400:
                    for k in range(0,len(order_book_ask)):
                        diff = order_book_ask.QuantityDifference_[k] - data[i:i+1].QuantityDifference_.iloc[0]
                        if order_book_ask.Price[k] <= data[i:i+1].Price.iloc[0] and diff >= 0:
                            order_book_ask.QuantityDifference_[k] = diff
                            data[i:i+1].QuantityDifference_.iloc[0] = 0
                            break
                        elif order_book_ask.Price[k] <= data[i:i+1].Price.iloc[0] and diff < 0:
                            order_book_ask.QuantityDifference_[k] = 0
                            data[i:i+1].QuantityDifference_.iloc[0] = - diff
                            pass
                        else:
                            break
                if data.TimeStamp[i] == x2[temp_bid]:
                    position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                    order_book_bid = insert(order_book_bid,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)                
                    if time_second > 32400 and time_second < 57300:
                        if position_ == 0 and len(order_book_bid) > 1:              
                            if order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                                            
                                print 'Some error1(Bid & Q>0 & timestamp not change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:                    
                                pass 
                        elif 0 < position_< len(order_book_bid)-1: 
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                             
                                print 'Some error1(Bid & Q>0 & timestamp not change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break    
                            else:   
                                pass   
                        elif position_ == len(order_book_bid)-1 and len(order_book_bid) > 1:   
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:                        
                                print 'Some error1(Bid & Q>0 & timestamp not change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:                
                                pass
                        elif position_ == 0 and len(order_book_bid[temp_bid]) == 1:
                            pass 
                    else:
                        pass
                elif data.TimeStamp[i] != x2[temp_bid]:
                    if temp_bid == 0:
                        best_price = data[i:(i+1)]['BestPrice']             
                        position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                        temp_bid = temp_bid + 1                 
                        order_book_bid = insert(order_book_bid,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)                                     
                        if time_second > 32400 and time_second < 57300:
                            if position_ == 0  and len(order_book_bid) > 1:
                                if order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0] or order_book_bid['Price'][0:1].iloc[0] != data['BestPrice'][i]:                                
                                    print 'Some error2(Bid & Q>0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0]) + data['OrderNumber'][i:i+1].iloc[0]
                                    break
                                else:                   
                                    pass      
                            elif 0 < position_< len(order_book_bid)-1:    
                                if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                                
                                    print 'Some error2(Bid & Q>0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                    break
                                else: 
                                    pass
                            elif position_ == len(order_book_bid)-1:
                                if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid['Price'][0:1].iloc[0] != data['BestPrice'][i]:                                
                                    print 'Some error2(Bid & Q>0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])                                        
                                    pass
                                else:
                                    pass
                            elif position_ == 0 and len(order_book_bid) == 1: 
                                    pass
                        else:
                            pass
                    else:
                        if time_second > 32400 and time_second < 57300:
                            if round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) > 0.03 or\
                            round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) < 0:
                                order_book_bid_sum,order_book_ask_sum = order_book_to_csv(order_book_bid,order_book_ask,data,i)                    
                                if data[i-1:i].BidOrAsk.iloc[0] == 'B':
                                    if order_book_bid_sum[0:1].values.tolist()[0][1] == data[i-1:i].BestQuantity.iloc[0]:
                                        pass
                                    else:
                                        print 'Best bid quantity is false'
                                        #break
                                        pass
                                else:
                                    j = i - 1
                                    while j >= 1:
                                        if data[j-1:j].BidOrAsk.iloc[0] == 'B':
                                            if order_book_bid_sum[0:1].values.tolist()[0][1] == data[j-1:j].BestQuantity.iloc[0]:
                                                break
                                            else:
                                                print 'Best bid quantity is false'
                                                #break
                                                pass
                                        else:
                                            j = j - 1
                                            pass
                        else:
                            pass
                        position_ = int(data[['OrderBookPosition']][i:i+1].iloc[0]) - 1 
                        temp_bid = temp_bid + 1 
                        order_book_bid = insert(order_book_bid,data[['Price','OrderNumber','QuantityDifference','QuantityDifference_']][i:i+1],position_)                       
                        if time_second > 32400 and time_second < 57300:
                            if position_ == 0 and len(order_book_bid) > 1:
                                if order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0] or order_book_bid['Price'][0:1].iloc[0] != data['BestPrice'][i]:                                
                                    print 'Some error3(Bid & Q>0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])     
                                    break
                                else:                    
                                    pass
                            elif 0 < position_< len(order_book_bid)-1:    
                                if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                                
                                    print 'Some error3(Bid & Q>0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                    break
                                else: 
                                    pass
                            elif position_ == len(order_book_bid)-1:   
                                if order_book_bid[position_-1:position_-1 + 1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid['Price'][0:1].iloc[0] != data['BestPrice'][i]:                                
                                    print 'Some error3(Bid & Q>0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])      
                                    break
                                else:                      
                                    pass
                            elif position_ == 0 and len(order_book_bid[0]) == 1:
                                pass
                        else:
                            pass
            elif int(data[['QuantityDifference']][i:i+1].values) < 0:    
                if data.TimeStamp[i] == x2[temp_bid]: 
                    order_number_ =  data['OrderNumber'][i : i + 1].iloc[0]
                    position_ = order_book_bid[order_book_bid.OrderNumber == order_number_].index[0]                
                    price_ = data[i:i+1]['Price'].iloc[0]
                    if time_second > 32400 and time_second < 57300:
                        if position_ == 0 and len(order_book_bid) > 1:    
                            if order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error4(Bid & Q<0 & timestamp not change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:                     
                                pass               
                        elif 0 < position_< len(order_book_bid)-1:      
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error4(Bid & Q<0 & timestamp not change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else: 
                                pass
                        elif position_ == len(order_book_bid)-1:    
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error4(Bid & Q<0 & timestamp not change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])      
                                break
                            elif position_ == 0:
                                pass
                            else:                        
                                pass
                        elif position_ == 0 and len(order_book_bid) == 1:
                            pass
                    else:
                        pass
                    if order_book_bid[(order_book_bid.OrderNumber == order_number_)&(order_book_bid.Price == price_)]['QuantityDifference'].iloc[0] == abs(data[i:i+1]['QuantityDifference'].iloc[0]):                    
                        order_book_bid = order_book_bid.drop(order_book_bid.index[[position_]]).reset_index(drop = True)                
                    else:
                        order_book_bid['QuantityDifference'][order_book_bid.OrderNumber == order_number_] = order_book_bid['QuantityDifference'][order_book_bid.OrderNumber == order_number_] + data[i:i+1]['QuantityDifference'].iloc[0]                            
                elif data.TimeStamp[i] != x2[temp_bid]:
                    if time_second > 32400 and time_second < 57300:
                        if round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) > 0.03 or\
                        round(float(data[i:i+1].TimeStamp.iloc[0][18:29]) - float(data[i-1:i].TimeStamp.iloc[0][18:28]),4) < 0:
                            order_book_bid_sum,order_book_ask_sum = order_book_to_csv(order_book_bid,order_book_ask,data,i)
                            if data[i-1:i].BidOrAsk.iloc[0] == 'B':
                                if order_book_bid_sum[0:1].values.tolist()[0][1] == data[i-1:i].BestQuantity.iloc[0]:
                                    pass
                                else:
                                    print 'Best bid quantity is false'
                                    #break
                                    pass
                            else:
                                j = i - 1
                                while j >= 1:
                                    if data[j-1:j].BidOrAsk.iloc[0] == 'B':
                                        if order_book_bid_sum[0:1].values.tolist()[0][1] == data[j-1:j].BestQuantity.iloc[0]:
                                            break
                                        else:
                                            print 'Best bid quantity is false'
                                            #break
                                            pass
                                    else:
                                        j = j - 1
                                        pass
                    else:
                        pass
                    order_number_ =  data['OrderNumber'][i:i+1].iloc[0]
                    position_ = order_book_bid[order_book_bid.OrderNumber == order_number_].index[0]
                    price_ = data[i:i+1]['Price'].iloc[0]
                    temp_bid = temp_bid + 1
                    if time_second > 32400 and time_second < 57300:
                        if position_ == 0 and len(order_book_bid) > 1:   
                            if order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error5(Bid & Q<0 & timestamp change & 1),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:                   
                                pass   
                        elif 0 < position_< len(order_book_bid)-1:    
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0] or order_book_bid[position_+1:position_+1+1]["Price"].iloc[0] > data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error5(Bid & Q<0 & timestamp change & 2),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            else:  
                                pass
                        elif position_ == len(order_book_bid)-1:    
                            if order_book_bid[position_-1:position_-1+1]["Price"].iloc[0] < data['Price'][i:i+1].iloc[0]:                            
                                print 'Some error5(Bid & Q<0 & timestamp change & 3),position = %d,index = %d,price = %d,OrderNumber = %s'%(position_,i,data['Price'][i:i+1].iloc[0],data['OrderNumber'][i:i+1].iloc[0])
                                break
                            elif position_ == 0:
                                pass
                            else:                      
                                pass    
                        elif position_ == 0 and len(order_book_bid) == 1:
                            pass  
                    else:
                        pass
                    if order_book_bid[(order_book_bid.OrderNumber == order_number_)&(order_book_bid.Price == price_)]['QuantityDifference'].iloc[0] == abs(data[i:i+1]['QuantityDifference'].iloc[0]):
                        order_book_bid = order_book_bid.drop(order_book_bid.index[[position_]]).reset_index(drop = True)                
                    else:
                        order_book_bid['QuantityDifference'][order_book_bid.OrderNumber == order_number_] = order_book_bid['QuantityDifference'][order_book_bid.OrderNumber == order_number_] + data[i:i+1]['QuantityDifference'].iloc[0]
    return data, order_book_bid, order_book_ask #, order_book_bid_sum, order_book_ask_sum

if __name__ == '__main__':
    
    path = 'C:\\Users\\banking\\Documents\\rory\\SGX Tick Data\\CN_Futures_'
    year = 2014
    best_price_number = 3
    
    # Future Delivery Months 近月合約代碼 : series
    # 2014 :CNF14:1月, CNG14:2月, CNH14:3月, CNJ14:4月, CNK14:5月, CNM14:6月,
    #       CNN14:7月, CNQ14:8月, CNU14:9月, CNV14:10月, CNX14:11月, CNZ14:12月
    # 2015 :CNF15:1月, CNG15:2月, CNH15:3月, CNJ15:4月, CNK15:5月, CNM15:6月,
    #       CNN15:7月, CNQ15:8月, CNU15:9月, CNV15:10月, CNX15:11月, CNZ15:12月
        
    series = 'CNZ14' 
    month = 12
    day_ = [29] #25,26 data exist bugs
    for i in day_:
        print i
        start = time.time()
        data, order_book_bid, order_book_ask = order_book_tranform(year,month,i,path,best_price_number,series)
        end = time.time()
        print "Total time = %f"%(end - start)    
        
    series = 'CNF15' 
    month = 12
    day_ = [30,31]
    for i in day_:
        print i
        start = time.time()
        data, order_book_bid, order_book_ask = order_book_tranform(year,month,i,path,best_price_number,series)
        end = time.time()
        print "Total time = %f"%(end - start) 
        
        
        
        
        