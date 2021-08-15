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
                    'day_start_time': '09:00:00',
                    'day_end_time': '17:00:00',
                    'time_zone': 'Asia/Calcutta'
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
                    'day_start_time': '10:00:00',
                    'day_end_time': '18:00:00',
                    'time_zone': 'Asia/Calcutta'
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
                "start": "2022-06-04T11:00:00+05:30",
                "end": "2022-06-04T12:00:00+05:30"
            },
            {
                "start": "2022-06-04T14:00:00+05:30",
                "end": "2022-06-04T15:00:00+05:30"
            },
            {
                "start": "2022-06-04T15:00:00+05:30",
                "end": "2022-06-04T16:00:00+05:30"
            }
        ]

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestAPI(TestSetUp):
    def test_suggested_time(self):
        body = {}
        for user in self.users:
            res = self.client.post(self.userTimingPreferences_url,
                                   user['timing_preferences'])
            self.assertEqual(res.status_code, 201)
            payload = {
                "username": user['username'],
                "password": user['password'],
                'timing_preferences': res.data['id']
            }
            res = self.client.post(self.user_url, payload)
            self.assertEqual(res.status_code, 201)
            body[str(res.data['id'])] = user['cal_info']
        suggested_time = '/api/v1/suggested-time/?users=1,2' \
                         '&duration_mins=60&count=3'
        res = self.client.post(suggested_time, body, format='json')
        self.assertEqual(res.status_code, 200)
        for i in range(0, 3):
            self.assertEqual(self.slots[i]['start'],
                             res.data['slots'][i]['start'])
            self.assertEqual(self.slots[i]['end'],
                             res.data['slots'][i]['end'])
        res = self.client.get(self.user_url+"1")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], self.users[0]['username'])
        res = self.client.get(self.userTimingPreferences_url +
                              str(res.data['timing_preferences']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['day_start_time'],
                         self.users[0]['timing_preferences']['day_start_time'])
        self.assertEqual(res.data['day_end_time'],
                         self.users[0]['timing_preferences']['day_end_time'])
        self.assertEqual(res.data['time_zone'],
                         self.users[0]['timing_preferences']['time_zone'])
        payload = {
            "username": "user3",
            "password": self.users[0]['password'],
            'timing_preferences': res.data['id']
        }
        res = self.client.put(self.user_url + "1", payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], payload['username'])
        payload = {
            'day_start_time': '09:00',
            'day_end_time': '17:00',
            'time_zone': 'Europe/London'
        }
        res = self.client.put(self.userTimingPreferences_url +
                              str(res.data['timing_preferences']), payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['time_zone'], payload['time_zone'])
        res = self.client.delete(self.user_url+'1')
        self.assertEqual(res.status_code, 204)
        res = self.client.delete(self.userTimingPreferences_url + '1')
        self.assertEqual(res.status_code, 204)
