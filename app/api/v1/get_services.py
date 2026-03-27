from typing import Annotated

from fastapi import Depends

from app.api.v1.dependencies import DbDep, UserDep
from app.service.car_service import CarService
from app.service.usage_service import UsageService
from app.service.user_service import UserService


def get_user_service(db: DbDep) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_car_service(db: DbDep, user: UserDep) -> CarService:
    return CarService(db, user)


CarServiceDep = Annotated[CarService, Depends(get_car_service)]


def get_usage_service(db: DbDep) -> UsageService:
    return UsageService(db)


UsageServiceDep = Annotated[UsageService, Depends(get_usage_service)]
