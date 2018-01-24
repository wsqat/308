#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from cStringIO import StringIO


def load_configs(column='config', config_ini_path='config.ini'):
    _cp = ConfigParser()
    fp = open(config_ini_path, 'rb')
    content = fp.read()
    fp.close()
    # 替换bom信息
    content = content.replace('\xef\xbb\xbf', '')
    fp = StringIO(content)
    _cp.readfp(fp)
    return _cp.items(column)


configs = dict(load_configs())


class IniConfig(object):

    def __getattribute__(self, *args, **kwargs):
        val = configs.get(args[0], '').strip()
        return val


ini_config = IniConfig()
