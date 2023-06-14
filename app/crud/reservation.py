from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, between, and_

from app.crud.base import CRUDBase
from app.models import Reservation, User


class CRUDReservation(CRUDBase):
    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: int | None = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        # select_stmt = select(Reservation).where(
        #     Reservation.meetingroom_id == meetingroom_id,
        #     or_(
        #         between(
        #             from_reserve,
        #             Reservation.from_reserve,
        #             Reservation.to_reserve
        #         ),
        #         between(
        #             to_reserve,
        #             Reservation.from_reserve,
        #             Reservation.to_reserve
        #         ),
        #         and_(
        #             from_reserve <= Reservation.from_reserve,
        #             to_reserve >= Reservation.to_reserve
        #         )
        #     )
        # )
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
        self,
        meetingroom_id: int,
        session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                Reservation.to_reserve >= datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Reservation]:
        user_reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return user_reservations.scalars().all()


reservation_crud = CRUDReservation(Reservation)
