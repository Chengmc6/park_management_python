from sqlmodel import Session, col, desc, func, select

from app.common.page_result import PageResult
from app.models.car import Car
from app.models.car_usage import CarUsage
from app.models.user import User
from app.schemas.usage_dto.usage_request import UsageRequestDto
from app.schemas.usage_dto.usage_response import UsageResponseVo


class UsageService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def history(self, data: UsageRequestDto):

        stmt = (
            select(CarUsage, User, Car)
            .join(User, col(CarUsage.user_id) == col(User.id))
            .join(Car, col(CarUsage.car_id) == col(Car.id))
            .where(CarUsage.car_id == data.car_id)
            .order_by(desc(CarUsage.ride_time))
        )

        # 更高效的 Count 写法
        total = self.db.exec(
            select(func.count()).where(CarUsage.car_id == data.car_id)
        ).one()

        offset = (data.page_num - 1) * data.page_size

        total_pages = (total + data.page_size - 1) // data.page_size

        results = self.db.exec(stmt.offset(offset).limit(data.page_size)).all()

        show_data: list[UsageResponseVo] = []

        for usage, user, car in results:
            drop_alcohol = 0
            if usage.drop_alcohol_level:
                drop_alcohol = usage.drop_alcohol_level
            usage_vo = UsageResponseVo(
                car_number=car.car_number,
                username=user.username,
                ride_time=usage.ride_time,
                ride_alcohol_level=usage.ride_alcohol_level,
                drop_time=usage.drop_time,
                drop_alcohol_level=drop_alcohol,
            )
            show_data.append(usage_vo)

        return PageResult(
            total=total,
            page_num=data.page_num,
            page_size=data.page_size,
            total_pages=total_pages,
            records=show_data,
        )
