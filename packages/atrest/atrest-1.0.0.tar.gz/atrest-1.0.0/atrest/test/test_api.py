import os
import unittest
import requests

from atrest.client import Client

AT_BASE_URL = os.getenv("AT_BASE_URL")
AT_INTEGRATION_CODE = os.getenv("AT_INTEGRATION_CODE")
AT_USERNAME = os.getenv("AT_USERNAME")
AT_SECRET = os.getenv("AT_SECRET")

TEST_QUEUE_ID = 29683487


class TestClientInitialization(unittest.TestCase):
    def testSuccessfulClientInitialization(self):
        client = Client("test", "test", "test", "test")
        self.assertIsInstance(client, Client)


class TestWithBadSecrets(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(
            AT_BASE_URL,
            AT_INTEGRATION_CODE,
            AT_USERNAME,
            AT_SECRET,
        )

    def testSuccessfulTicketSubmission(self):
        self.assertIsInstance(self.client, Client)
        ticket_id = self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)
        self.assertIsInstance(ticket_id, int)

    def testMalformedHeader(self):
        self.client.api.headers["ApiIntegrationCode"] = 111111111
        with self.assertRaisesRegex(
            requests.exceptions.InvalidHeader, "Header is improperly formatted."
        ):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)

    def testInvalidBaseUrl(self):
        self.client.api.base_url = "test"
        with self.assertRaisesRegex(
            requests.exceptions.MissingSchema, "Missing / Invalid Autotask URL."
        ):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)

    def testMalformedAutotaskUrl(self):
        self.client.api.base_url = (
            "https://webservices15.autotask.net/atservicesrest/v1.05"
        )
        with self.assertRaisesRegex(requests.exceptions.HTTPError, "Bad Autotask URL"):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)

    def testInvalidIntegrationCode(self):
        self.client.api.headers["ApiIntegrationCode"] = "11111111111111"
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "Invalid Autotask integration code"
        ):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)

    def testInvalidUsername(self):
        self.client.api.headers["UserName"] = "fakeemail@strivehealth.com"
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "Invalid Autotask credentials."
        ):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)

    def testInvalidSecret(self):
        self.client.api.headers["Secret"] = "reallyFakePassword"
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "Invalid Autotask credentials."
        ):
            self.client.create_ticket("test", "test", 1, 1, 0, TEST_QUEUE_ID)


class TestCreateTicket(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(
            AT_BASE_URL,
            AT_INTEGRATION_CODE,
            AT_USERNAME,
            AT_SECRET,
        )

    def testBadStatus(self):
        BAD_STATUS = 1111111111111
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "bad query parameters"
        ):
            ticket_id = self.client.create_ticket(
                "test", "test", BAD_STATUS, 1, 0, TEST_QUEUE_ID
            )

    def testBadPriority(self):
        BAD_PRIORITY = 1111111111111
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "bad query parameters"
        ):
            ticket_id = self.client.create_ticket(
                "test", "test", 1, BAD_PRIORITY, 0, TEST_QUEUE_ID
            )

    def testBadCompanyId(self):
        BAD_COMPANY_ID = 1111111111111
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "bad query parameters"
        ):
            ticket_id = self.client.create_ticket(
                "test", "test", 1, 1, BAD_COMPANY_ID, TEST_QUEUE_ID
            )

    def testBadQueueId(self):
        BAD_QUEUE_ID = 1111111111111
        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "bad query parameters"
        ):
            ticket_id = self.client.create_ticket("test", "test", 1, 1, 0, BAD_QUEUE_ID)


class TestQueryTickets(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(
            AT_BASE_URL,
            AT_INTEGRATION_CODE,
            AT_USERNAME,
            AT_SECRET,
        )

    def testGoodQuery(self):
        resp = self.client.query_tickets("9877")
        self.assertIsNotNone(resp)
        self.assertIsInstance(resp, requests.Response)

    def testBadQuery(self):
        with self.assertRaisesRegex(ValueError, "You must enter a ticket id"):
            self.client.query_tickets("")
