from pony.orm import Database, Required

db = Database("sqlite", "../bitchlasagnabot.db", create_db=True)


class Chat(db.Entity):
    chatId = Required(int)
    isGroup = Required(bool)
    wantsAlert = Required(bool, default=False)


db.generate_mapping(create_tables=True)