"""UI strings for English, Russian, and Uzbek.

Keys and {placeholders} are identical across languages. Amazon's menu path is
kept in English on purpose — it's a navigation path users match literally.
HTML formatting (parse_mode=HTML) is used throughout.
"""
from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ──────────────────────────── English ────────────────────────────────────
    "en": {
        "welcome": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "Send me any supported document and I'll forward it to your Kindle.\n\n"
            "<b>One-time setup:</b>\n"
            "1. /myemail — get my sender address\n"
            "2. Add it to your <b>Amazon Approved Personal Document E-mail List</b>\n"
            "   (amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings)\n"
            "3. /setkindle your_name@kindle.com — save your Kindle address\n\n"
            "Then just send a file! Use /help for details and limits.\n\n"
            "🌐 Change language: /language"
        ),
        "help": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "<b>SETUP (one-time):</b>\n"
            "1. /myemail to get my sender address\n"
            "2. amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings → Approved Personal Document E-mail List → add it\n"
            "3. /setkindle your_name@kindle.com to save your Kindle email\n\n"
            "<b>SENDING:</b>\nJust send any supported file to this chat!\n\n"
            "✅ <b>Supported:</b>\n{formats}\n\n"
            "⚠️ <b>Limits:</b>\n"
            "• Max file size: {max_mb} MB (Telegram Bot API limit)\n"
            "• Amazon's own cap is 50 MB — larger files need special setup\n"
            "• EPUB requires a Kindle with 2022+ firmware\n"
            "• Your sender email MUST be whitelisted in Amazon settings or\n"
            "  documents will silently not arrive\n"
            "• Amazon provides 5 GB free storage; old docs may be removed\n\n"
            "<b>Commands:</b>\n"
            "/setkindle &lt;email&gt; — save your Kindle address\n"
            "/myemail — show the address to whitelist at Amazon\n"
            "/status — your settings &amp; send count\n"
            "/convert — toggle Amazon auto-conversion\n"
            "/language — change language\n"
            "/help — this message"
        ),
        "btn_send": "✅ Send",
        "btn_cancel": "❌ Cancel",
        "language_choose": "🌐 Choose your language:",
        "language_set": "✅ Language set to <b>English</b>.",
        "setkindle_usage": (
            "Usage: <code>/setkindle your_name@kindle.com</code>\n\n"
            "Find your Kindle address at amazon.com → Manage Your Content and "
            "Devices → Devices → (your Kindle)."
        ),
        "setkindle_invalid": (
            "That doesn't look like a Kindle address. It should end with "
            "<b>@kindle.com</b>, e.g. <code>your_name@kindle.com</code>."
        ),
        "setkindle_saved": (
            "✅ Saved! I'll send your documents to <code>{email}</code>.\n\n"
            "⚠️ Make sure <code>{sender}</code> is on your Amazon Approved Personal "
            "Document E-mail List, or delivery will silently fail."
        ),
        "myemail": (
            "📧 My sender address is:\n<code>{sender}</code>\n\n"
            "<b>Add it</b> to your Amazon Approved Personal Document E-mail List:\n"
            "amazon.com →  <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences → "
            "Personal Document Settings.\n\n"
            "Without this, Amazon silently drops everything I send."
        ),
        "status": (
            "<b>Your settings</b>\n"
            "Kindle email: <code>{kindle}</code>\n"
            "Documents sent: <b>{count}</b>\n"
            "Auto-convert: <b>{convert}</b>\n"
            "Language: <b>{lang}</b>"
        ),
        "status_no_kindle": "— (use /setkindle)",
        "state_on": "on",
        "state_off": "off",
        "convert_on": (
            "Auto-conversion is now <b>ON</b>.\n"
            'The email subject is set to "Convert" so Amazon converts formats '
            "like DOCX to Kindle format."
        ),
        "convert_off": "Auto-conversion is now <b>OFF</b>.",
        "unsupported": "❌ Unsupported file type <b>{ext}</b>.{hint}\n\n✅ I accept: {formats}",
        "unsupported_hint": " Amazon doesn't accept {ext} files.",
        "too_large": (
            "❌ That file is too large. My limit is {max_mb} MB "
            "(Telegram Bot API download cap)."
        ),
        "no_kindle": (
            "You haven't set your Kindle email yet.\n"
            "Use <code>/setkindle your_name@kindle.com</code> first."
        ),
        "rate_limited": (
            "⏳ Daily limit reached ({limit} documents/day). Try again tomorrow."
        ),
        "confirm_prompt": "Send <b>{filename}</b> to <code>{email}</code>?",
        "sending": "Sending…",
        "sent_ok": (
            "✅ Sent <b>{filename}</b> to <code>{email}</code>.\n\n"
            "If it doesn't arrive, confirm <code>{sender}</code> is whitelisted at Amazon."
        ),
        "cancelled": "❌ Cancelled. Nothing was sent.",
        "cancelled_answer": "Cancelled.",
        "expired": "This request expired — please resend the file.",
        "send_error": "❌ Something went wrong while sending. Please try again later.",
        "set_kindle_first": "Set your Kindle email first with /setkindle.",
        "setkindle_prompt": (
            "📧 Send me your Kindle email address.\n"
            "It looks like <code>your_name@kindle.com</code>.\n\n"
            "Send /cancel to abort."
        ),
        "action_cancelled": "✅ Cancelled.",
        "cancel_nothing": "Nothing to cancel.",
    },
    # ──────────────────────────── Russian ────────────────────────────────────
    "ru": {
        "welcome": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "Отправьте мне любой поддерживаемый документ — я перешлю его на ваш Kindle.\n\n"
            "<b>Разовая настройка:</b>\n"
            "1. /myemail — узнать мой адрес отправителя\n"
            "2. Добавьте его в <b>Amazon Approved Personal Document E-mail List</b>\n"
            "   (amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings)\n"
            "3. /setkindle your_name@kindle.com — сохранить ваш адрес Kindle\n\n"
            "После этого просто пришлите файл! Подробности и лимиты — /help.\n\n"
            "🌐 Сменить язык: /language"
        ),
        "help": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "<b>НАСТРОЙКА (один раз):</b>\n"
            "1. /myemail — узнать мой адрес отправителя\n"
            "2. amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings → Approved Personal Document E-mail List → добавьте его\n"
            "3. /setkindle your_name@kindle.com — сохранить ваш адрес Kindle\n\n"
            "<b>ОТПРАВКА:</b>\nПросто пришлите любой поддерживаемый файл в этот чат!\n\n"
            "✅ <b>Поддерживается:</b>\n{formats}\n\n"
            "⚠️ <b>Ограничения:</b>\n"
            "• Максимальный размер файла: {max_mb} МБ (лимит Telegram Bot API)\n"
            "• Собственный лимит Amazon — 50 МБ; для файлов больше нужна особая настройка\n"
            "• EPUB требует Kindle с прошивкой 2022 года и новее\n"
            "• Ваш адрес отправителя ОБЯЗАТЕЛЬНО должен быть в белом списке Amazon,\n"
            "  иначе документы не дойдут (без уведомления)\n"
            "• Amazon даёт 5 ГБ бесплатного хранилища; старые документы могут удаляться\n\n"
            "<b>Команды:</b>\n"
            "/setkindle &lt;email&gt; — сохранить адрес Kindle\n"
            "/myemail — показать адрес для белого списка Amazon\n"
            "/status — ваши настройки и счётчик отправок\n"
            "/convert — переключить авто-конвертацию Amazon\n"
            "/language — сменить язык\n"
            "/help — это сообщение"
        ),
        "btn_send": "✅ Отправить",
        "btn_cancel": "❌ Отмена",
        "language_choose": "🌐 Выберите язык:",
        "language_set": "✅ Язык переключён на <b>Русский</b>.",
        "setkindle_usage": (
            "Использование: <code>/setkindle your_name@kindle.com</code>\n\n"
            "Ваш адрес Kindle можно найти на amazon.com → Manage Your Content and "
            "Devices → Devices → (ваш Kindle)."
        ),
        "setkindle_invalid": (
            "Это не похоже на адрес Kindle. Он должен заканчиваться на "
            "<b>@kindle.com</b>, например <code>your_name@kindle.com</code>."
        ),
        "setkindle_saved": (
            "✅ Сохранено! Я буду отправлять документы на <code>{email}</code>.\n\n"
            "⚠️ Убедитесь, что <code>{sender}</code> есть в вашем Amazon Approved Personal "
            "Document E-mail List, иначе доставка молча не сработает."
        ),
        "myemail": (
            "📧 Мой адрес отправителя:\n<code>{sender}</code>\n\n"
            "<b>Добавьте его</b> в ваш Amazon Approved Personal Document E-mail List:\n"
            "amazon.com →  <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences → "
            "Personal Document Settings.\n\n"
            "Без этого Amazon молча отклоняет всё, что я отправляю."
        ),
        "status": (
            "<b>Ваши настройки</b>\n"
            "Адрес Kindle: <code>{kindle}</code>\n"
            "Отправлено документов: <b>{count}</b>\n"
            "Авто-конвертация: <b>{convert}</b>\n"
            "Язык: <b>{lang}</b>"
        ),
        "status_no_kindle": "— (используйте /setkindle)",
        "state_on": "вкл",
        "state_off": "выкл",
        "convert_on": (
            "Авто-конвертация теперь <b>ВКЛ</b>.\n"
            'Тема письма ставится "Convert", чтобы Amazon конвертировал форматы '
            "вроде DOCX в формат Kindle."
        ),
        "convert_off": "Авто-конвертация теперь <b>ВЫКЛ</b>.",
        "unsupported": "❌ Неподдерживаемый тип файла <b>{ext}</b>.{hint}\n\n✅ Я принимаю: {formats}",
        "unsupported_hint": " Amazon не принимает файлы {ext}.",
        "too_large": (
            "❌ Файл слишком большой. Мой лимит — {max_mb} МБ "
            "(ограничение загрузки Telegram Bot API)."
        ),
        "no_kindle": (
            "Вы ещё не указали адрес Kindle.\n"
            "Сначала используйте <code>/setkindle your_name@kindle.com</code>."
        ),
        "rate_limited": (
            "⏳ Достигнут дневной лимит ({limit} документов в день). Попробуйте завтра."
        ),
        "confirm_prompt": "Отправить <b>{filename}</b> на <code>{email}</code>?",
        "sending": "Отправляю…",
        "sent_ok": (
            "✅ Отправлено <b>{filename}</b> на <code>{email}</code>.\n\n"
            "Если не дойдёт — проверьте, что <code>{sender}</code> в белом списке Amazon."
        ),
        "cancelled": "❌ Отменено. Ничего не отправлено.",
        "cancelled_answer": "Отменено.",
        "expired": "Запрос устарел — пришлите файл заново.",
        "send_error": "❌ Что-то пошло не так при отправке. Попробуйте позже.",
        "set_kindle_first": "Сначала укажите адрес Kindle командой /setkindle.",
        "setkindle_prompt": (
            "📧 Пришлите ваш адрес Kindle.\n"
            "Он выглядит как <code>your_name@kindle.com</code>.\n\n"
            "Отправьте /cancel для отмены."
        ),
        "action_cancelled": "✅ Отменено.",
        "cancel_nothing": "Отменять нечего.",
    },
    # ──────────────────────────── Uzbek ──────────────────────────────────────
    "uz": {
        "welcome": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "Menga qo‘llab-quvvatlanadigan istalgan hujjatni yuboring — uni Kindle’ingizga yetkazaman.\n\n"
            "<b>Bir martalik sozlash:</b>\n"
            "1. /myemail — mening jo‘natuvchi manzilimni oling\n"
            "2. Uni <b>Amazon Approved Personal Document E-mail List</b>’ga qo‘shing\n"
            "   (amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings)\n"
            "3. /setkindle your_name@kindle.com — Kindle manzilingizni saqlang\n\n"
            "Shundan so‘ng faylni yuboravering! Tafsilot va cheklovlar — /help.\n\n"
            "🌐 Tilni o‘zgartirish: /language"
        ),
        "help": (
            "📚 <b>Kindle Sender Bot</b>\n\n"
            "<b>SOZLASH (bir marta):</b>\n"
            "1. /myemail — jo‘natuvchi manzilimni olish\n"
            "2. amazon.com → <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → Preferences →\n"
            "   Personal Document Settings → Approved Personal Document E-mail List → qo‘shing\n"
            "3. /setkindle your_name@kindle.com — Kindle manzilingizni saqlash\n\n"
            "<b>YUBORISH:</b>\nQo‘llab-quvvatlanadigan faylni shu chatga yuboravering!\n\n"
            "✅ <b>Qo‘llab-quvvatlanadi:</b>\n{formats}\n\n"
            "⚠️ <b>Cheklovlar:</b>\n"
            "• Maksimal fayl hajmi: {max_mb} MB (Telegram Bot API cheklovi)\n"
            "• Amazon’ning o‘z chegarasi — 50 MB; kattaroq fayllar uchun maxsus sozlash kerak\n"
            "• EPUB uchun 2022-yildan keyingi proshivkali Kindle kerak\n"
            "• Jo‘natuvchi manzilingiz Amazon sozlamalarida ALBATTA oq ro‘yxatda bo‘lishi shart,\n"
            "  aks holda hujjatlar (ogohlantirishsiz) yetib bormaydi\n"
            "• Amazon 5 GB bepul xotira beradi; eski hujjatlar o‘chirilishi mumkin\n\n"
            "<b>Buyruqlar:</b>\n"
            "/setkindle &lt;email&gt; — Kindle manzilingizni saqlash\n"
            "/myemail — Amazon oq ro‘yxati uchun manzilni ko‘rsatish\n"
            "/status — sozlamalaringiz va yuborishlar soni\n"
            "/convert — Amazon avto-konvertatsiyasini almashtirish\n"
            "/language — tilni o‘zgartirish\n"
            "/help — shu xabar"
        ),
        "btn_send": "✅ Yuborish",
        "btn_cancel": "❌ Bekor qilish",
        "language_choose": "🌐 Tilni tanlang:",
        "language_set": "✅ Til <b>O‘zbekcha</b>ga o‘rnatildi.",
        "setkindle_usage": (
            "Foydalanish: <code>/setkindle your_name@kindle.com</code>\n\n"
            "Kindle manzilingizni amazon.com →  <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Manage Your Content and Devices</a> → "
            "Devices → (Kindle’ingiz) bo‘limidan topasiz."
        ),
        "setkindle_invalid": (
            "Bu Kindle manziliga o‘xshamaydi. U <b>@kindle.com</b> bilan tugashi kerak, "
            "masalan <code>your_name@kindle.com</code>."
        ),
        "setkindle_saved": (
            "✅ Saqlandi! Hujjatlaringizni <code>{email}</code> manziliga yuboraman.\n\n"
            "⚠️ <code>{sender}</code> manzili <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Amazon Approved Personal Document E-mail List</a>’da ekanligiga ishonch hosil qiling, aks holda yetkazish jimgina amalga oshmaydi."
        ),
        "myemail": (
            "📧 Mening jo‘natuvchi manzilim:\n<code>{sender}</code>\n\n"
            "<b>Uni qo‘shing</b> — <a href=\"https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment:~:text=Approved%20Personal%20Document%20E%2Dmail%20List\">Amazon Approved Personal Document E-mail List</a>’ga:\n"
            "amazon.com → Manage Your Content and Devices → Preferences → "
            "Personal Document Settings.\n\n"
            "Busiz Amazon men yuborgan hamma narsani jimgina rad etadi."
        ),
        "status": (
            "<b>Sozlamalaringiz</b>\n"
            "Kindle manzili: <code>{kindle}</code>\n"
            "Yuborilgan hujjatlar: <b>{count}</b>\n"
            "Avto-konvertatsiya: <b>{convert}</b>\n"
            "Til: <b>{lang}</b>"
        ),
        "status_no_kindle": "— (/setkindle dan foydalaning)",
        "state_on": "yoqilgan",
        "state_off": "o‘chirilgan",
        "convert_on": (
            "Avto-konvertatsiya endi <b>YOQILGAN</b>.\n"
            'Xat mavzusi "Convert" qilib qo‘yiladi, shunda Amazon DOCX kabi '
            "formatlarni Kindle formatiga o‘giradi."
        ),
        "convert_off": "Avto-konvertatsiya endi <b>O‘CHIRILGAN</b>.",
        "unsupported": "❌ Qo‘llab-quvvatlanmaydigan fayl turi <b>{ext}</b>.{hint}\n\n✅ Men qabul qilaman: {formats}",
        "unsupported_hint": " Amazon {ext} fayllarini qabul qilmaydi.",
        "too_large": (
            "❌ Bu fayl juda katta. Mening chegaram — {max_mb} MB "
            "(Telegram Bot API yuklab olish chegarasi)."
        ),
        "no_kindle": (
            "Siz hali Kindle manzilingizni kiritmadingiz.\n"
            "Avval <code>/setkindle your_name@kindle.com</code> dan foydalaning."
        ),
        "rate_limited": (
            "⏳ Kunlik chegaraga yetdingiz (kuniga {limit} hujjat). Ertaga urinib ko‘ring."
        ),
        "confirm_prompt": "<b>{filename}</b> ni <code>{email}</code> ga yuborilsinmi?",
        "sending": "Yuborilmoqda…",
        "sent_ok": (
            "✅ <b>{filename}</b> <code>{email}</code> ga yuborildi.\n\n"
            "Yetib bormasa — <code>{sender}</code> Amazon oq ro‘yxatida ekanligini tekshiring."
        ),
        "cancelled": "❌ Bekor qilindi. Hech narsa yuborilmadi.",
        "cancelled_answer": "Bekor qilindi.",
        "expired": "So‘rov eskirdi — faylni qaytadan yuboring.",
        "send_error": "❌ Yuborishda nimadir xato ketdi. Keyinroq urinib ko‘ring.",
        "set_kindle_first": "Avval /setkindle bilan Kindle manzilingizni kiriting.",
        "setkindle_prompt": (
            "📧 Kindle manzilingizni yuboring.\n"
            "U <code>your_name@kindle.com</code> ko‘rinishida bo‘ladi.\n\n"
            "Bekor qilish uchun /cancel yuboring."
        ),
        "action_cancelled": "✅ Bekor qilindi.",
        "cancel_nothing": "Bekor qiladigan narsa yo‘q.",
    },
}
