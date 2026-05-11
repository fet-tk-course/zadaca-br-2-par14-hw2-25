from fastapi import APIRouter
from seat_type_routes import router as seat_type_router
from hall_type_routes import router as hall_type_router
from hall_routes import router as hall_router
from seat_routes import router as seat_router

router = APIRouter()

router.include_router(seat_type_router)
router.include_router(hall_type_router)
router.include_router(hall_router)
router.include_router(seat_router)