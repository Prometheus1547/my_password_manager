from enum import Enum

# because the api for this bot is too shitty and I have
# to divide string to get value
DELIMITER = '#####'

class GENERATE(Enum):
    ASK_HOW = 'need name service or now'
    SERVICE = 'name of this service'


class SAVING(Enum):
    ASK_HOW = 'need name service or now'
    SERVICE = 'name of this service'
    PASSWORD = 'save the password'

class FIND(Enum):
    FIND = 'find a password'
    UPDATE = 'FINDupdate password'+DELIMITER
    DELETE = 'FINDdelete password'+DELIMITER

class UPDATE(Enum):
    SERVICE = 'enter service name'
    UPDATE = 'update password'

class DELETE(Enum):
    DELETE = 'delete password'


class SHOW_ALL(Enum):
    INIT = 'init working with list'
    GET = 'get a password' + DELIMITER
    UPDATE = 'update a password' + DELIMITER
    DELETE = 'delete a password' + DELIMITER
