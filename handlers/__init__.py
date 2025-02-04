from aiogram import Router

from .add_holiday import router as add_holiday_router
from .all_holiday import router as all_holiday_router
from .register import router as register_router
from .start import router as start_router
from .this_month_holidays import router as this_month_holidays_router


def register_handlers(dp: Router):
    dp.include_router(add_holiday_router)
    dp.include_router(all_holiday_router)
    dp.include_router(register_router)
    dp.include_router(start_router)
    dp.include_router(this_month_holidays_router)
