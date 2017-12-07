#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-12 10:26:53
# @Author  : zhanghong (zhanghonged@126.com)
# @Link    : http://blog.codecp.org/
# @Version : $Id$

from urlparse import urljoin

import csv
import requests
from bs4 import BeautifulSoup

URL='http://xa.ganji.com/fang1/o{page}'
ADDR='http://xa.ganji.com'

start_page=0
end_page=1


def do(x):
	return x.string.encode("gbk").strip()

with open('god.csv',"wb") as f:
	csv_writer= csv.writer(f, delimiter=',')
	print "start..."
	while start_page < end_page:
		start_page+=1
		print "get:{0}".format(URL.format(page=start_page))
		response=requests.get(URL.format(page=start_page))
		html=BeautifulSoup(response.text,"html.parser")
		house_list=html.select(".f-list-item > .f-list-item-wrap")

		if not house_list:
			break
		for house in house_list:
			house_title=house.select(".title > a")[0].string.encode("gbk")
			house_addr_temp=map(do,house.select(".address > .area > .address-eara"))
			#去除list里的空值
			while '' in house_addr_temp:
				house_addr_temp.remove('')
			house_addr='-'.join(house_addr_temp)
			house_price=house.select(".info > .price > .num")[0].string.encode("gbk")+house.select(".info > .price > .yue")[0].string.encode("gbk")
			house_url=urljoin(ADDR,house.select(".title > a")[0]['href'])
			csv_writer.writerow([house_title,house_addr,house_price,house_url])
	print "end..."

