import json
import requests


class API:
    def __init__(self, at_base_url, at_integration_code, at_username, at_secret):
        self.base_url = at_base_url
        self.headers = {
            "ApiIntegrationCode": at_integration_code,
            "UserName": at_username,
            "Secret": at_secret,
            "Content-Type": "application/json",
        }

    def __exception_parser(self, e):
        if isinstance(e, requests.exceptions.InvalidHeader):
            return requests.exceptions.InvalidHeader(
                "Header is improperly formatted. Ensure values are strings."
            )
        if isinstance(e, requests.exceptions.MissingSchema):
            return requests.exceptions.MissingSchema("Missing / Invalid Autotask URL.")

        if isinstance(e, requests.exceptions.HTTPError) and "404 Client Error" in repr(
            e
        ):
            return requests.exceptions.HTTPError(f"Bad Autotask URL: {e}")
        if isinstance(e, requests.exceptions.HTTPError) and "Unauthorized" in repr(e):
            return requests.exceptions.HTTPError("Invalid Autotask credentials.")
        if isinstance(
            e, requests.exceptions.HTTPError
        ) and "Internal Server Error" in repr(e):
            return requests.exceptions.HTTPError(
                f"Invalid Autotask integration code OR bad query parameters."
            )

    def query_tickets(self, ticket_id):
        if not ticket_id:
            raise ValueError("You must enter a ticket id.")
        try:
            qs = f'/Tickets/query?search={{"filter":[{{"op":"eq","field":"Id","value":"{ticket_id}"}}]}}'
            resp = requests.get(self.base_url + qs, headers=self.headers)
            resp.raise_for_status()
            return resp
        except Exception as e:
            raise self.__exception_parser(e) from None

    def create_ticket(self, title, description, status, priority, company_id, queue_id):
        data = {
            "Title": title,
            "Description": description,
            "Status": status,
            "Priority": priority,
            "CompanyID": company_id,
            "QueueID": queue_id,
        }

        payload = json.dumps(data)
        try:
            resp = requests.post(
                self.base_url + "/Tickets", headers=self.headers, data=payload
            )
            resp.raise_for_status()
            ticket_id = resp.json()["itemId"]
            return ticket_id
        except Exception as e:
            raise self.__exception_parser(e) from None
