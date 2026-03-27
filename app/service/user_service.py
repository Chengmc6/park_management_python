from sqlmodel import Session, select

from app.common.result_code import ResultCode
from app.core.security import create_access_token, get_password_hash, verify_password
from app.exception.business_exception import BusinessException
from app.models.user import User
from app.schemas.user_dto.password_change_dto import UserPasswordChangeDto
from app.schemas.user_dto.user_info_vo import UserInfoVo
from app.schemas.user_dto.user_login_request_dto import UserLoginRequestDto
from app.schemas.user_dto.user_login_response_vo import UserLoginResponseVo
from app.schemas.user_dto.user_register_dto import UserRegisterDto


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, login_data: UserLoginRequestDto) -> UserLoginResponseVo:

        if not login_data:
            raise BusinessException(ResultCode.BAD_REQUEST)

        user = self.db.exec(
            select(User)
            .where(User.username == login_data.username)
            .where(User.is_deleted == 0)
        ).first()

        if not user:
            raise BusinessException(ResultCode.USER_NOT_FOUND)

        if not verify_password(login_data.password, user.password):
            raise BusinessException(ResultCode.LOGIN_FAILED)

        token = create_access_token(
            subject=user.username, extra_data={"role": user.role}
        )

        response_data = UserLoginResponseVo(
            id=user.id, username=user.username, token=token
        )
        return response_data

    def register(self, register_data: UserRegisterDto):

        if not register_data:
            raise BusinessException(ResultCode.BAD_REQUEST)

        user = self.db.exec(
            select(User).where(User.username == register_data.username)
        ).first()

        if user:
            raise BusinessException(ResultCode.USERNAME_EXISTS)

        register_user = User(
            username=register_data.username,
            password=get_password_hash(register_data.password),
        )

        self.db.add(register_user)
        self.db.flush()
        return register_user

    def get_user_info(self, user_id: int) -> UserInfoVo:

        user = self.db.exec(
            select(User).where(User.id == user_id).where(User.is_deleted == 0)
        ).first()

        if not user:
            raise BusinessException(ResultCode.NOT_FOUND)

        return UserInfoVo.model_validate(user)

    def change_password(self, user_id: int, change_data: UserPasswordChangeDto):

        user = self.db.exec(
            select(User).where(User.id == user_id).where(User.is_deleted == 0)
        ).first()

        if not user:
            raise BusinessException(ResultCode.NOT_FOUND)

        if not change_data:
            raise BusinessException(ResultCode.BAD_REQUEST)

        if not verify_password(change_data.old_password, user.password):
            raise BusinessException(ResultCode.PASSWORD_ERROR)

        if verify_password(change_data.new_password, user.password):
            raise BusinessException(ResultCode.PASSWORD_SAME)

        user.password = get_password_hash(change_data.new_password)
        self.db.add(user)
        # db.commit()
