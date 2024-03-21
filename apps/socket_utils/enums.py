from enum import Enum



class NotificationTypeEnum(Enum):
    NEW_SOLCOT  = 'NEW_SOLCOT'
    NEW_MESSAGE = 'NEW_MESSAGE'

    @classmethod
    def choices(cls):
        # Return a list of tuples: [(enum_member.value, enum_member.value) for enum_member in cls]
        return [(key.value, key.value) for key in cls]