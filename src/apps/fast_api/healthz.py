from fastapi import APIRouter, Request


router = APIRouter(prefix='/v1/healthz', tags=['HealthCheck'])


@router.get('')
async def get(request: Request):
    return {'message': 'OK'}
