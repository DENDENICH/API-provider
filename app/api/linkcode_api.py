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
<<<<<<< HEAD
    try:
        link_code_service = LinkCodeService(session=session)
        linkcode = await link_code_service.get_link_code_by_user_id(user_id=request.state.user_id)

    except NotFoundError as e:
        logger.info(
            msg="Linkcode is not found by user id -> \n{}".format(request.state.user_id)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except BadRequestError as e:
        logger.info(
            msg="Bad request\n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.error(
            msg="Error \n{}".format(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
=======
    link_code_service = LinkCodeService(session=session)
    linkcode = await link_code_service.get_link_code_by_user_id(user_id=request.state.user_id)
>>>>>>> exception-working

    return LinkCodeResponse(linkcode=linkcode.code)
