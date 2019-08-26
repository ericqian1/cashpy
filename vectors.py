# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:55:56 2019

@author: eric.qian
"""

from base import stream

        
class discount(stream):
    
    
    def __init__(self,
                 discount_rate = 0,
                 period = None,
                 t = 100):
        
        period_dict = {'yearly': 1,
                       'quarterly': 4,
                       'monthly': 12,
                       'weekly': 52,
                       'daily': 365}
        
        self.discount_rate = discount_rate
        
        if type(period) == str:
            
            try:
                self.period = period_dict[period]
            except:
                raise ValueError('Valid period str types: yearly, quarterly, monthly, weekly, daily')
                
        if type(period) == int:
            
            self.period = period
            
        if not self.period:
            
            raise ValueError('Properly define the period as str descriptor or int of annualized period')
            
        super().__init__(init_val = 1,
                         change = lambda i, t: 1/(1 + self.discount_rate/self.period)**(self.period * (t/self.period)),
                         t = t)


class cashflow(stream):
    
    
    def __init__(self,
                 cash_vector = None,
                 units = None,
                 price = None,
                 change = None,
                 rate_of_change = 0,
                 init_val = 0,
                 periods = 0,
                 period = 1):
        
        self.rate_of_change = rate_of_change
        self.units = units
        self.price = price
        self.period = period
        self.periods = periods
        self.init_val = init_val
        
        if rate_of_change: 
            
            self.change =  lambda i, t: i*(1 + self.rate_of_change/self.period)**(self.period * (t/self.period))
            
        else:

            self.change = change            
        
        if cash_vector:
            
            super().__init__(cash_vector)
            
        elif units and price:
            
            super().__init__(init_val = self.units * self.price,
                             change = self.change,
                             t = self.periods)

        elif init_val and periods:
            
            super().__init__(init_val = init_val,
                             change = self.change,
                             t = self.periods)
        

