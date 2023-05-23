from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard(type: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    match type:
        case 'after_login_actions':
            keyboard.row_width = 1
            account_info = InlineKeyboardButton(text="Информация о счёте", callback_data='binance_account')
            orders = InlineKeyboardButton(text='Информация об ордерах', callback_data='binance_orders')
            keyboard.add(account_info, orders)
        case 'login_register':
            # keyboard.row_width = 2
            enter = InlineKeyboardButton(text="Вход", callback_data='login')
            register = InlineKeyboardButton(text='Регистрация', callback_data='register')
            keyboard.add(enter, register)
        case 'get_confirmation':
            # keyboard.row_width = 2
            confirm = InlineKeyboardButton(text="Подтвердить", callback_data='register_confirm')
            cancel = InlineKeyboardButton(text='Отмена', callback_data='register_cancel')
            keyboard.add(confirm, cancel)
        case 'register_only':
            keyboard.row_width = 1
            register = InlineKeyboardButton(text='Регистрация', callback_data='register')
            keyboard.add(register)
        case _:
            pass
    return keyboard