from http import HTTPStatus

from db.db import aio_redis
from schemas.user import UserModel


class CRUDUser:

    @staticmethod
    async def upinsert_address_by_phone(obj_in: UserModel) -> int:
        await aio_redis.hset('user', obj_in.phone_number, obj_in.address)
        return HTTPStatus.OK

    @staticmethod
    async def get_address_by_phone(phone: str) -> UserModel | dict:
        user_info = await aio_redis.hget('user', phone)
        if user_info:
            user_obj = {'phone_number': phone, 'address': user_info}
            return UserModel.parse_obj(user_obj)
        else:
            return {'status': HTTPStatus.EXPECTATION_FAILED,
                    'description': 'Такого номера телефона нет в базе'}


crud_user = CRUDUser()
