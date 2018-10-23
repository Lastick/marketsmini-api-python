#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright (c) 2016-2018, Karbo developers (Lastick)
#
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from urlparse import urlparse
import urllib
import httplib
import json
from time import sleep
import sys

class MarketsminiAPI:

  socket_status = False
  api_status = False
  api_url = 'https://karbo-labs.pp.ua/services/markets/api/ticker.json'
  pairs = ['UAH', 'USD', 'EUR', 'RUR', 'BTC']
  user_agent = "KarboStatsMinibot/1.0"

  def __init__(self):
    pass

  def client(self):
    buff = ''
    self.socket_status = False
    try:
      o = urlparse(self.api_url)
      conn = httplib.HTTPSConnection(o.hostname, 443, timeout=15);
      headers = {"User-Agent": self.user_agent}
      sleep(0.07)
      conn.request("GET", o.path, '', headers)
      res = conn.getresponse()
      if (res.status == 200):
        buff = res.read()
        self.socket_status = True
        conn.close()
    except Exception as e:
      self.socket_status = False
      print('-> Markets error: ' + str(e))
    return buff;

  def getTicker(self):
    res = {'ccys' : [], 'change': 0, 'cap': 0}
    res_data = {}
    buy = 0.0
    sell = 0.0
    vol = 0.0
    price = 0.0
    change = 0.0
    cap = 0.0
    get_status_t = False
    res_data = self.client()
    if (self.socket_status):
      try:
        json_obj = json.loads(res_data)
        if ('status' in json_obj):
          if (json_obj['status'] == True):
            if ('ticker' in json_obj):
              ticker_root = json_obj['ticker']
              if ('ccys' in ticker_root):
                ccys = ticker_root['ccys']
                for pair in self.pairs:
                  buy = 0.0
                  sell = 0.0
                  vol = 0.0
                  price = 0.0
                  if (pair in ccys):
                    ticker_target = ccys[pair]
                    if ('buy' in ticker_target):
                      buy = ticker_target['buy']
                    if ('sell' in ticker_target):
                      sell = ticker_target['sell']
                    #if ('price' in ticker_target):
                    #  price = ticker_target['price']
                    price = (buy + sell) / 2
                    if ('vol' in ticker_target):
                      vol = ticker_target['vol']
                  res['ccys'].append({'pair': pair, 'buy': buy, 'sell': sell, 'price': price, 'vol': vol})
              if ('change' in ticker_root):
                change = ticker_root['change']
              res['change'] = change
              #if ('cap' in ticker_root):
              #  cap = ticker_root['cap']
              res['cap'] =  cap
            get_status_t = True
      except:
        get_status_t = False
    if (get_status_t):
      self.api_status = True
    else:
      self.api_status = False
    #print(res)
    return res

  def getStatus(self):
    return self.api_status
