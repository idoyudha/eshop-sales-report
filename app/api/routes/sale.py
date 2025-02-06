from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Any

from app.api.deps import AsyncSessionDep
from app.models.sale import SalesPublic
from app.service.sale import get_sales_service, count_total_sales_service, generate_sales_report_xlsx_service
from app.api.middleware import requires_auth

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=SalesPublic)
@requires_auth()
async def read_sales(
    session: AsyncSessionDep, 
    skip: int = 0, 
    limit: int = 10
) -> Any:
    """
    Retrieve sales.
    """
    count = await count_total_sales_service(session=session)
    sales = await get_sales_service(session=session, offset=skip, limit=limit)
    return SalesPublic(
        code=HTTPStatus.OK,
        data=sales, 
        count=count,
        message="success get"
    )

@router.get("/xlsx-report")
@requires_auth()
async def generate_sales_report_xlsx(session: AsyncSessionDep) -> Any:
    """
    Generate sales report in xlsx format.
    """
    output = await generate_sales_report_xlsx_service(session=session)
    headers = {
        "Content-Disposition": f"attachment; filename=sales-report.xlsx",
    }
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return StreamingResponse(output, media_type=media_type, headers=headers)