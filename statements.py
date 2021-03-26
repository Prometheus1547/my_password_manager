from enum import Enum


class GENERATE(Enum):
    ASK_HOW = 'need name service or now'
    SERVICE = 'name of this service'


class SAVING(Enum):
    ASK_HOW = 'need name service or now'
    SERVICE = 'name of this service'
    PASSWORD = 'save the password'