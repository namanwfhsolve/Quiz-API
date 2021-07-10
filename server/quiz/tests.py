from django.test import TestCase
from django.utils import timezone as tz

from rest_framework.test import APIClient

import json
from datetime import timedelta, datetime

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
        """returns isoformated time"""
        return tz.localtime(datetime.fromisoformat(data))

    def _post_quiz(self, data):
        """post quiz with given data"""
        res = self.api_client.post(
            "/quiz/quiz/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        return res.json()

    def _upcoming_filter(self, now=tz.localtime()):
        """
        return the upcoming filter fo get list api

        - time since should be before now
        - available till should be after now
        """
        return [
            ("live_since__lte", now.strftime("%Y-%m-%dT%H:%M:%S")),
            ("available_till__gte", now.strftime("%Y-%m-%dT%H:%M:%S")),
        ]

    def _get_quiz_list(self, *filters):
        """
        - get quizes from list api
        - filters:
            - takes a tuple of key, values pairs
        """
        res = self.api_client.get(
            f"/quiz/quizes/?{'&'.join(['='.join(f) for f in filters])}"
        )
        self.assertEqual(res.status_code, 200)
        return res.json()

    def _validate_quized_res(self, res, reference=tz.localtime()):
        """
        validate the quiz list response against referenced time

        - check if reference is after live since
        - check if available till is after reference
        """
        for i in res:
            self.assertGreaterEqual(reference, self._to_datetime(i["live_since"]))
            self.assertGreaterEqual(self._to_datetime(i["available_till"]), reference)

    def test_quiz_create(self):
        data = get_quiz_data()
        res = self._post_quiz(data)

        self.assertEqual(res["name"], data["name"])
        self.assertTrue(Quiz.objects.filter(id=res["id"]).exists())

    def test_quiz_list(self):
        data = get_quiz_data()

        # post quiz for after 1 hour now up to 5 hours
        data["live_since"] = (
            tz.localtime() + timedelta(hours=1, minutes=10)
        ).isoformat()
        data["available_till"] = (
            tz.localtime() + timedelta(hours=5, minutes=15)
        ).isoformat()
        self._post_quiz(data)

        # print(self._get_quiz_list())

        def validate_after(hours=0):
            # print("> hour", hours)
            # considering now as n hour after
            now = tz.localtime() + timedelta(hours=hours)
            # print(self._upcoming_filter(now))
            res = self._get_quiz_list(*self._upcoming_filter(now))

            # print("validate for", now, res)
            self._validate_quized_res(res, now)

        validate_after()
        validate_after(1)
        validate_after(2)
        validate_after(3)
        validate_after(4)
        validate_after(5)
        validate_after(6)
