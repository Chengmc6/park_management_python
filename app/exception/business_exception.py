from app.common.result_code import ResultCode


class BusinessException(Exception):
    def __init__(self, code: int | ResultCode, message: str | None = None):
        if isinstance(code, ResultCode):
            self.code = code.code
            self.message = message if message else code.message
        else:
            self.code = code
            self.message = message if message else "UNKNOWN ERROR"
        super().__init__(self.message)
