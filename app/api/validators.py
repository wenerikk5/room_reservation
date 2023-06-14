from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> int | None:
    room_id = await meeting_room_crud.get_room_id_by_name(
        room_name, session
    )

    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )
    return room_id


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    meeting_room = await meeting_room_crud.get(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room


async def check_reservation_intersections(
    **kwargs,
) -> None:
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )
    return


async def check_reservation_before_edit(
    reservation_id: int,
    session: AsyncSession,
):
    db_reservation = await reservation_crud.get(
        obj_id=reservation_id, session=session
    )
    if not db_reservation:
        raise HTTPException(
            status_code=422,
            detail='Бронь не найдена!'
        )
    return db_reservation
