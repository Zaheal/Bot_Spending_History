from datetime import datetime
import calendar

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from states import FSMSpending
from keyboards import create_spending_menu_kb
from lexicon import RU_LEXICON
from database import create_users_db, create_wallets_db, create_descriptions_db,\
                    add_user_in_db, add_wallet_in_db, add_description_in_db, update_wallet,\
                    check_user_in_db, check_wallet_in_db, check_description_in_db,\
                    show_lust_spending, show_month_spending, show_year_spending, show_day_spending


# Хэндлер отправляет сообщение на комманду /start
async def process_start_command(message: Message):
    await message.answer(RU_LEXICON['/start'])


# Хэндлер отправляет сообщение на команду /help
async def process_help_command(message: Message):
    await message.answer(RU_LEXICON['/help'])


# Реагирует на команду /create_user, создает таблицы users, wallets, descriptions
# И если нет юзера добавляет его в бд
async def process_create_user_command(message: Message):
    create_users_db()
    create_wallets_db()
    create_descriptions_db()
    tg_id = message.from_user.id
    if check_user_in_db(tg_id):
        await message.answer(RU_LEXICON['already_user'])
    else:
        add_user_in_db(tg_id)
        await message.answer(RU_LEXICON['created_user'])


# Реагирует на команду /create_spending, если нет кошелька добавляет его в бд
# Запускает машину состояний и ждет ответа вида "<int> <str>"
async def process_create_spending_command(message: Message, state: FSMContext):
    date = datetime.now()
    year = date.year
    tg_id = message.from_user.id
    if check_user_in_db(tg_id):
        if not check_wallet_in_db(tg_id):
            add_wallet_in_db(tg_id, year)
        await message.answer(RU_LEXICON['/create_spending'])
        await state.set_state(FSMSpending.waiting_spent.state)
    else:
        await message.answer(RU_LEXICON['not_user'])


# Обрабатывает сообщение вида "<int> <str>" и добавляет в бд данные
# обновляет данные в бд wallets и добавляет новую запись descriptions
async def add_spending(message: Message, state: FSMContext):
    if len(message.text.split(' ', 1)) != 2:
        await message.answer(text=RU_LEXICON['wrong_answer'])
        return
    tg_id = message.from_user.id
    date = datetime.now()
    year = date.year
    if check_user_in_db(tg_id) and check_wallet_in_db(tg_id):
        month = calendar.month_name[date.month].lower()
        day = date.day
        spent_money = int(message.text.split(' ', 1)[0])
        description = message.text.split(' ', 1)[1]

        update_wallet(tg_id, year, month, spent_money)
        add_description_in_db(tg_id, year, month, day, spent_money, description)
        await message.answer(RU_LEXICON['created_spending'])
    else:
        await message.answer(RU_LEXICON['not_user_or_wallet'])
    await state.finish()
            

# Реагирует на команду /spending_menu 
# создает inline клавиатуру выбора периода
async def process_spending_menu_command(message: Message):
    tg_id = message.from_user.id
    if check_user_in_db(tg_id) and check_wallet_in_db(tg_id) and check_description_in_db(tg_id):
        await message.answer('За какой период вы хотите посмотреть свои расходы?', reply_markup=create_spending_menu_kb())
    else:
        await message.answer(RU_LEXICON['not_user_or_wallet'])


# Реагирует на нажатие inline кнопок
async def process_period_press(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    year = datetime.now().year
    if callback.data.startswith('lust'):
        spending = show_lust_spending(tg_id, year) # присваивает переменной значение последней записи
        await callback.message.edit_text(text=f'Твоя последняя запись: {spending}р', reply_markup=create_spending_menu_kb())
        await callback.answer()
        # Просит ввести дату, за которую пользователь хочет посмотреть свои расходы
    elif callback.data.startswith('year'):
        await callback.message.edit_text(text=RU_LEXICON['chosen_year'], reply_markup=create_spending_menu_kb()) 
        await callback.answer()
    elif callback.data.startswith('month'):
        await callback.message.edit_text(text=RU_LEXICON['chosen_month'], reply_markup=create_spending_menu_kb()) 
        await callback.answer()
    elif callback.data.startswith('day'):
        await callback.message.edit_text(text=RU_LEXICON['chosen_day'], reply_markup=create_spending_menu_kb())
        await callback.answer()
    await state.set_state(FSMSpending.waiting_date.state) # Запуск FMS


# Хэндлер выводит запрошенную информацию в чат
async def process_total_show(message: Message, state: FSMContext):
    if not message.text.split('.')[0].isdigit() and message.text.split('.') > 3: # Сработает если данные не корректные
        await message.answer(text=RU_LEXICON['wrong_answer'])
        return
    answer = message.text.split('.')
    tg_id = message.from_user.id
    if len(answer) == 1: # Если пользователь указал только год
        spending = show_year_spending(tg_id, int(answer[0]))
        await message.answer(text=f'Total: {spending}р')
    elif len(answer) == 2: # Если пользователь ввел месяц и год, вывод количества записей и всего затраяенных денег
        year = int(answer[1])
        month = calendar.month_name[int(answer[0])].lower()
        spending = show_month_spending(tg_id, year, month)
        await message.answer(text=f'Сделано записей: {spending[0]}.\nВсего затрат за месяц: {spending[1]}р.')
    elif len(answer) == 3: # Если пользователь написал полную дату, вывод всех записей по одной
        year = int(answer[2])
        month = calendar.month_name[int(answer[1])].lower()
        day = int(answer[0])
        spending = show_day_spending(tg_id, year, month, day)
        if spending:
            string = ''
            for cost, desc in spending:
                string += str(cost) + ' ' + desc + '\n'
            await message.answer(text=f'Ваши записи:\n{string}')
        else:
            await message.answer(text='Нет записей за этот день.')
    else: # Что-то не сошлось
        await message.answer(text=RU_LEXICON['wrong_answer'])
    await state.finish()


# Регистрация хэндлеров
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))
    dp.register_message_handler(process_create_user_command, Command(commands=['create_user']))
    dp.register_message_handler(process_create_spending_command, Command(commands=['create_spending']))
    dp.register_message_handler(add_spending, state=FSMSpending.waiting_spent)
    dp.register_message_handler(process_spending_menu_command, Command(commands=['spending_menu']))
    dp.register_callback_query_handler(process_period_press, Text(endswith='period'))
    dp.register_message_handler(process_total_show, state=FSMSpending.waiting_date)