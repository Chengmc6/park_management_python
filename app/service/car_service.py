from sqlmodel import Session, col, func, select, update

from app.common.page_result import PageResult
from app.common.result_code import ResultCode
from app.exception.business_exception import BusinessException
from app.models.car import Car
from app.models.car_usage import CarUsage
from app.models.user import User
from app.schemas.car_dto.car_add import CarAddRequestDto
from app.schemas.car_dto.car_delete import CarDeleteRequestDto
from app.schemas.car_dto.car_execute import CarDropRequestDto, CarRideRequestDto
from app.schemas.car_dto.car_page import CarPageResponseVo
from app.schemas.car_dto.car_query import CarQueryRequestDto
from app.schemas.car_dto.car_update import CarUpdateRequestDto


class CarService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def car_add(self, add_data: CarAddRequestDto):
        car = Car(car_number=add_data.car_number)

        self.db.add(car)
        self.db.flush()

    def car_delete(self, delete_data: CarDeleteRequestDto):
        statement = (
            update(Car)
            .where(col(Car.id).in_(delete_data.ids))
            .where(col(Car.status) == 0)
            .values(is_deleted=1)
        )
        self.db.exec(statement)

    def car_page_info(self, query: CarQueryRequestDto):

        statement = select(Car).where(Car.is_deleted == 0)

        if query.car_number:
            statement = statement.where(
                col(Car.car_number).contains(query.car_number)
            ).order_by(Car.car_number)

        # 查询总条数
        # 使用 func.count() 提高性能
        total = self.db.exec(
            select(func.count()).select_from(statement.subquery())
        ).one()

        # 查询当前页数据
        offset = (query.page_num - 1) * query.page_size
        records = self.db.exec(statement.offset(offset).limit(query.page_size)).all()

        show_data = [CarPageResponseVo.model_validate(item) for item in records]

        # 总页数
        total_pages = (total + query.page_size - 1) // query.page_size
        return PageResult(
            total=total,
            page_num=query.page_num,
            page_size=query.page_size,
            total_pages=total_pages,
            records=show_data,
        )

    def car_update(self, data: CarUpdateRequestDto):

        car = self.db.exec(
            select(Car).where(Car.id == data.id).where(Car.is_deleted == 0)
        ).first()

        if not car:
            raise BusinessException(ResultCode.NOT_FOUND)

        if data.car_number:
            car.car_number = data.car_number

        self.db.add(car)
        self.db.flush()
        return car

    def ride(self, data: CarRideRequestDto):
        # 校验车辆状态
        car = self.db.exec(
            select(Car)
            .where(Car.id == data.car_id)
            .where(Car.is_deleted == 0)
            .where(Car.status == 0)
        ).first()

        if not car:
            raise BusinessException(ResultCode.NOT_FOUND)
        # 更新车辆状态
        statement = (
            update(Car)
            .where(
                (col(Car.id) == data.car_id)
                & (col(Car.status) == 0)
                & (col(Car.is_deleted == 0))
            )
            .values(current_user_id=self.current_user.id, status=1)
        )

        result = self.db.exec(statement)
        updated_count = result.rowcount

        if updated_count == 0:
            current_car = car = self.db.exec(
                select(Car)
                .where(Car.id == data.car_id)
                .where(Car.is_deleted == 0)
                .where(Car.status == 0)
            ).first()
            if not current_car:
                raise BusinessException(ResultCode.ILLEGAL_PERMISSION)
            raise BusinessException(ResultCode.BAD_REQUEST)

        if car.id is None:
            raise BusinessException(ResultCode.SERVER_ERROR)

        if self.current_user.id is None:
            raise BusinessException(ResultCode.SERVER_ERROR)
        # 记录用车记录
        usage = CarUsage(
            car_id=car.id,
            user_id=self.current_user.id,
            ride_time=data.ride_time,
            ride_alcohol_level=data.ride_alcohol_level,
        )
        self.db.add(usage)

        self.db.flush()

    def drop(self, data: CarDropRequestDto):

        car = self.db.exec(
            select(Car).where(Car.id == data.car_id).where(Car.is_deleted == 0)
        ).first()
        if not car:
            raise BusinessException(ResultCode.NOT_FOUND)

        if car.current_user_id != self.current_user.id:
            raise BusinessException(ResultCode.ILLEGAL_PERMISSION)
        # 更新车辆状态为空闲
        car.current_user_id = None
        car.status = 0
        self.db.add(car)
        # 更新用车记录
        usage = self.db.exec(
            select(CarUsage)
            .where(CarUsage.car_id == car.id)
            .where(CarUsage.user_id == self.current_user.id)
            .where(col(CarUsage.drop_time).is_(None))
            .order_by(col(CarUsage.ride_time).desc())
            .limit(1)
        ).first()
        if not usage:
            raise BusinessException(ResultCode.SERVER_ERROR)

        usage.drop_time = data.drop_time
        usage.drop_alcohol_level = data.drop_alcohol_level
        self.db.add(usage)

        self.db.flush()
