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
    


class SolcotTypeEnum(Enum):
    PRODUCT  = '01HRCMT4589A8V99ZYSFWCB0WZ'
    SERVICE  = '01HRCMT45870GGN0AKHX288R1G'
    MIXED    = '01HRCMT45862JRV5A1KV6QN90K'
    
    @classmethod
    def choices(cls):
        # Return a list of tuples: [(enum_member.value, enum_member.value) for enum_member in cls]
        return [(key.value, key.value) for key in cls]
    


class SolcotStructureEnum(Enum):
    BASE = ["product", "quantity", "measurementUnit", "budget", "limit_date", 
            "contract_manager", "specification", "description", "is_unique_provider",
            "is_visit_required", "sub_category", "files",]