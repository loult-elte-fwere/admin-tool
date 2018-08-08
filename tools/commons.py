from gi.repository import Gtk

class UserList:
    """Wrapper around the 'currently connected users' dictionary"""

    def __init__(self, userlist_data):
        # liststore has 3 celles : pokemon, adj and userid
        self.list_store = Gtk.ListStore(str, str, str)
        self.parse_userlist(userlist_data)

    def parse_userlist(self, userlist_data):
        self.list_store.clear()
        for user_data in userlist_data:
            params = user_data["params"]
            self.list_store.append([params["name"], params["adjective"], user_data["userid"]])

    def del_user(self, user_id):
        for row in self.list_store:
            if row[2] == user_id:
                self.list_store.remove(row.iter)

    def add_user(self, user_id, params):
        self.list_store.append([params["name"], params["adjective"], user_id])

    def __str__(self):
        return "Connected users :\n" \
               "%s" % "\n".join(["\t - %s %s" % (row[0], row[1) for row in self.list_store])


class AbstractResponse:
    pass


class Message(AbstractResponse):

    def __init__(self, msg: str):
        self.msg = msg

    def to_dict(self):
        return {"lang": "fr", "msg": self.msg, "type": "msg"}


class BotMessage(AbstractResponse):

    def __init__(self, msg: str):
        self.msg = msg

    def to_dict(self):
        return {"type": "bot", "msg": self.msg}


class Sound(AbstractResponse):

    def __init__(self, sound_filepath: str):
        self.filepath = sound_filepath

    def get_bytes(self):
        with open(self.filepath, "rb") as soundfile:
            return soundfile.read()


class AttackCommand(AbstractResponse):

    def __init__(self, target_name: str, offset=1):
        self.target = target_name
        self.offset = offset

    def to_dict(self):
        return {"target": self.target, "order": self.offset, "type": "attack"}

class Sleep(AbstractResponse):

    def __init__(self, duration : int):
        self.duration = duration