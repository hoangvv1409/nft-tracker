from fastapi import APIRouter, Request, Depends
from src.utils.dict_ultility import to_dict
from ..dependencies import resolve_dependencies, Dependencies

router = APIRouter(
    prefix='/v1/collections', tags=['Collections'])


@router.get('/{address}/tokens')
async def get(
    request: Request, address: str,
    page: int = 1, page_size: int = 50,
    q: str = None, sort_by: str = None,
    deps: Dependencies = Depends(resolve_dependencies)
):
    tokens = []
    count, total_page, records = \
        deps.token_repository.get_sorted_tokens(
            contract_address=address,
            page=page,
            page_size=page_size,
        )

    for t in records:
        token = to_dict(t)
        del token['id']
        del token['provider_payload']

        tokens.append({**token})

    response = {
        'total': count,
        'page': page,
        'page_size': page_size,
        'total_page': total_page,
        'items': tokens,
    }

    return {**response}
