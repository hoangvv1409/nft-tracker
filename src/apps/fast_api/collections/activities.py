from fastapi import APIRouter, Request, Depends
from src.utils.dict_ultility import to_dict
from ..dependencies import resolve_dependencies, Dependencies

router = APIRouter(
    prefix='/v1/collections', tags=['Collections'])


@router.get('/{address}/activities')
async def get(
    request: Request, address: str,
    page: int = 1, page_size: int = 50,
    deps: Dependencies = Depends(resolve_dependencies)
):
    txns = []
    count, total_page, records = \
        deps.collection_transaction_repository.get_sorted_transactions(
            contract_address=address,
            page=page,
            page_size=page_size,
        )

    for r in records:
        txn = to_dict(r)
        del txn['id']
        del txn['provider_payload']

        txns.append({**txn})

    response = {
        'total': count,
        'page': page,
        'page_size': page_size,
        'total_page': total_page,
        'items': txns,
    }

    return {**response}
