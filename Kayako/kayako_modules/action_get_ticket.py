from typing import Annotated

from pydantic.v1 import BaseModel, Field

from .base_action import KayakoAction
from . import KayakoModule


class KayakoGetTicketArguments(BaseModel):
    ticketid: Annotated[str, Field(description="The unique numerical ticket ID or the mask ticket ID")]

class KayakoGetTicket(KayakoAction):
    name = "Get a Ticket by ID"
    description = "Returns ticket data for the given ticket ID"
    module: KayakoModule

    def run(self, arguments: KayakoGetTicketArguments) -> dict | None:
        

        response = self.get_json(
            params={"e": "/Tickets/Ticket/" + arguments.ticketid}
        )

        return response['tickets']['ticket'] if response else {}