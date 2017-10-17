# coding: utf-8

import requests, gevent, time
from pyquery import PyQuery
from gevent import monkey; monkey.patch_all()
from gevent.queue import Queue

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_director():
    directory_queue = Queue()
    html = requests.get('http://www.douyu.com/directory').text
    pq = PyQuery(html)
    size = pq.find('.unit').size()
    for index in range(size):
        item = pq.find('.unit').eq(index)
        name = item.find('p').text()
        url = item.find('a').attr('href')
        img = item.find('img').attr('data-original')
        directory_queue.put({
            'name': name,
            'url': 'http://www.douyu.com' + url,
            'img': img
        })
    return directory_queue

def get_rooms(queue):
    while not queue.empty():
        directory_info = queue.get_nowait()
        print('[%s]Getting Directory => %s'%(gevent.getcurrent(), directory_info['name']))
        html = requests.get(directory_info['url']).text
        pq = PyQuery(html)
        size = pq.find('#live-list-contentbox > li').size()
        for index in range(size):
            item = pq.find('#live-list-contentbox > li').eq(index)
            title = item.find('a').attr('title')
            url = 'http://www.douyu.com' + item.find('a').attr('href')
            username = item.find('.dy-name').text()
            cat = directory_info['name']
            viewers = item.find('.dy-num').text()
            content = '''
房间标题 => %s
主播名称 => %s
观众数量 => %s
分类栏目 => %s
房间链接 => %s
'''%(title, username, viewers, cat, url)
            with open('result.txt', 'a') as f:
                f.write(content)
if __name__ == '__main__':
    start = time.time()
    gevent_list = []
    directory_queue = get_director()
    for index in range(20):
        gevent_list.append(
            gevent.spawn(get_rooms, directory_queue)
        )
    gevent.joinall(gevent_list)
    print('Total run time: %s' %(str(time.time()-start)))