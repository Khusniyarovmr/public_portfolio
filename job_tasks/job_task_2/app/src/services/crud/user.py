from http import HTTPStatus

from core.handle_exceptions import SomeError
from db.db import aio_redis
from schemas.user import UserModel
from services.logger.logger import logger


class CRUDUser:

    @staticmethod
    async def create_user_by_phone(obj_in: UserModel) -> int:
        try:
            await aio_redis.hset('user', obj_in.phone_number, obj_in.address)
            return HTTPStatus.OK
        except SomeError:
            logger.warning(f'Problem with phone {obj_in.phone_number}')
            return HTTPStatus.EXPECTATION_FAILED

    @staticmethod
    async def update_address_by_phone(obj_in: UserModel) -> int:
        try:
            await aio_redis.hset('user', obj_in.phone_number, obj_in.address)
            return HTTPStatus.OK
        except SomeError:
            logger.warning(f'Problem with phone {obj_in.phone_number}')
            return HTTPStatus.EXPECTATION_FAILED

    @staticmethod
    async def get_address_by_phone(phone: str) -> UserModel | int:
        try:
            user_info = await aio_redis.hget('user', phone)
            user_obj = {'phone_number': phone, 'address': user_info}
            return UserModel.parse_obj(user_obj)
        except SomeError:
            logger.warning(f'Problem with phone {phone}')
            return HTTPStatus.EXPECTATION_FAILED


crud_user = CRUDUser()
