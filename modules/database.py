from pony.orm import Database, PrimaryKey, Required

db = Database("sqlite", "../data.db", create_db=True)


class Chat(db.Entity):
    chatId = PrimaryKey(int, sql_type='BIGINT', size=64)
    wantsAlert = Required(bool, default=False)


class Data(db.Entity):
    id = PrimaryKey(int)
    mrbeast = Required(int, default=0)
    tseries = Required(int, default=0)

    @property
    def diff(self) -> int:
        return self.mrbeast - self.tseries


db.generate_mapping(create_tables=True)
