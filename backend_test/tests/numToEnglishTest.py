from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from backend_test.models.numToEnglish import NumToEnglish
from backend_test.models.payload import Payload


class NumToEnglishTest(TestCase):
    def setUp(self):
        import django
        django.setup()

    def test_num_to_english_units(self):
        num_to_english_proccessor = NumToEnglish("1")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "one")

    def test_tens(self):
        num_to_english_proccessor = NumToEnglish("12")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "twelve")

        num_to_english_proccessor = NumToEnglish("53")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "fifty three")

    def test_hundredths(self):
        num_to_english_proccessor = NumToEnglish("954")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "nine hundredth fifty four")

    def test_thousands(self):
        num_to_english_proccessor = NumToEnglish("1000")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "one thousand")

        num_to_english_proccessor = NumToEnglish("1257")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "one thousand two hundredth fifty seven")

    def test_boundary_case(self):
        num_to_english_proccessor = NumToEnglish("1235257")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "one million two hundredth thirty five thousand two hundredth fifty seven")

        num_to_english_proccessor = NumToEnglish("320001235257")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english,
                         "three hundredth twenty billion one million two hundredth thirty five thousand two hundredth fifty seven")

        num_to_english_proccessor = NumToEnglish("-1257")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "minus one thousand two hundredth fifty seven")

        num_to_english_proccessor = NumToEnglish(f"{pow(10, 35)}")
        msg_status, num_in_english = num_to_english_proccessor.process()
        self.assertEqual(num_in_english, "one hundredth decillion")


class NumToEnglishAPITest(APITestCase):
    def setUp(self):
        import django
        django.setup()
        self.client.login(username='backend_test', password='LM5CtcBkAYj93df5')

    def test_get_num_to_english_but_sending_bad_data(self):
        response = self.client.get('/num_to_english')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get('/num_to_english?number="not_number"')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get('/num_to_english?number=12.2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        big_number = pow(10, 37)
        response = self.client.get(f'/num_to_english?number={big_number}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_num_to_english(self):
        # GET /num_to_english?number=12345678
        response = self.client.get('/num_to_english?number=12345678')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ok",
                                         "num_in_english": "twelve million three hundredth forty five thousand six hundredth seventy eight"})

    def test_post_num_to_english(self):
        # POST /num_to_english
        # data: {"number":12345678}
        data = {"number": 12345678}
        response = self.client.post('/num_to_english', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ok",
                                         "num_in_english": "twelve million three hundredth forty five thousand six hundredth seventy eight"})
