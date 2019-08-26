# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:49:47 2019

@author: eric.qian
"""

import numpy as np
from vectors import discount, cashflow


class Asset():
    
    
    def __init__(self,
                 capital = 0,
                 discount_rate = 0,
                 periods = 100,
                 period = 1):
        
        period_dict = {'yearly': 1,
                       'quarterly': 4,
                       'monthly': 12,
                       'weekly': 52,
                       'daily': 365}
        
        self.capital = capital
        self.periods = periods
        self.period = period
        self.t = periods
        self.discount_rate = discount_rate
        self.revenues = {}
        self.expenses = {}
        self.taxes = {}
        self.royalties = {}
        self.t_b = None
        self.irr = None
        self.npv = 0
        self.dcf = np.array([0 for i in range(self.t)], dtype = np.float32)
        self.cf = np.array([0 for i in range(self.t)], dtype = np.float32)
        self.cum_dcf = np.array([0 for i in range(self.t)], dtype = np.float32)
        
        if type(period) == str:
            
            try:
                self.period = period_dict[period]
            except:
                raise ValueError('Valid period str types: yearly, quarterly, monthly, weekly, daily')
                
        if type(period) == int:
            
            self.period = period
            
        if not self.period:
            
            raise ValueError('Properly define the period as str descriptor or int of annualized period')
        
        self.discount = discount(self.discount_rate, self.period, self.periods).vector

    
    def add_revenue(self,
                    name = '',
                    cash_vector = None,
                    units = None,
                    price = None,
                    change = None,
                    rate_of_change = 0,
                    init_val = 0):
        
        self.revenues[name] =  cashflow(cash_vector = cash_vector,
                                 units = units,
                                 price = price,
                                 change = change,
                                 rate_of_change = rate_of_change,
                                 init_val = init_val,
                                 periods = self.periods,
                                 period = self.period
                                 ).vector
        
        
    def add_expense(self,
                    name = '',
                    cash_vector = None,
                    units = None,
                    price = None,
                    change = None,
                    rate_of_change = 0,
                    init_val = 0):
        
        self.expenses[name] =  cashflow(cash_vector = cash_vector,
                                 units = units,
                                 price = price,
                                 change = change,
                                 rate_of_change = rate_of_change,
                                 init_val = init_val,
                                 periods = self.periods,
                                 period = self.period
                                 ).vector
    
    
    def add_tax(self,
                name,
                rate):
        
        self.taxes[name] = rate
        
    
    def add_royalty(self,
                    name,
                    rate):
    
        self.taxes[name] = rate
        
        
    def calc_cf(self):
        
        for k, revenue in self.revenues.items():
            self.cf += revenue
            
        self.cf = self.cf * (1-sum(list(self.royalties.items())))
        
        for k, expense in self.expenses.items():
            self.cf -= expense
        
        return self.cf

        
    def calc_dcf(self):
        
        for k, revenue in self.revenues.items():
            self.dcf += revenue
            
        self.dcf = self.dcf * (1-sum(list(self.royalties.items())))

        for k, expense in self.expenses.items():
            self.dcf -= expense
            
        self.dcf = self.dcf * self.discount 
        
        return self.dcf
    
    
    def calc_atax_npv(self):
        
        self.calc_dcf()
        effective_rate = sum(list(self.taxes.items()))
        self.npv = sum(self.dcf * (1-effective_rate)) - self.capital 
        
        return self.npv


    def calc_btax_npv(self):
        
        self.calc_dcf()
        self.npv = sum(self.dcf) - self.capital
        
        return self.npv

    
    def calc_cum_dcf(self):
        
        self.calc_dcf()
        self.cum_dcf = np.cumsum(self.dcf)
        
        return self.cum_dcf
    
    
    def breakeven(self):
        
        self.calc_cum_dcf()
        cum_dcf = self.cum_dcf - self.capital
        
        for i, val in enumerate(cum_dcf):
            
            if val > 0:
                self.t_b = i            
                break
        
        return self.t_b
        
    
    def calc_irr(self):
        
        threshold = self.capital * .01
        npv = 0
        self.calc_cf()
        
        for disc in range(1,10000):
            
            curr_disc = discount(disc/10000, self.period, self.periods).vector
            dcf = self.cf * curr_disc
            npv = sum(dcf) - self.capital
            
            if abs(npv) < threshold: 
                self.irr = disc
                break
            
        return self.irr


