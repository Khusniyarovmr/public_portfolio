import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message, CallbackQuery

from services.buttons import get_keyboard
from src.core.config import app_settings
from src.services.auth.telegram_auth import get_user_by_chat_id, registration_from_telegram

bot = AsyncTeleBot(app_settings.TELEGRAM_TOKEN)


class MyStates(StatesGroup):
    username = State()
    email = State()
    pwd = State()


class IfRegistration:
    reg_check: str | None

    def set_reg_check_username(self):
        self.reg_check = 'username'

    def set_reg_check_email(self):
        self.reg_check = 'email'

    def set_reg_check_pwd(self):
        self.reg_check = 'pwd'

    def set_reg_check_none(self):
        self.reg_check = None


is_registration = IfRegistration()


class PreviousMessageId:
    id: int

    def set_message_id(self, msg_id: int):
        self.id = msg_id


prev_msg_id = PreviousMessageId()


async def _delete_prev_message(msg_id: int, chat_id: int) -> None:
    await bot.delete_message(chat_id, msg_id)


async def start_executor(message: Message) -> None:
    action = get_keyboard('login_register')
    msg = await bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=action)
    prev_msg_id.set_message_id(msg.id)


@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call: CallbackQuery) -> None:
    match call.data:
        case 'login':
            username = await _get_user_name_by_chat_id(call.from_user.id)
            if username:
                await _delete_prev_message(prev_msg_id.id, call.message.chat.id)
                actions = get_keyboard('after_login_actions')
                msg = await bot.send_message(call.from_user.id, f"Привет, {username}!", reply_markup=actions)
                prev_msg_id.set_message_id(msg.id)
            else:
                await _delete_prev_message(prev_msg_id.id, call.message.chat.id)
                actions = get_keyboard('register_only')
                msg = await bot.send_message(call.from_user.id, f"Я не могу Вас узнать. Зарегистрируйтесь, пожалуйста!",
                                             reply_markup=actions)
                prev_msg_id.set_message_id(msg.id)
        case 'register':
            is_registration.set_reg_check_username()
            if await _get_user_name_by_chat_id(call.from_user.id) is None:
                await _delete_prev_message(prev_msg_id.id, call.message.chat.id)
                msg = await bot.send_message(call.from_user.id, 'Укажите username', protect_content=True)
                prev_msg_id.set_message_id(msg.id)
            else:
                await _delete_prev_message(prev_msg_id.id, call.message.chat.id)
                action = get_keyboard('login_register')
                msg = await bot.send_message(call.from_user.id, "Вы уже зарегистрированы!", reply_markup=action)
                prev_msg_id.set_message_id(msg.id)
        case 'register_confirm':
            await _registration(call.from_user.id, call.message.chat.id)
        case 'register_cancel':
            await bot.delete_state(call.from_user.id, call.message.chat.id)
            await _delete_prev_message(prev_msg_id.id, call.message.chat.id)
            action = get_keyboard('login_register')
            msg = await bot.send_message(call.from_user.id, "Добро пожаловать!", reply_markup=action)
            prev_msg_id.set_message_id(msg.id)
        case 'binance_account':
            print('binance_account_information')
            pass
        case 'binance_orders':
            print('binance_orders_information')
            pass
        case _:
            print(call.data)


async def _registration(user_id: int, chat_id: int) -> None:
    async with bot.retrieve_data(user_id, chat_id) as data:
        user_name = data['username']
        user_email = data['email']
        user_pwd = data['pwd']
        await registration_from_telegram(user_id, user_name, user_email, user_pwd)
    await _delete_prev_message(prev_msg_id.id, chat_id)
    actions = get_keyboard('after_login_actions')
    msg = await bot.send_message(user_id, f"Регистрация прошла успешно!", reply_markup=actions)
    prev_msg_id.set_message_id(msg.id)


async def _bot_message_handler(message: Message) -> None:
    if is_registration.reg_check:
        await _add_registry_information_into_state(message, msg_type=is_registration.reg_check)


async def _add_registry_information_into_state(message: Message, msg_type: str) -> None:
    if message and msg_type == 'username':
        await bot.set_state(message.from_user.id, MyStates.username, message.chat.id)
        await bot.add_data(message.from_user.id, message.chat.id, username=message.text)
        is_registration.set_reg_check_email()
        await _delete_prev_message(prev_msg_id.id, message.chat.id)
        msg = await bot.send_message(message.chat.id, f'Укажите {is_registration.reg_check}', protect_content=True)
        prev_msg_id.set_message_id(msg.id)
    elif message and msg_type == 'email':
        await bot.set_state(message.from_user.id, MyStates.email, message.chat.id)
        await bot.add_data(message.from_user.id, message.chat.id, email=message.text)
        is_registration.set_reg_check_pwd()
        await _delete_prev_message(prev_msg_id.id, message.chat.id)
        msg = await bot.send_message(message.chat.id, f'Укажите {is_registration.reg_check}', protect_content=True)
        prev_msg_id.set_message_id(msg.id)
    elif message and msg_type == 'pwd':
        await bot.set_state(message.from_user.id, MyStates.pwd, message.chat.id)
        await bot.add_data(message.from_user.id, message.chat.id, pwd=message.text)
        is_registration.set_reg_check_none()
        await _ready_for_answer(message)


async def _ready_for_answer(message: Message) -> None:
    action = get_keyboard('get_confirmation')
    await _delete_prev_message(prev_msg_id.id, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg_text = ("Подтвердите данные:\n<b>"
                    f"Name: {data['username']}\n"
                    f"Email: {data['email']}\n"
                    f"pwd: {data['pwd']}</b>")
        msg = await bot.send_message(message.chat.id, msg_text, parse_mode="html", protect_content=True,
                                     reply_markup=action)
        prev_msg_id.set_message_id(msg.id)


async def _get_user_name_by_chat_id(chat_id: int) -> str:
    user_name = await get_user_by_chat_id(chat_id)
    return user_name


bot.register_message_handler(start_executor, commands=['start'])
bot.register_message_handler(_bot_message_handler)
bot.add_custom_filter(StateFilter(bot))

asyncio.run(bot.polling(skip_pending=True))
