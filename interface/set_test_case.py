import unittest
import requests


class GetEventListTest(unittest.TestCase):
    # 查询发布会信息（带用户验证）

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_get_event_list"

    def test_get_event_list_auth_null(self):
        # auth 为空
        r = requests.get(self.base_url, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'user auth null')

    def test_get_event_list_auth_error(self):
        # auth 错误
        auth_user = ('abc', '123')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user auth fail')

    def test_get_event_list_eid_null(self):
        # eid 参数为空
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['satatus'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_list_eid_success(self):
        # 根据 eid 查询成功
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['satatus'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], u'小米5发布会')
        self.assertEqual(result['data']['address'], u'北京国家会议中心')


if __name__ == '__main__':
    unittest.main()
