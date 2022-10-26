from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext

from keyboards.default import kb_faq
from states import StateProblem
from loader import dp, bot


@dp.message_handler(commands=['faq'])
@dp.message_handler(text=['FAQ'])
@dp.message_handler(commands=['faq'], state=StateProblem.all_states)
async def bot_faq(message: types.Message, state: FSMContext):
    # f = await bot.get_chat_members_count(chat_id=-832474250)
    # a = await bot.get_chat_member(chat_id=-832474250, user_id=message.chat.id)
    # print(a.status)
    # print(type(a))
    await state.finish()
    await message.answer("Полные инструкции находятся на "
                         "http://confluence.fisgroup.ru:8080/pages/viewpage.action?pageId=109121428\n"
                         "Что вас интересует?", reply_markup=kb_faq)


@dp.message_handler(text='Изолированная/Обычная среда')
async def bot_faq_isonorm(message: types.Message):
    await message.answer("<b>Обычная</b> - внешняя ссылка(http://demo.fisgroup.ru:180XX/web). "
                         "Доступ предоставляется по IP или VPN. Возможен доступ из нашей инфраструктуры "
                         "по доп. портам (включая SSH).\n<b>Изолированная</b> - внешняя ссылка"
                         "(http://demo.fisgroup.ru:190ХХ/web). Доступ открыт всем по ссылке,"
                         " SSH и дополнительные порты исключены. Высокий риск потери стенда, риск для "
                         "инфраструктуры минимален.")


@dp.message_handler(text='Для презентации/Доступа/Разработки')
async def bot_faq_type(message: types.Message):
    await message.answer("<b>для презентации</b> – когда запрашивают стенд только на несколько часов для показа "
                         "презентации клиенту\n<b>для доступа</b> – когда запрашивают для открытия доступа клиенту "
                         "для самостоятельного изучения\n<b>для доработок</b> – когда нужен стенд для модификации "
                         "существующего шаблона или создания нового на основе имеющегося/копии с разработческого")


@dp.message_handler(text='Доступ к SSH')
async def bot_faq_ssh(message: types.Message):
    await message.answer("Порт TCP 22 (SSH) никому наружу не даём, даже на изолированных стендах.\n"
                         "Для стендов demoXX.fisgroup.ru из нашей сети доступ к SSH уже открыт\n"
                         "Стандартные логин/пароль для SSH - login/password\n"
                         "Если нужен доступ к SSH, нужно указывать это при заказе стенда.\n"
                         "Если доступ понадобился после организации стенда - создать новую заявку.\n"
                         "Для стендов на http://demo.fisgroup.ru:180XX/web Ссылка для ssh подключения, "
                         "если оно запрашивалось, будет в решении задачи. Инструкция по подключению:")
    await message.reply_document(open("files/ssh-ds1.docx", "rb"))


@dp.message_handler(text='Доступ к СП')
async def bot_faq_as(message: types.Message):
    await message.answer("Если нужен доступ к админке сервера приложений, нужно указывать это при заказе стенда.\n"
                         "Если доступ понадобился после организации стенда - создать новую заявку.\n"
                         "Для стендов на http://demo.fisgroup.ru:180XX/web сылка для доступа к админке сервера "
                         "приложений, если он запрашивался, будет в решении задачи и "
                         "имеет вид http://demo.fisgroup.ru:48XXX/web/\n"
                         "Для стендов demoXX.fisgroup.ru из нашей сети доступ к СП уже открыт по ссылке "
                         "https://demoXX.fisgroup.ru:4848/\n"
                         "Для входа обычно установлены login/password . Если не подходят - нужно смотреть "
                         "описание шаблона")


@dp.message_handler(text='Клиент не может войти на стенд')
async def bot_faq_access_client(message: types.Message):
    await message.answer("Если предостевлена ссылка вида http://demoXX.fisgroup.ru:8080/web/ попробуйте войти "
                         "не указывая порт, те http://demo18.fisgroup.ru/web/\n"
                         "Если предоставлялся доступ по ip - проверьте внешний ip, например на ресурсе https://2ip.ru/")


@dp.message_handler(text='Не открывается http://demo.fisgroup.ru:180XX/web у сотрудника')
async def bot_faq_access_emplyee(message: types.Message):
    await message.answer("Если через VPN заходите, пропишите маршрут в командной строке:\n"
                         "Если тип VPN L2TP: route add -p 142.132.222.190 mask 255.255.255.255 10.10.113.1\n"
                         "Если тип VPN PPTP: route add /P 142.132.222.190 mask 255.255.255.255 10.10.112.1\n"
                         "Если сервер подключения vpn2.fisgroup.ru(тип VPN не важен): "
                         "route add /P 142.132.222.190 mask 255.255.255.255 10.10.111.1\n"
                         "У кого OpenVPN никаких маршрутов добавлять не нужно\n"
                         "на macos для l2tp через bash: sudo route -n add -net 142.132.222.190 10.10.113.1")


@dp.message_handler(text='Ошибка JDBCException: Cannot open connection')
async def bot_faq_jdbc_error(message: types.Message):
    await message.answer("Войти в админку сервера приложений. В разделе Resources - JDBC - JDBC Connection Pools "
                         "спинговать схемы. У проблемной схемы помогает изменение параметров "
                         "Maximum Pool Size, Max Wait Time")
    await bot.send_photo(chat_id=message.chat.id, photo=InputFile("files/image_gf.png"))


@dp.message_handler(text='Доступ клиенту по VPN')
async def bot_faq_vpn_client(message: types.Message):
    await message.answer("Клиент должен быть занесен в таблицу учета клиентов: "
                         "http://confluence.fisgroup.ru:8080/pages/viewpage.action?pageId=44007496\n"
                         "Клиента заносят менеджеры перед постановкой задачи на предоставления доступа\n"
                         "В рамках задачи администраторы создают клиенту VPN профиль и предоставляют "
                         "логин и пароль(ключи)\n"
                         "Инструкция по настройке VPN:")
    await message.reply_document(open("files/VPN.docx", "rb"))