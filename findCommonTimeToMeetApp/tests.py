from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.user_url = '/api/v1/user/'
        self.userTimingPreferences_url = '/api/v1/userTimingPreferences/'
        self.users = [
            {
                'username': 'user1',
                'password': 'user1',
                'timing_preferences': {
                    "day_start_time": "09:00:00",
                    "day_end_time": "21:00:00",
                    "time_zone": "Asia/Kolkata"
                },
                "cal_info": {
                    "calendars": {
                        "primary": {
                            "busy": [
                                {
                                    "start": "2022-06-04T09:00:00+05:30",
                                    "end": "2022-06-04T10:00:00+05:30"
                                },
                                {
                                    "start": "2022-06-04T12:00:00+05:30",
                                    "end": "2022-06-04T14:00:00+05:30"
                                }
                            ]
                        }
                    }
                }
            },
            {
                'username': 'user2',
                'password': 'user2',
                'timing_preferences': {
                    "day_start_time": "09:00:00",
                    "day_end_time": "21:00:00",
                    "time_zone": "Europe/London"
                },
                "cal_info": {
                    "calendars": {
                        "primary": {
                            "busy": [
                                {
                                    "start": "2022-06-04T10:00:00+05:30",
                                    "end": "2022-06-04T11:00:00+05:30"
                                },
                                {
                                    "start": "2022-06-04T12:00+05:30",
                                    "end": "2022-06-04T13:00:00+05:30"
                                }
                            ]
                        }
                    }
                }
            }
        ]
        self.slots = [
            {
                'start': '2022-06-04T14:30:00+05:30',
                'end': '2022-06-04T15:30:00+05:30'
            },
            {
                'start': '2022-06-04T15:30:00+05:30',
                'end': '2022-06-04T16:30:00+05:30'
            },
            {
                'start': '2022-06-04T16:30:00+05:30',
                'end': '2022-06-04T17:30:00+05:30'
            }
        ]

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestAPI(TestSetUp):
    def create_userTimingPreferences(self, user):
        res = self.client.post(self.userTimingPreferences_url,
                               user['timing_preferences'])
        return res

    def create_user(self, user):
        res = self.create_userTimingPreferences(user)
        payload = {
            "username": user['username'],
            "password": user['password'],
            'timing_preferences': res.data['id']
        }
        res = self.client.post(self.user_url, payload)
        return res

    def test_create_userTimingPreferences(self):
        res = self.create_userTimingPreferences(self.users[0])
        self.assertEqual(res.status_code, 201)

    def test_create_user(self):
        res = self.create_user(self.users[0])
        self.assertEqual(res.status_code, 201)

    def test_get_userTimingPreferences(self):
        res = self.create_userTimingPreferences(self.users[0])
        res = self.client.get(self.userTimingPreferences_url +
                              str(res.data['id']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['day_start_time'],
                         self.users[0]['timing_preferences']['day_start_time'])
        self.assertEqual(res.data['day_end_time'],
                         self.users[0]['timing_preferences']['day_end_time'])
        self.assertEqual(res.data['time_zone'],
                         self.users[0]['timing_preferences']['time_zone'])

    def test_get_user(self):
        res = self.create_user(self.users[0])
        res = self.client.get(self.user_url +
                              str(res.data['id']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], self.users[0]['username'])

    def test_update_userTimingPreferences(self):
        res = self.create_userTimingPreferences(self.users[0])
        payload = {
            'day_start_time': '09:00',
            'day_end_time': '17:00',
            'time_zone': 'Europe/London'
        }
        res = self.client.put(self.userTimingPreferences_url +
                              str(res.data['id']), payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['time_zone'], payload['time_zone'])

    def test_update_user(self):
        res = self.create_user(self.users[0])
        payload = {
            "username": "user3",
            "password": self.users[0]['password'],
            'timing_preferences': res.data['timing_preferences']
        }
        res = self.client.put(self.user_url + str(res.data['id']), payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], payload['username'])

    def test_delete_userTimingPreferences(self):
        res = self.create_userTimingPreferences(self.users[0])
        res = self.client.delete(self.userTimingPreferences_url +
                                 str(res.data['id']))
        self.assertEqual(res.status_code, 204)

    def test_delete_user(self):
        res = self.create_user(self.users[0])
        res = self.client.delete(self.user_url + str(res.data['id']))
        self.assertEqual(res.status_code, 204)

    def test_get_user_list(self):
        for user in self.users:
            self.create_user(user)
        res = self.client.get(self.user_url)
        for i in range(len(res.data)):
            self.assertEqual(self.users[i]['username'],
                             res.data[i]['username'])

    def test_suggested_time(self):
        body = {}
        for user in self.users:
            res = self.create_user(user)
            body[str(res.data['id'])] = user['cal_info']
        suggested_time = '/api/v1/suggested-time/?users=1,2' \
                         '&duration_mins=60&count=3'
        res = self.client.post(suggested_time, body, format='json')
        print(res.data)
        self.assertEqual(res.status_code, 200)
        for i in range(0, 3):
            self.assertEqual(self.slots[i]['start'],
                             res.data['slots'][i]['start'])
            self.assertEqual(self.slots[i]['end'],
                             res.data['slots'][i]['end'])
