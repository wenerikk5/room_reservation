from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MeetingRoom
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomUpdate, MeetingRoomDB
)
from app.crud.base import CRUDBase


class CRUDMeetingRoom(CRUDBase):

    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> int | None:
        db_room_id = await session.execute(
            select(self.model.id).where(self.model.name == room_name)
        )
        return db_room_id.scalars().first()


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)

# async def create_meeting_room(
#     new_room: MeetingRoomCreate,
#     session: AsyncSession,
# ) -> MeetingRoom:
#     new_room_data = new_room.dict()
#     db_room = MeetingRoom(**new_room_data)
#     session.add(db_room)
#     await session.commit()
#     await session.refresh(db_room)
#     return db_room


# async def get_room_id_by_name(
#     room_name: str,
#     session: AsyncSession,
# ) -> int | None:
#     db_room_id = await session.execute(
#         select(MeetingRoom.id).where(MeetingRoom.name == room_name)
#     )
#     return db_room_id.scalars().first()


# async def get_meeting_room_by_id(
#     room_id: int,
#     session: AsyncSession,
# ) -> MeetingRoom | None:
#     db_room = await session.get(MeetingRoom, room_id)
#     return db_room


# async def read_all_rooms_from_db(
#     session: AsyncSession,
# ) -> list[MeetingRoom]:
#     db_rooms = await session.execute(
#         select(MeetingRoom)
#     )
#     return db_rooms.scalars().all()


# async def update_meeting_room(
#     db_room: MeetingRoom,
#     room_in: MeetingRoomUpdate,
#     session: AsyncSession,
# ) -> MeetingRoom:
#     obj_data = jsonable_encoder(db_room)

#     update_data = room_in.dict(exclude_unset=True)

#     for field in obj_data:
#         if field in update_data:
#             setattr(db_room, field, update_data[field])

#     session.add(db_room)
#     await session.commit()
#     await session.refresh(db_room)
#     return db_room


# async def delete_meeting_room(
#     db_room: MeetingRoom,
#     session: AsyncSession,
# ) -> None:
#     await session.delete(db_room)
#     await session.commit()
#     return db_room
