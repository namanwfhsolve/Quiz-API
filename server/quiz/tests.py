from django.test import TestCase
from django.utils import timezone as tz

from rest_framework.test import APIClient

import json
from datetime import timedelta, datetime
from time import sleep

from quiz.models import Quiz


def get_quiz_data():
    with open("assets/quiz.json", "r") as fp:
        data = json.load(fp)
    return data


# Create your tests here.
class BaseTestCase(TestCase):
    api_client = APIClient()


class QuizTest(BaseTestCase):
    def _to_datetime(self, data):
        return tz.localtime(datetime.fromisoformat(data))

    def _post_quiz(self, data):
        res = self.api_client.post(
            "/quiz/quiz/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        return res.json()

    def _get_quiz_list(self, *filters):
        res = self.api_client.get(
            f"/quiz/quizes/?{'&'.join([''.join(f) for f in filters])}"
        )
        self.assertEqual(res.status_code, 200)
        return res.json()

    def test_quiz_create(self):
        data = get_quiz_data()
        res = self._post_quiz(data)

        self.assertEqual(res["name"], data["name"])
        self.assertTrue(Quiz.objects.filter(id=res["id"]).exists())

    def test_quiz_list(self):
        data = get_quiz_data()

        # post quiz for past
        data["live_since"] = (tz.localtime() + timedelta(seconds=1)).isoformat()
        data["available_till"] = (tz.localtime() + timedelta(seconds=5)).isoformat()
        self._post_quiz(data)

        # sleep for 1 sec
        sleep(1)

        # post quiz for later
        data["live_since"] = (tz.localtime() + timedelta(days=10)).isoformat()
        data["available_till"] = (tz.localtime() + timedelta(days=15)).isoformat()
        self._post_quiz(data)

        # fetch going on quizes
        # i.e. whose live since time is less than now
        res = self._get_quiz_list(("live_since__lte", tz.localtime().isoformat()))

        print(res)
        for i in res:
            print(i["live_since"], i["available_till"])
            self.assertLessEqual(self._to_datetime(i["live_since"]), tz.localtime())
            self.assertLessEqual(self._to_datetime(i["available_till"]), tz.localtime())
