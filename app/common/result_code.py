from enum import Enum


class ResultCode(Enum):
    SUCCESS = (200, "success")
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    VALIDATION_ERROR = (422, "VALIDATION_ERROR")
    SERVER_ERROR = (500, "Server Error")
    USERNAME_EXISTS = (1001, "ユーザーは既に存在しています")
    PASSWORD_ERROR = (1002, "パスワードは間違いました")
    CONFIRM_PASSWORD_ERROR = (1007, "confirmPassword is wrong")
    USER_NOT_FOUND = (1003, "ユーザーは存在しません")
    PASSWORD_SAME = (1004, "新しいパスワードと古いパスワードは同じではないでください")
    ILLEGAL_PERMISSION = (1005, "権限不足")
    NOT_AVAILABLE = (1006, "車輌使用不可")
    LOGIN_FAILED = (1008, "Login Failed")
    CAR_ALREADY_IN_USE = (1009, "車輌使用中です")

    UNKNOWN_ERROR = (5900, "未知错误")

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]

    @classmethod
    def get_by_code(cls, code: int) -> "ResultCode":
        for item in cls:
            if item.code == code:
                return item
        return cls.UNKNOWN_ERROR
