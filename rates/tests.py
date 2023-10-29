from urllib.parse import quote

from rest_framework import status
from rest_framework.test import APITestCase

from rates.models import Rate


class RateTests(APITestCase):
    def setUp(self):
        pass

    def test_get_rates(self):
        rate = Rate.objects.create(
            days="mon,tues,wed", times="0900-1700", tz="America/Chicago", price=1500
        )

        response = self.client.get("/rates/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["days"], rate.days)
        self.assertEqual(response.data[0]["times"], rate.times)
        self.assertEqual(response.data[0]["tz"], rate.tz)
        self.assertEqual(response.data[0]["price"], rate.price)

    def test_get_multiple_rates(self):
        rate_1 = Rate.objects.create(
            days="mon,tues,wed", times="0900-1700", tz="America/Chicago", price=1500
        )
        rate_2 = Rate.objects.create(
            days="sat,sun", times="0600-1400", tz="America/Chicago", price=2400
        )

        response = self.client.get("/rates/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["days"], rate_1.days)
        self.assertEqual(response.data[0]["times"], rate_1.times)
        self.assertEqual(response.data[0]["tz"], rate_1.tz)
        self.assertEqual(response.data[0]["price"], rate_1.price)
        self.assertEqual(response.data[1]["days"], rate_2.days)
        self.assertEqual(response.data[1]["times"], rate_2.times)
        self.assertEqual(response.data[1]["tz"], rate_2.tz)
        self.assertEqual(response.data[1]["price"], rate_2.price)

    def test_put_rates(self):
        Rate.objects.create(
            days="mon,tues,wed", times="0900-1700", tz="America/Chicago", price=1500
        )
        Rate.objects.create(
            days="sat,sun", times="0600-1400", tz="America/Chicago", price=2400
        )

        put_rate = {
            "days": "mon,tues,wed",
            "times": "0900-1700",
            "tz": "America/Chicago",
            "price": 1500,
        }
        response = self.client.put("/rates/", data=[put_rate], format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)

        self.assertEqual(response_json[0]["days"], put_rate["days"])
        self.assertEqual(response_json[0]["times"], put_rate["times"])
        self.assertEqual(response_json[0]["tz"], put_rate["tz"])
        self.assertEqual(response_json[0]["price"], put_rate["price"])

    def test_post_rates_not_allowed(self):
        response = self.client.post("/rates/")

        self.assertEqual(response.status_code, 405)

    def test_patch_rates_not_allowed(self):
        response = self.client.patch("/rates/")

        self.assertEqual(response.status_code, 405)

    def test_delete_rates_not_allowed(self):
        response = self.client.delete("/rates/")

        self.assertEqual(response.status_code, 405)


class PriceTests(APITestCase):
    fixtures = ["rates_fixture"]

    def test_get_price_requires_query_parameters(self):
        response = self.client.get("/price/", format="json")

        self.assertEqual(
            "Query parameters, 'start' and 'end' are required to be specified as ISO-8601 strings.",
            response.json(),
        )

    def test_get_price_sample_result_1(self):
        start = quote("2015-07-01T07:00:00-05:00")
        end = quote("2015-07-01T12:00:00-05:00")

        response = self.client.get("/price/", QUERY_STRING=f"start={start}&end={end}")

        self.assertEqual(1750, response.json()["price"])

    def test_get_price_sample_result_2(self):
        start = quote("2015-07-04T15:00:00+00:00")
        end = quote("2015-07-04T20:00:00+00:00")

        response = self.client.get("/price/", QUERY_STRING=f"start={start}&end={end}")

        self.assertEqual(2000, response.json()["price"])

    def test_get_price_sample_result_3(self):
        start = quote("2015-07-04T07:00:00+05:00")
        end = quote("2015-07-04T20:00:00+05:00")

        response = self.client.get("/price/", QUERY_STRING=f"start={start}&end={end}")

        self.assertEqual("unavailable", response.json()["price"])

    def test_get_price_validate_query(self):
        start = quote("2015-07-04T20:00:00+05:00")
        end = quote("2015-07-04T07:00:00+05:00")

        response = self.client.get("/price/", QUERY_STRING=f"start={start}&end={end}")

        self.assertEqual(
            "Query parameters, 'start' must be before 'end'.", response.json()
        )

    def test_post_price_not_allowed(self):
        response = self.client.post("/price/")

        self.assertEqual(response.status_code, 405)

    def test_patch_price_not_allowed(self):
        response = self.client.patch("/price/")

        self.assertEqual(response.status_code, 405)

    def test_put_price_not_allowed(self):
        response = self.client.put("/price/")

        self.assertEqual(response.status_code, 405)

    def test_delete_price_not_allowed(self):
        response = self.client.delete("/price/")

        self.assertEqual(response.status_code, 405)
