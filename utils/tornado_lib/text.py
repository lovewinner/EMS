#! /usr/bin/env python
#coding=utf-8
import os
import os.path as osp
from random import randint, randrange
import string
import urllib


def get_in(data, b, e=None, start=0, flag=False):
    if data is None:
        return None
    b1 = data.find(b, start)
    if b1 == -1:
        return None
    b1 += len(b)
    if e is None:
        return data[b1:]
    if isinstance(e, list):
        e1 = -1
        for i in range(b1 + 1, len(data)):
            if data[i] in e:
                e1 = i
                break
    else:
        e1 = data.find(e, b1)
    if e1 == -1:
        if flag:
            return data[b1:]
        return None
    return data[b1:e1]


def get_in_list(data, b, e, start=0):
    if data is None:
        return
    while True:
        b1 = data.find(b, start)
        if b1 == -1:
            return
        b1 += len(b)
        e1 = data.find(e, b1)
        if e1 == -1:
            return
        yield data[b1:e1]
        start = e1


def rnd_str(num):
    if not num:
        return ''
    result = []
    for i in range(num):
        result.append(chr(randint(97, 122)))
    return ''.join(result)

letters = '0123456789' + string.ascii_letters


def rnd_letters(num):
    if not num:
        return ''
    result = []
    l = len(letters)
    for i in range(num):
        result.append(letters[randrange(0, l)])
    return ''.join(result)


def force_unicode(s):
    if isinstance(s, unicode):
        return s
    try:
        s = s.decode('gbk')
        if isinstance(s, unicode):
            return s
    except:
        pass

    try:
        s = s.decode('utf-8')
        if isinstance(s, unicode):
            return s
    except:
        pass
    try:
        import chardet
        res = chardet.detect(s)
        try:
            s = s.decode(res['encoding'])
            if isinstance(s, unicode):
                return s
        except:
            pass
    except:
        pass
    return s


def force_write(filename, content, mode='wb'):
    path = osp.dirname(osp.abspath(filename))
    if not osp.exists(path):
        os.makedirs(path)
    return file(filename, mode).write(content)


def add_querystr(url, param):
    if not param:
        return url
    if isinstance(param, dict):
        param = urllib.urlencode(param)
    if url.endswith('?') or url.endswith('&'):
        return url + param
    if url.find('?') == -1:
        return url + '?' + param
    return url + '&' + param
