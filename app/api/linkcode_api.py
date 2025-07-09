from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
)

from core import settings
from service.bussines_services.link_code import LinkCodeService
from schemas.linkcode import LinkCodeResponse

from api.dependencies import get_session


router = APIRouter(
    prefix=settings.api.linkcode.prefix,
    tags=settings.api.linkcode.tags,
)


@router.get("", status_code=status.HTTP_200_OK, response_model=LinkCodeResponse)
async def get_linkcode(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    """Получить собственный код привязки"""
    link_code_service = LinkCodeService(session=session)
    linkcode = await link_code_service.get_link_code_by_user_id(user_id=request.state.user_id)

    return LinkCodeResponse(linkcode=linkcode.code)
