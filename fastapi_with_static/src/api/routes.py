from fastapi import APIRouter

from src.services.report_service import report_service

route = APIRouter(
    prefix="/report",
    tags=["Report"],
)


@route.get("")
async def get_report(
        address: str,
):
    """
    Endpoint to get the report.
    :param address: Email address in string format
    :return: list[tuple[str, str]]
    """
    return await report_service.get_report(address)
