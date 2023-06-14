from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
    ReservationDB
)
from app.crud.reservation import reservation_crud
from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_intersections,
    check_reservation_before_edit,
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User


router = APIRouter()


@router.get(
    '/my-reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    reservations = await reservation_crud.get_by_user(
        user=user, session=session
    )
    return reservations


@router.post(
    '/',
    response_model=ReservationDB,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    await check_meeting_room_exists(
        reservation.meetingroom_id, session
    )
    await check_reservation_intersections(
        **reservation.dict(), session=session,
    )
    new_reservation = await reservation_crud.create(
        reservation, session, user
    )
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    db_reservations = await reservation_crud.get_multi(session)
    return db_reservations


@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB,
)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """For author or superuser only"""
    db_reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=db_reservation.meetingroom_id,
        session=session
    )
    db_reservation = await reservation_crud.update(
        db_obj=db_reservation,
        obj_in=obj_in,
        session=session,
    )
    return db_reservation


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """For author or superuser only"""
    db_reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    db_reservation = await reservation_crud.remove(
        db_reservation, session
    )
    return db_reservation
