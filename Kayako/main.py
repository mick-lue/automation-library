from kayako_modules import KayakoModule

from kayako_modules.action_create_ticket import KayakoCreateTicket
from kayako_modules.action_add_post import KayakoAddPost
from kayako_modules.action_update_ticket import KayakoUpdateTicket
from kayako_modules.action_get_ticket import KayakoGetTicket


if __name__ == "__main__":
    module = KayakoModule()
    module.register(KayakoCreateTicket, "KayakoCreateTicket")
    module.register(KayakoAddPost, "KayakoAddPost")
    module.register(KayakoUpdateTicket, "KayakoUpdateTicket")
    module.register(KayakoGetTicket, "KayakoGetTicket")
    module.run()
