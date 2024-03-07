from enum import Enum


class ProcessStateEnum(Enum):
    PENDING    = 'PENDIENTE'
    ACCEPTED   = 'ACEPTADO'
    REJECTED   = 'RECHAZADO'
    IN_PROCESS = 'RESTORE'
    FINISHED   = 'FINALIZADO'
    EXPIRED    = 'VENCIDA'
    CLOSED     = 'CERRADO'
    REVIEW     = 'REVISION'
    RETURNED   = 'DEVUELTA'
    
    @classmethod
    def choices(cls):
        # Return a list of tuples: [(enum_member.value, enum_member.value) for enum_member in cls]
        return [(key.value, key.value) for key in cls]