from pony.orm import Database, Required, PrimaryKey

db = Database("sqlite", "../bitchlasagnabot.db", create_db=True)


class Chat(db.Entity):
    chatId = Required(str, unique=True)
    isGroup = Required(bool)
    wantsAlert = Required(bool, default=False)


class Data(db.Entity):
    id = PrimaryKey(int, default=0)
    pewdiepie = Required(int, default=0)
    tseries = Required(int, default=0)
    difference = Required(int, default=0)


db.generate_mapping(create_tables=True)