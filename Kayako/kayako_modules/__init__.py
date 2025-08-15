from typing import Annotated
from pydantic.v1 import BaseModel, Field, AnyHttpUrl, SecretStr
from sekoia_automation.module import Module


class KayakoModuleConfiguration(BaseModel):
    kayako_url: Annotated[AnyHttpUrl, Field(description="The URL of the Kayako instance")]
    kayako_apikey: Annotated[SecretStr, Field(description="The API key with access to your instance")]
    kayako_secretkey: Annotated[SecretStr, Field(description="The secret key")]
    trust_any_cert: Annotated[bool, Field(description="Whether to trust any certificate presented at the URL of your instance. Defaults to false, validating the certificate")] = False

class KayakoModule(Module):
    configuration: KayakoModuleConfiguration
