from typing import Annotated

from pydantic.v1 import BaseModel, Field

from .base_action import KayakoAction
from . import KayakoModule


class KayakoAddPostArguments(BaseModel):
    ticketid: Annotated[str, Field(description="The unique numerical ticket ID or the mask ticket ID")]
    contents: Annotated[str, Field(description="Contents of the post")]
    userid: Annotated[str | None, Field(description="User ID")] = None
    staffid: Annotated[str | None, Field(description="Staff ID")] = None
    isprivate: Annotated[int, Field(description="Set to 1 to make the post hidden to customer. Applies only if post is created by staff.")] = 0

class KayakoAddPost(KayakoAction):
    name = "Add a Post to a Ticket"
    description = "Adds a post to an existing ticket with the provided data."
    module: KayakoModule

    def run(self, arguments: KayakoAddPostArguments) -> dict | None:
        
        response = self.post_json(
            params={"e": "/Tickets/TicketPost/"},
            data=arguments.dict(exclude_none=True)
        )

        return response['posts']['post'] if response else {}