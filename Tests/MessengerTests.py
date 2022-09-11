#  Copyright (c) 2022-2022 Etienne Clairis
# #

from fbchat import Client
from fbchat.models import *

client = Client("etienne.clairis@gmail.com", "S1licium14")

print("Own id: {}".format(client.uid))

client.send(Message(text="Hi me!"), thread_id=client.uid, thread_type=ThreadType.USER)

client.logout()
