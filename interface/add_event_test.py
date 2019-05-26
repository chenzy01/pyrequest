import os
import sys
import unittest

import requests

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from pyrequest.db_fixture import test_data


class AddEventTest(unittest.TestCase):
    # 添加发布会
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    def tearDown(self):
        print(self.result)

    def test_add_event_all_null(self):
        # 所有参数为空
        payload = {'id': '', 'name': '', '`limit`': '', 'address': '', 'start_time': '', 'create_time': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status', 10021])
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_eid_exist(self):
        # id 已存在
        payload = {'id': 1, 'name': '一加4发布会', '`limit`': 20000, 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id is already exist')

    def test_add_event_name_exist(self):
        # 名称已存在
        payload = {'id': 11, 'name': '红米发布会', '`limit`': 2000, 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exist')

    def test_add_event_data_type_error(self):
        # 日期格式错误
        payload = {'id': 6, 'name': '一加4发布会', '`limit`': 2000, 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error.', self.result['message'])

    def test_add_event_success(self):
        # 添加成功
        payload = {'id': 7, 'name': '红米 Pro 发布会', 'limit': 2000, 'address': '深圳宝体',
                   'start_time': '2017-05-10 12:00:00', 'create_time': '2017-05-10 12:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    test_data.init_data()  # 初始化接口数据
    unittest.main()








