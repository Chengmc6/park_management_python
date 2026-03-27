from fastapi import APIRouter

from app.api.v1.get_services import UsageServiceDep
from app.common.api_response import ApiResponse
from app.schemas.usage_dto.usage_request import UsageRequestDto

router = APIRouter(prefix="/usage", tags=["使用履历"])


@router.post("/histpry")
def history(data: UsageRequestDto, service: UsageServiceDep):
    result = service.history(data)
    return ApiResponse.success(data=result)
