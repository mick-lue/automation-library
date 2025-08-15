from typing import Annotated

from pydantic.v1 import BaseModel, Field

from .base_action import KayakoAction
from . import KayakoModule


class KayakoUpdateTicketArguments(BaseModel):
    ticketid: Annotated[str, Field(description="The unique numerical ticket ID or the mask ticket ID", exclude=True)]
    subject: Annotated[str | None, Field(description="The ticket subject")] = None
    fullname: Annotated[str | None, Field(description="Full name of creator")] = None
    email: Annotated[str | None, Field(description="Email address of creator")] = None
    departmentid: Annotated[str | None, Field(description="The ID of the main department for this ticket")] = None
    ticketstatusid: Annotated[str | None, Field(description="Ticket status ID")] = None
    ticketpriorityid: Annotated[str | None, Field(description="Ticket priority ID")] = None
    tickettypeid: Annotated[str | None, Field(description="Ticket type ID")] = None
    ownerstaffid: Annotated[str | None, Field(description="Owner Staff ID, if you want to set an owner for this ticket")] = None

class KayakoUpdateTicket(KayakoAction):
    name = "Update a Ticket by ID"
    description = "Updates the ticket with the given ID using the values provided and returns the updated ticket."
    module: KayakoModule

    def run(self, arguments: KayakoUpdateTicketArguments) -> dict | None:
        
        response = self.post_json(
            params={"e": "/Tickets/Ticket/" + arguments.ticketid},
            data=arguments.dict(exclude_none=True)
        )

        return response['tickets']['ticket'] if response else {}