from typing import Annotated

from pydantic.v1 import BaseModel, Field

from .base_action import KayakoAction
from . import KayakoModule


class KayakoCreateTicketArguments(BaseModel):
    subject: Annotated[str | None, Field(description="The ticket subject")] = None
    fullname: Annotated[str | None, Field(description="Full name of creator")] = None
    email: Annotated[str | None, Field(description="Email address of creator")] = None
    contents: Annotated[str | None, Field(description="Contents of the first ticket post")] = None
    departmentid: Annotated[str | None, Field(description="The ID of the main department for this ticket")] = None
    ticketstatusid: Annotated[str | None, Field(description="Ticket status ID")] = None
    ticketpriorityid: Annotated[str | None, Field(description="Ticket priority ID")] = None
    tickettypeid: Annotated[str | None, Field(description="Ticket type ID")] = None
    userid: Annotated[str | None, Field(description="User ID, if the ticket is to be created as a user")] = None
    staffid: Annotated[str | None, Field(description="Staff ID, if the ticket is to be created as a staff")] = None
    ownerstaffid: Annotated[str | None, Field(description="Owner Staff ID, if you want to set an owner for this ticket")] = None
    ignoreautoresponder: Annotated[int, Field(description="Set to 0 to enable auto-respond mail")] = 1
    autouserid: Annotated[int, Field(description="Set to 0 if the creator should differ from the user connected to the email")] = 1

class KayakoCreateTicket(KayakoAction):
    name = "Create a new Kayako Ticket"
    description = "Creates a new ticket in Kayako with the provided data and returns that ticket."
    module: KayakoModule

    def run(self, arguments: KayakoCreateTicketArguments) -> dict | None:
        
        response = self.post_json(
            params={"e": "/Tickets/Ticket/"},
            data=arguments.dict(exclude_none=True)
        )

        return response['tickets']['ticket'] if response else {}