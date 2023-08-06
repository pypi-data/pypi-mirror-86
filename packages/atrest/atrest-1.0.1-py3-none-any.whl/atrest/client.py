import requests
from atrest.api import API


class Client:
    def __init__(self, at_base_url, at_integration_code, at_username, at_secret):
        self.api = API(at_base_url, at_integration_code, at_username, at_secret)

    def query_tickets(self, ticket_id) -> requests.Response:
        """
        Query for a ticket by ticket id.
        Returns either the ticket information in json, or raises an exception.
        """
        return self.api.query_tickets(ticket_id)

    def create_ticket(
        self, title, description, status, priority, company_id, queue_id
    ) -> int:
        """
        Create a ticket.
        Returns either the ticket ID of the created ticket, or raises an exception.
        """
        return self.api.create_ticket(
            title, description, status, priority, company_id, queue_id
        )
