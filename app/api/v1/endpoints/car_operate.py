from fastapi import APIRouter

from app.api.v1.dependencies import AdminDep
from app.api.v1.get_services import CarServiceDep
from app.common.api_response import ApiResponse
from app.schemas.car_dto.car_add import CarAddRequestDto
from app.schemas.car_dto.car_delete import CarDeleteRequestDto
from app.schemas.car_dto.car_execute import CarDropRequestDto, CarRideRequestDto
from app.schemas.car_dto.car_query import CarQueryRequestDto
from app.schemas.car_dto.car_update import CarUpdateRequestDto

router = APIRouter(prefix="/car", tags=["车辆操作"])


@router.post("/add")
async def car_add(add_data: CarAddRequestDto, service: CarServiceDep, admin: AdminDep):
    service.car_add(add_data)
    return ApiResponse.success(message="新增成功")


@router.delete("/delete")
async def car_delete(
    data: CarDeleteRequestDto, service: CarServiceDep, admin: AdminDep
):
    service.car_delete(data)
    return ApiResponse.success(message="删除成功")


@router.post("/query")
async def query(data: CarQueryRequestDto, service: CarServiceDep):
    return ApiResponse.success(data=service.car_page_info(data))


@router.post("/update")
async def car_update(
    data: CarUpdateRequestDto, service: CarServiceDep, admin: AdminDep
):
    result = service.car_update(data)
    return ApiResponse.success(data=result)


@router.post("/ride")
async def ride(data: CarRideRequestDto, service: CarServiceDep):
    service.ride(data)
    return ApiResponse.success()


@router.post("/drop")
async def drop(data: CarDropRequestDto, service: CarServiceDep):
    service.drop(data)
    return ApiResponse.success()
