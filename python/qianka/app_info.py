# -*- coding: utf-8 -*-

import json
import time

import msgpack


class AppInfo(object):
    """
    已安装应用的信息

    item_id(appid), bundle_id, bundle_type, purchase_date, redownload
    """
    def __init__(self, **kwargs):
        try:
            item_id = int(kwargs.get('item_id'))
        except:
            item_id = 0
        bundle_id = kwargs.get('bundle_id', '')

        if item_id == 0 and bundle_id == '':
            raise ValueError('item_id and bundle_id missed')

        self.appid = item_id
        self.bundle_id = bundle_id
        self.bundle_type = str(kwargs.get('bundle_type', ''))

        try:
            self.dsid = int(kwargs.get('dsid'))
        except:
            # dsid 为空字符串或不合法，为数据库 unique key 做特殊处理，设成 -1
            self.dsid = -1

        self.redownload = kwargs.get('redownload')
        if self.redownload is True or self.redownload == 1:
            self.redownload = 1
        else:
            self.redownload = 0

        try:
            self.purchase_date = int(kwargs.get('purchase_date'))
        except:
            self.purchase_date = 0

        if self.purchase_date <= 0:
            self.purchase_date = int(time.time()) # 改成可以收集的到的最早时间

    def __eq__(self, other):
        return self.key_v2 == other.key_v2

    def __repr__(self):
        return json.dumps(self.value_v2())

    def __hash__(self):
        return hash(self.key_v2)

    def from_app_store(self):
        """
        item_id(appid) != 0 时从 App Store 下载
        """
        return self.appid != 0

    @property
    def key(self):
        if self.from_app_store():
            return int(self.appid)
        else:
            return str(self.bundle_id)

    def value(self, to_bytes=True):
        if self.from_app_store():
            v = [self.dsid, self.purchase_date, self.redownload]
        else:
            v = [self.purchase_date, self.redownload]
        if to_bytes:
            return msgpack.packb(v, encoding='utf-8')
        else:
            return v

    @staticmethod
    def to_list(lppa):
        if type(lppa) != type([]):
            return []

        list_ = []
        for app_dict in lppa:
            try:
                app_info = AppInfo(**app_dict)
                list_.append(app_info)
            except:
                pass

        return list_

    @staticmethod
    def list_to_dict(app_list):
        return {app_info.key: app_info.value(to_bytes=False)
                for app_info in app_list}

    @property
    def key_v2(self):
        if self.from_app_store():
            return int(self.appid)
        else:
            return '0:%s' % self.bundle_id

    def value_v2(self):
        return {
            'item_id': self.appid,
            'bundle_id': self.bundle_id,
            'bundle_type': self.bundle_type,
            'dsid': self.dsid,
            'purchase_date': self.purchase_date,
            'redownload': self.redownload,
        }

    @staticmethod
    def list_to_dict_v2(app_list):
        return {app_info.key_v2: app_info.value_v2() for app_info in app_list}

    @staticmethod
    def from_v1(key, value):
        try:
            if len(value) == 3:
                item_id = int(key)
                dsid, purchase_date, redownload = value
                bundle_id = ''
                bundle_type = ''
            elif len(value) == 2:
                bundle_id = str(key)
                purchase_date, redownload = value
                item_id = 0
                dsid = 0
                bundle_type = ''
            else:
                return None
            item = dict(item_id=item_id, dsid=dsid,
                        bundle_id=bundle_id, bundle_type=bundle_type,
                        purchase_date=purchase_date, redownload=redownload)
            return AppInfo(**item)
        except:
            return None


if __name__ == '__main__':
    # 来自 keys.update_state 的数据，也是 v2 版本格式
    app_dict = {
        'item_id': 395096736,
        'bundle_id': 'com.ctrip',
        'bundle_type': 'User',
        'dsid': 10126730231,
        'purchase_date': 1482816931,
        'redownload': 1,
    }
    # v1 版本格式
    k1, v1 = (395096736, [10126730231, 1482816931, 1])
    k2, v2 = ('com.ctrip', [1482816931, 1])

    # 测试接收 keys.update_state 数据没有问题
    app_info = AppInfo(**app_dict)
    # 测试兼容 v1 版本数据
    app_info_1 = AppInfo.from_v1(k1, v1)
    app_info_2 = AppInfo.from_v1(k2, v2)

    # 测试 from_app_store/key/key_v2 方法正常
    assert(app_info.from_app_store())
    assert(app_info.key == 395096736)
    assert(app_info.key_v2 == 395096736)

    assert(app_info_1.from_app_store())
    assert(app_info_1.key == 395096736)
    assert(app_info_1.key_v2 == 395096736)

    assert(not app_info_2.from_app_store())
    assert(app_info_2.key == 'com.ctrip')
    assert(app_info_2.key_v2 == '0:com.ctrip')

    # == 比较两个 app_info 是不是同一个应用(__eq__)
    assert(app_info == app_info_1)
    assert(app_info != app_info_2)
    # in 来判断 app_info 是否在列表中
    assert(app_info_1 in [app_info])
    assert(app_info_2 not in [app_info])
    # 可以使用集合操作
    assert(len(set([app_info]) - set([app_info_1])) == 0)
    assert(len(set([app_info]) - set([app_info_2])) == 1)
