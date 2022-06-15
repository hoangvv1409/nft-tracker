from fastapi import APIRouter, Request, Depends
from src.utils import to_posix
from src.utils.dict_ultility import to_dict
from ..dependencies import resolve_dependencies, Dependencies

router = APIRouter(
    prefix='/v1/collections', tags=['Collections'])


@router.get('')
async def get(
    request: Request, page: int = 1, page_size: int = 50,
    q: str = None, sort_by: str = None,
    deps: Dependencies = Depends(resolve_dependencies)
):
    collections = []
    count, total_page, records = \
        deps.collection_repository.get_sorted_collections(
            page=page,
            page_size=page_size,
            query=q,
            sort_by=sort_by,
        )

    for r in records:
        # TODO: Use mapper to resolve model from orm,
        # put all posix date to model prop
        collection = to_dict(r[0])
        stats = to_dict(r[1])
        del collection['id']
        del collection['provider_payload']
        del stats['id']

        stats['updated_date_posix'] = to_posix(stats['updated_date'])
        collection['created_date_posix'] = to_posix(collection['created_date'])

        collections.append({
            **collection,
            'stats': stats,
        })

    response = {
        'total': count,
        'page': page,
        'page_size': page_size,
        'total_page': total_page,
        'items': collections,
    }

    return {**response}
