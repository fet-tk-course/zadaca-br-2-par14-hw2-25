from fastapi import APIRouter

from seat_type_routes import router as seat_type_router

router = APIRouter()

router.include_router(seat_type_router)