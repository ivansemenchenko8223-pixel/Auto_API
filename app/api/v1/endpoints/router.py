from app.api.v1.endpoints import auth, detal, order
from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(detal.router)
router.include_router(order.router) 
