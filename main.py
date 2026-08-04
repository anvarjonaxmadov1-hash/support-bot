import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, ADMIN_IDS
import database as db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@dp.message(CommandStart())
async def cmd_start(message: Message):
    if is_admin(message.from_user.id):
        await message.answer(
            "👋 Salom! Bu — support (yordam) bot.\n\n"
            "Mijozlar shu botga yozganda, ularning xabari sizga shu yerda ko'rinadi. "
            "Javob berish uchun mijozning xabariga <b>Reply</b> qilib yozing — javobingiz avtomatik mijozga yetkaziladi."
        )
    else:
        await message.answer(
            "👋 Salom! Savolingiz yoki muammoingiz bo'lsa, shu yerga yozib qoldiring — "
            "tez orada javob beramiz."
        )


@dp.message(F.chat.type == "private")
async def relay_message(message: Message):
    user_id = message.from_user.id

    if is_admin(user_id):
        if message.reply_to_message:
            target_user_id = await db.get_user_for_reply(message.chat.id, message.reply_to_message.message_id)
            if target_user_id:
                try:
                    await bot.copy_message(
                        chat_id=target_user_id,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id,
                    )
                    await message.reply("✅ Mijozga yuborildi.")
                except Exception as e:
                    await message.reply(f"⚠️ Yuborib bo'lmadi: {e}")
            else:
                await message.reply("⚠️ Bu xabar mijozga bog'lanmagan — to'g'ridan-to'g'ri mijozning xabariga Reply qiling.")
        return

    username = message.from_user.username or "-"
    full_name = message.from_user.full_name or "-"
    info_text = f"👤 <b>{full_name}</b> (@{username})\n🆔 ID: <code>{user_id}</code>"

    for admin_id in ADMIN_IDS:
        try:
            info_msg = await bot.send_message(admin_id, info_text)
            forwarded_msg = await bot.forward_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            await db.save_mapping(admin_id, info_msg.message_id, user_id)
            await db.save_mapping(admin_id, forwarded_msg.message_id, user_id)
        except Exception as e:
            logging.error(f"Adminga yuborishda xatolik: {e}")

    await message.answer("✅ Xabaringiz qabul qilindi, tez orada javob beramiz.")


async def main():
    await db.init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
