from enum import IntEnum, Enum, auto

class FollowStatus(IntEnum):
    FOLLOW_TO = 1
    FOLLOW_FROM = 2
    FOLLOW_BOTH = 3

class BookCategoryEnum(Enum):
    TECH = auto()
    #经管
    MANAGE = auto()
    POEM = auto()
    #科幻小说
    S_NOVEL = auto()
    #言情小说
    L_NOVEL = auto()
    #推理小说
    D_NOVEL = auto()
    #经典小说
    C_NOVEL = auto()
    #网络小说
    I_NOVEL = auto()
    #文学
    LITERATURE = auto()
    CULTURE = auto()

class LikeStatus(IntEnum):
    LIKE = 1
    NOLIKE = 0