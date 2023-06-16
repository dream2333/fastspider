from msgspec import Struct, structs


class BaseItem(Struct, omit_defaults=True):
    def fingerprint(self):
        return "TODO"

    def asdict(self):
        return structs.asdict(self)

    def astuple(self):
        return structs.astuple(self)
