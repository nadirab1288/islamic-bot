import asyncio
import random
import json
import os
import logging
from datetime import datetime, date

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

# ==========================================
# 1. КОНФИГУРАЦИЯ
# ==========================================
API_TOKEN = os.getenv("BOT_TOKEN", "8655013275:AAF_FNcJ-GmhzLFXj4NvcN1GGj0q2ZG5hXY")
CHANNEL_LINK = '<a href="https://t.me/salyaf64">@salyaf64</a>'

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

FILES = {
    "users": "users.json",
    "counter": "counter.json",
    "daily": "daily_counter.json",
    "quiz": "quiz_progress.json",
    "prayer": "prayer_tracker.json"
}

# ==========================================
# 2. БАЗЫ ДАННЫХ
# ==========================================

# 99 ИМЁН АЛЛАХА (первые 20 для примера - добавь остальные по желанию)
ALLAH_NAMES = {
    "🕌 Аллах (الله)": {
        "translit": "Аллах",
        "meaning": "Единственный достойный поклонения Бог",
        "desc": "Величайшее имя Аллаха, включающее все остальные имена и атрибуты."
    },
    "💚 Ар-Рахман (الرحمن)": {
        "translit": "Ар-Рахман",
        "meaning": "Милостивый",
        "desc": "Тот, чья милость охватывает всё сущее в этом мире."
    },
    "💚 Ар-Рахим (الرحيم)": {
        "translit": "Ар-Рахим",
        "meaning": "Милосердный",
        "desc": "Тот, кто проявляет особую милость к верующим в Последней жизни."
    },
    "👑 Аль-Малик (الملك)": {
        "translit": "Аль-Малик",
        "meaning": "Властелин",
        "desc": "Истинный Царь и Властелин всего сущего, у Которого нет сотоварища."
    },
    "✨ Аль-Куддус (القدوس)": {
        "translit": "Аль-Куддус",
        "meaning": "Святой",
        "desc": "Пречистый от всех недостатков, пороков и несовершенств."
    },
    "🕊️ Ас-Салям (السلام)": {
        "translit": "Ас-Салям",
        "meaning": "Источник мира",
        "desc": "Тот, кто свободен от всех недостатков и дарует мир Своим рабам."
    },
    "🛡️ Аль-Муъмин (المؤمن)": {
        "translit": "Аль-Муъмин",
        "meaning": "Дарующий безопасность",
        "desc": "Тот, кто дарует верующим безопасность в этом мире и в Последней жизни."
    },
    "⚖️ Аль-Мухаймин (المهيمن)": {
        "translit": "Аль-Мухаймин",
        "meaning": "Хранитель",
        "desc": "Всевышний Наблюдатель и Хранитель всего сущего."
    },
    "💪 Аль-Азиз (العزيز)": {
        "translit": "Аль-Азиз",
        "meaning": "Могущественный",
        "desc": "Обладатель силы и могущества, Которого никто не может победить."
    },
    "🔥 Аль-Джаббар (الجبار)": {
        "translit": "Аль-Джаббар",
        "meaning": "Величественный",
        "desc": "Тот, кто принуждает Своих рабов к тому, что Он пожелает, и исправляет дела Своих творений."
    },
    "👑 Аль-Мутакаббир (المتكبر)": {
        "translit": "Аль-Мутакаббир",
        "meaning": "Великий",
        "desc": "Обладатель величия и гордости, Которому подобает только Ему одному."
    },
    "🎨 Аль-Халик (الخالق)": {
        "translit": "Аль-Халик",
        "meaning": "Творец",
        "desc": "Тот, кто создал всё из небытия и определил всему меру."
    },
    "🔨 Аль-Бари (البارئ)": {
        "translit": "Аль-Бари",
        "meaning": "Создатель",
        "desc": "Тот, кто создал творения без примера и образца."
    },
    "🎭 Аль-Мусаввир (المصور)": {
        "translit": "Аль-Мусаввир",
        "meaning": "Придающий образ",
        "desc": "Тот, кто придаёт каждому творению совершенный образ и форму."
    },
    " Аль-Гаффар (الغفار)": {
        "translit": "Аль-Гаффар",
        "meaning": "Прощающий",
        "desc": "Тот, кто многократно прощает грехи Своих рабов."
    },
    "💎 Аль-Каххар (القهار)": {
        "translit": "Аль-Каххар",
        "meaning": "Покоряющий",
        "desc": "Тот, кто покоряет Своих рабов и подчиняет их Своей воле."
    },
    "🎁 Аль-Ваххаб (الوهاب)": {
        "translit": "Аль-Ваххаб",
        "meaning": "Дарующий",
        "desc": "Тот, кто дарует Своим рабам блага безвозмездно и без расчёта."
    },
    "💰 Ар-Раззак (الرزاق)": {
        "translit": "Ар-Раззак",
        "meaning": "Наделяющий уделом",
        "desc": "Тот, кто наделяет уделом все Свои творения."
    },
    "🚪 Аль-Фаттах (الفتاح)": {
        "translit": "Аль-Фаттах",
        "meaning": "Открывающий",
        "desc": "Тот, кто открывает Своим рабам двери милости и облегчения."
    },
    "📚 Аль-Алим (العليم)": {
        "translit": "Аль-Алим",
        "meaning": "Всезнающий",
        "desc": "Тот, кто знает всё явное и скрытое, прошлое и будущее."
    }
}

# 40 ХАДИСОВ АН-НАВАВИ (первые 10 для примера)
NAWAWI_HADITHS = {
    "1. Намерение": "📖 Пророк (ﷺ) сказал:\n\n«Поистине, дела оцениваются только по намерениям, и каждому человеку достанется лишь то, что он намеревался сделать».\n\n(Аль-Бухари 1, Муслим 1907)\n\n **Пояснение:**\nЭто один из важнейших хадисов в исламе. Намерение (ният) — основа всех поклонений. Без искреннего намерения ради Аллаха даже благие дела не будут приняты.",
    
    "2. Ислам, Иман, Ихсан": "📖 Пророк (ﷺ) сказал:\n\n«Ислам — это свидетельство того, что нет божества, кроме Аллаха, и что Мухаммад — посланник Аллаха, совершение намаза, выплата закята, пост в Рамадан и совершение хаджа».\n\n(Муслим 8)\n\n💡 **Пояснение:**\nЭтот хадис описывает пять столпов ислама — основу религии, на которой строится жизнь мусульманина.",
    
    "3. Столпы Ислама": "📖 Пророк () сказал:\n\n«Ислам построен на пяти [столпах]: свидетельстве, что нет божества, кроме Аллаха, и что Мухаммад — Его раб и посланник; совершении намаза; выплате закята; совершении хаджа к Дому и посте в Рамадане».\n\n(Аль-Бухари 8, Муслим 16)\n\n💡 **Пояснение:**\nПять столпов — это основа, на которой держится ислам. Без них вера человека неполноценна.",
    
    "4. Этапы творения": " Пророк (ﷺ) сказал:\n\n«Поистине, каждый из вас был создан в чреве своей матери за сорок дней в виде капли семени».\n\n(Аль-Бухари 3208, Муслим 2643)\n\n💡 **Пояснение:**\nЭтот хадис напоминает о скромности человека и о том, что Аллах создал его из ничтожной капли.",
    
    "5. Запрет нововведений": "📖 Пророк (ﷺ) сказал:\n\n«Кто внесёт в это наше дело [религию] то, что не имеет к нему отношения, то это будет отвергнуто».\n\n(Аль-Бухари 2697, Муслим 1718)\n\n💡 **Пояснение:**\nВажное предупреждение о недопустимости нововведений (бид'а) в религии. Религия совершенна и не нуждается в дополнениях.",
    
    "6. Остерегайся сомнительного": " Пророк (ﷺ) сказал:\n\n«Халяль ясен, и харам ясен, а между ними есть сомнительные дела».\n\n(Аль-Бухари 52, Муслим 1599)\n\n💡 **Пояснение:**\nМудрость этого хадиса в том, чтобы мусульманин остерегался сомнительного, чтобы не впасть в запретное.",
    
    "7. Религия — это искренность": " Пророк (ﷺ) сказал:\n\n«Религия — это искренность».\n\n(Муслим 55)\n\n💡 **Пояснение:**\nИскренность (насиха) — это основа религии. Она включает искренность к Аллаху, Его Книге, посланнику, руководителям мусульман и всем мусульманам.",
    
    "8. Запрет крови мусульманина": "📖 Пророк (ﷺ) сказал:\n\n«Мне было велено сражаться с людьми, пока они не засвидетельствуют, что нет божества, кроме Аллаха».\n\n(Аль-Бухари 25, Муслим 22)\n\n💡 **Пояснение:**\nЭтот хадис говорит о важности шахады и защите ислама.",
    
    "9. Запретное — это то, что запретил Аллах": "📖 Пророк (ﷺ) сказал:\n\n«То, что Аллах сделал дозволенным в Своей Книге, то дозволено. А то, что Он запретил, то запрещено».\n\n(Муслим 1599)\n\n💡 **Пояснение:**\nИсточником законов является Коран и Сунна, а не мнения людей.",
    
    "10. Аллах прекрасен": "📖 Пророк (ﷺ) сказал:\n\n«Поистине, Аллах прекрасен и любит красоту».\n\n(Муслим 91)\n\n💡 **Пояснение:**\nАллах любит, чтобы Его рабы были красивы, опрятны и украшали себя в дозволенных рамках."
}

# Дуа для витр намаза (Кунут)
DUAS = {
    "🍽 Перед едой": "بِسْمِ اللَّهِ\n«Бисмиллях»\n(Во имя Аллаха)",
    "🍽 После еды": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ\n«Альхамду лилляхи ль-лязи атъамани хаза ва разақанихи мин гъайри хаулин минни ва ля қувватин»\n(Хвала Аллаху, Который накормил меня)",
    "📿 После азана": "اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ وَالصَّلَاةِ الْقَائِمَةِ آتِ مُحَمَّدًا الْوَسِيلَةَ وَالْفَضِيلَةَ\n«Аллахумма рабба хазихи ад-да'вати ат-таммати ва-с-салати аль-қа'имати, ати Мухаммадан аль-василата ва-ль-фадилата»\n(О Аллах, Господь этого совершенного призыва, даруй Мухаммаду посредничество)",
    "🌙 Витр намаз (Кунут)": "اللَّهُمَّ إِنَّا نَسْتَعِينُكَ وَنَسْتَهْدِيكَ وَنَسْتَغْفِرُكَ وَنَتُوبُ إِلَيْكَ\nوَنُؤْمِنُ بِكَ وَنَتَوَكَّلُ عَلَيْكَ\nوَنُثْنِي عَلَيْكَ الْخَيْرَ كُلَّهُ نَشْكُرُكَ وَلَا نَكْفُرُكَ\nوَنَخْلَعُ وَنَتْرُكُ مَنْ يَفْجُرُكَ\n\nاللَّهُمَّ إِيَّاكَ نَعْبُدُ وَلَكَ نُصَلِّي وَنَسْجُدُ\nوَإِلَيْكَ نَسْعَى وَنَحْفِدُ\nنَرْجُو رَحْمَتَكَ وَنَخْشَى عَذَابَكَ\nإِنَّ عَذَابَكَ بِالْكُفَّارِ مُلْحِقٌ\n\n«Аллахумма, инна наста'инукя ва настахдикя ва настагфирукя ва натубу 'иляйк»\n«ва ну'мину бикя ва натаваккалю 'аляйка»\n«ва нусни 'аляйкя-ль-хайра кулляху, нашкурукя ва ля накфурук»\n«ва нахля'у ва натруку май-йафджурук»\n\n«Аллахумма, ийакя на'буду, ва лякя нусолли ва насджуд»\n«ва иляйкя нас'а ва нахфид»\n«нарджу рахматакя, ва нахша 'азабак»\n«инна 'азабакаль-джидда би-ль-куффари мульхик»\n\n📖 Перевод:\nО, Аллах, мы просим Твоей помощи, ищем Твоего руководства, прощения и раскаиваемся перед Тобой.\nМы веруем в Тебя и полагаемся на Тебя.\nМы восхваляем Тебя наилучшим образом, благодарим и не из числа неблагодарных.\nМы оставляем и отбрасываем всех непокорных Тебе.\n\nО, Аллах, только Тебе мы поклоняемся, лишь Тебе молимся и перед Тобой простираемся ниц.\nМы устремляемся к Тебе и быстры в служении.\nНадеемся на Твою милость и боимся Твоего гнева.\nВоистину, Твоё наказание постигнет неверующих.",
    "😴 Перед сном": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا\n«Бисмикя Аллахумма амуту ва ахья»\n(С Твоим именем, о Аллах, я умираю и оживаю)",
    "☀️ После пробуждения": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ\n«Альхамду лилляхи ль-лязи ахьяна баъда ма аматана ва иляйхи н-нушур»\n(Хвала Аллаху, Который оживил нас после того, как умертвил нас)",
    " Выход из дома": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ\n«Бисмилляхи таваккальту ъаля Ллахи ва ля хауля ва ля қуввата илля биллях»\n(Во имя Аллаха, уповаю на Аллаха)",
    "🏠 Вход в дом": "بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى رَبِّنَا تَوَكَّلْنَا\n«Бисмилляхи воляджна ва бисмилляхи хараджна ва ъаля Раббина таваккальна»\n(Во имя Аллаха мы вошли и вышли)",
    "😰 Тревога/Страх": "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ\n«Хасбуна Ллаху ва ни'маль вакиль»\n(Достаточен нам Аллах, и Он — лучший Попечитель)",
    " За родителей": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا\n«Рабби рхамhума кама раббаяни сагира»\n(Господь, помилуй их, как они растили меня малым)",
    "📚 За знание": "اللَّهُمَّ انْفَعْنِي بِمَا عَلَّمْتَنِي وَعَلِّمْنِي مَا يَنْفَعُنِي وَزِدْنِي عِلْمًا\n«Аллахумма нфа'ни би-ма 'алламтани ва 'аллимни ма янфа'уни ва зидни 'ильман»\n(О Аллах, принеси пользу тем, чему научил)",
    "🛒 Перед покупкой": "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَهَا وَخَيْرَ مَا جُبِلَتْ عَلَيْهِ\n«Аллахумма инни ас'алюка хайраhа ва хайра ма джубилат 'алейhи»\n(О Аллах, прошу о благе этого)",
    " Дождь": "اللَّهُمَّ صَيِّبًا نَافِعًا\n«Аллахумма саййибан нафи'ан»\n(О Аллах, сделай дождь полезным!)",
    "️ Гроза": "سُبْحَانَ الَّذِي يُسَبِّحُ الرَّعْدُ بِحَمْدِهِ وَالْمَلَائِكَةُ مِنْ خِيفَتِهِ\n«Субхана ль-лязи юсаббиху р-ра'ду би-хамдиhи»\n(Пречист Тот, Которого восхваляет гром)",
    "🤧 При чихании": "الْحَمْدُ لِلَّهِ\n«Альхамду лиллях»\n(Хвала Аллаху)",
    "🕌 Вход в мечеть": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ\n«Аллахумма фтах ли абваба раhматик»\n(Открой мне двери Твоей милости)",
    "🕌 Выход из мечети": "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ\n«Аллахумма инни ас'алюка мин фадлик»\n(Прошу Тебя из Твоей милости)",
    " При болезни": "بِسْمِ اللَّهِ أَعُوذُ بِاللَّهِ مِنْ شَرِّ مَا أَجِدُ\n«Бисмилляхи а'узу билляхи мин шарри ма аджиду»\n(С именем Аллаха прибегаю к защите от зла)",
    "🆘 Экстренная помощь": "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ\n«Ля иляха илля Анта субханака инни кунту мин аз-залимин»\n(Нет божества, кроме Тебя, пречист Ты)",
    "💔 При горе/печали": "اللَّهُمَّ رَحْمَتَكَ أَرْجُو فَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ\n«Аллахумма рахматака арджу фа-ля такилни иля нафси тарфата 'айн»\n(О Аллах, надеюсь на Твою милость)"
}

QURAN_DUAS = {
    " Дуа пророка Адама (7:23)": "رَبَّنَا ظَلَمْنَا أَنْفُسَنَا وَإِنْ لَمْ تَغْفِرْ لَنَا وَتَرْحَمْنَا لَنَكُونَنَّ مِنَ الْخَاسِرِينَ\n«Раббана заalamна анфусана ва иль лам тагфир лана ва тархамна лянакунанна мина ль-хасирин»\n(Господь наш! Мы были несправедливы к себе, прости нас и помилуй)",
    "📖 Дуа пророка Нуха (11:47)": "رَبِّ إِنِّي أَعُوذُ بِكَ أَنْ أَسْأَلَكَ مَا لَيْسَ لِي بِهِ عِلْمٌ\n«Рабби инни а'узу бика ан ас'алюка ма ляйса ли биhи 'ильм»\n(Господь, прибегаю к Тебе от того, чтобы просить о том, чего не знаю)",
    "📖 Дуа пророка Ибрахима (14:40)": "رَبِّ اجْعَلْنِي مُقِيمَ الصَّلَاةِ وَمِنْ ذُرِّيَّتِي\n«Рабби дж'ални муқима с-салати ва мин зуррияти»\n(Господь, сделай меня совершающим намаз и моих потомков)",
    "📖 Дуа пророка Мусы (20:25-26)": "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي\n«Рабби ишрах ли садри ва яссир ли амри»\n(Господь, раскрой мою грудь и облегчи моё дело)",
    "📖 Дуа пророка Юнуса (21:87)": "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ\n«Ля иляха илля Анта субханака инни кунту мин аз-залимин»\n(Нет божества, кроме Тебя, пречист Ты)",
    "📖 Дуа пророка Закарии (21:89)": "رَبِّ لَا تَذَرْنِي فَرْدًا وَأَنْتَ خَيْرُ الْوَارِثِينَ\n«Рабби ля тазарни фардан ва Анта хайру ль-варисин»\n(Господь, не оставляй меня одиноким)",
    " Дуа пророка Айюба (21:83)": "أَنِّي مَسَّنِيَ الضُّرُّ وَأَنْتَ أَرْحَمُ الرَّاحِمِينَ\n«Анни массани яд-дурру ва Анта архаму р-рахимин»\n(Беда постигла меня, а Ты — милостивейший)",
    "📖 Дуа пророка Сулеймана (27:19)": "رَبِّ أَوْزِعْنِي أَنْ أَشْكُرَ نِعْمَتَكَ الَّتِي أَنْعَمْتَ عَلَيَّ\n«Рабби авзи'ни ан ашкура ни'матака алляти ан'amта 'alayya»\n(Господь, вдохнови меня быть благодарным)",
    "📖 Дуа пророка Мухаммада ﷺ (2:201)": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ\n«Раббана атина фи д-дунья хасаната ва фи ль-ахирати хасаната ва қина 'азаба н-нар»\n(Господь, даруй нам благо в этом мире и в Последней жизни)",
    "📖 Дуа для родителей (71:28)": "رَبِّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِمَنْ دَخَلَ بَيْتِيَ مُؤْمِنًا\n«Рабби игфир ли ва ли-валидайя ва ли-ман дахала байти му'минан»\n(Господь, прости меня, моих родителей и верующих)"
}

QUIZ_QUESTIONS = [
    {"q": "Сколько ракаатов в Фаджре?", "o": ["2", "3", "4"], "c": 0, "e": "Фаджр: 2 сунны + 2 фарда."},
    {"q": "Какая сура — «Сердце Корана»?", "o": ["Аль-Фатиха", "Ясин", "Аль-Мульк"], "c": 1, "e": "Сердце Корана — сура Ясин (Тирмизи)."},
    {"q": "Первый столп Ислама?", "o": ["Намаз", "Шахада", "Закят"], "c": 1, "e": "Шахада — первый и главный столп."},
    {"q": "Месяц ниспослания Корана?", "o": ["Шаабан", "Рамадан", "Мухаррам"], "c": 1, "e": "Коран ниспослан в Рамадан (Бакара 2:185)."},
    {"q": "Что означает «Ислам»?", "o": ["Мир", "Покорность", "Вера"], "c": 1, "e": "Ислам — покорность Единому Богу."},
    {"q": "Сколько обязательных намазов?", "o": ["3", "4", "5"], "c": 2, "e": "Пять ежедневных намазов."},
    {"q": "Лучший зикр по словам Пророка ()?", "o": ["СубханАллах", "Альхамдулиллях", "Ля иляха илляЛлах"], "c": 2, "e": "Лучшее поминовение — Ля иляха илляЛлах."},
    {"q": "Ночной путь из Мекки в Иерусалим?", "o": ["Хиджра", "Исра", "Мирадж"], "c": 1, "e": "Исра — в Иерусалим, Мирадж — на небеса."},
    {"q": "Что такое Сунна?", "o": ["Коран", "Путь Пророка ﷺ", "Мечеть"], "c": 1, "e": "Слова, действия и одобрения Пророка (ﷺ)."},
    {"q": "Сура защиты от могилы?", "o": ["Аят аль-Курси", "Аль-Мульк", "Аль-Ихляс"], "c": 1, "e": "Сура Аль-Мульк защищает от мучений в могиле."},
    {"q": "Сколько столпов у Ислама?", "o": ["3", "4", "5"], "c": 2, "e": "Пять: Шахада, Намаз, Закят, Пост, Хадж."},
    {"q": "Праздничный намаз?", "o": ["Витр", "Ид-намаз", "Тарауих"], "c": 1, "e": "Ид-намаз в Курбан и Ураза байрам."},
    {"q": "Что такое Таухид?", "o": ["Единобожие", "Молитва", "Пост"], "c": 0, "e": "Убеждение в единственности Аллаха."},
    {"q": "Первый муэдзин?", "o": ["Абу Бакр", "Биляль", "Умар"], "c": 1, "e": "Биляль ибн Рабах."},
    {"q": "Сура в каждом ракаате?", "o": ["Аль-Ихляс", "Аль-Фатиха", "Ан-Нас"], "c": 1, "e": "Аль-Фатиха обязательна в каждом ракаате."},
    {"q": "Что такое Иджма?", "o": ["Мнение", "Единогласие учёных", "Аналогия"], "c": 1, "e": "Единогласие учёных уммы."},
    {"q": "Длительность Рамадана?", "o": ["28-29", "29-30", "30-31"], "c": 1, "e": "29 или 30 дней по луне."},
    {"q": "Первая кибла?", "o": ["Мекка", "Медина", "Иерусалим"], "c": 2, "e": "Масджид аль-Акса в Иерусалиме."},
    {"q": "Что такое Фитра?", "o": ["Закят имущества", "Милостыня разговения", "Садака"], "c": 1, "e": "Обязательная милостыня в конце Рамадана."},
    {"q": "Кто такой Халиф?", "o": ["Пророк", "Наследник/правитель", "Судья"], "c": 1, "e": "Наследник Пророка в управлении общиной."},
    {"q": "Сура без Бисмиллях?", "o": ["Ат-Тауба", "Аль-Фатиха", "Ясин"], "c": 0, "e": "Сура Ат-Тауба (Покаяние)."},
    {"q": "Что такое Куфр?", "o": ["Неверие", "Лицемерие", "Многобожие"], "c": 0, "e": "Неверие и отрицание истин Ислама."},
    {"q": "Пророков в Коране?", "o": ["15", "25", "30"], "c": 1, "e": "25 пророков упомянуты по имени."},
    {"q": "Что такое Амана?", "o": ["Доверие", "Наказание", "Награда"], "c": 0, "e": "Доверие, принятое только человеком."},
    {"q": "Ангел откровения?", "o": ["Микаил", "Джибриль", "Исрафил"], "c": 1, "e": "Джибриль (мир ему)."}
]

# ==========================================
# 3. УТИЛИТЫ
# ==========================================
def load_json(name, default=None):
    path = FILES[name]
    if default is None: default = {}
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
    except (json.JSONDecodeError, ValueError):
        pass
    return default

def save_json(name, data):
    with open(FILES[name], "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

def get_next_reminder():
    idx = load_json("counter", {"index": 0}).get("index", 0)
    rem = REMINDERS[idx]
    save_json("counter", {"index": (idx + 1) % len(REMINDERS)})
    return rem

def get_daily_content():
    data = load_json("daily", {"index": 0, "date": ""})
    today = datetime.now().strftime("%Y-%m-%d")
    if not isinstance(data, dict) or "index" not in data or "date" not in data:
        data = {"index": 0, "date": ""}
    if data["date"] != today:
        new_idx = (data["index"] + 1) % len(DAILY_CONTENT)
        data = {"index": new_idx, "date": today}
        save_json("daily", data)
    safe_idx = data["index"] % len(DAILY_CONTENT)
    return DAILY_CONTENT[safe_idx]

def get_quiz_seen(uid):
    return set(load_json("quiz", {}).get(str(uid), []))

def save_quiz_seen(uid, seen):
    d = load_json("quiz", {})
    d[str(uid)] = list(seen)
    save_json("quiz", d)

# ТРЕКЕР НАМАЗОВ
def get_prayer_status(uid):
    today = date.today().isoformat()
    data = load_json("prayer", {})
    user_data = data.get(str(uid), {})
    
    # Если дата не сегодняшняя — сбрасываем
    if user_data.get("date") != today:
        user_data = {
            "date": today,
            "fajr": False,
            "dhuhr": False,
            "asr": False,
            "maghrib": False,
            "isha": False
        }
        data[str(uid)] = user_data
        save_json("prayer", data)
    
    return user_data

def toggle_prayer(uid, prayer_name):
    data = load_json("prayer", {})
    user_data = get_prayer_status(uid)
    
    # Переключаем статус
    user_data[prayer_name] = not user_data[prayer_name]
    data[str(uid)] = user_data
    save_json("prayer", data)
    
    return user_data[prayer_name]

# Клавиатуры
MAIN_KB = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/further"), KeyboardButton(text="/shuffle")],
    [KeyboardButton(text="/dua"), KeyboardButton(text="/names")],
    [KeyboardButton(text="/hadith40"), KeyboardButton(text="/prayer")],
    [KeyboardButton(text="/quran_duas"), KeyboardButton(text="/quiz")],
    [KeyboardButton(text="/daily"), KeyboardButton(text="/status")]
], resize_keyboard=True)

BACK_BTN = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="↩️ Меню", callback_data="back")]])

# ==========================================
# 4. ОБРАБОТЧИКИ
# ==========================================
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    users = load_json("users")
    if uid not in users:
        users.append(uid)
        save_json("users", users)
    txt = (
        "Ассаляму алейкум! 🌙\n\n"
        "Я бот для напоминаний о важном.\n\n"
        "<b>Команды:</b>\n"
        "• /further — следующее напоминание по очереди\n"
        "• /shuffle — случайное напоминание\n"
        "• /status — номер в очереди\n"
        "• /dua — дуа по ситуациям\n"
        "• /names — 99 имён Аллаха\n"
        "• /hadith40 — 40 хадисов ан-Навави\n"
        "• /prayer — трекер намазов\n"
        "• /quran_duas — дуа пророков из Корана\n"
        "• /daily — аят или хадис дня\n"
        "• /quiz — викторина (25 вопросов)\n"
        "• Цифра 1–50 — конкретное напоминание\n\n"
        " Ежедневно в 08:00 присылаю контент.\n\n"
        f"📢 <b>Рекомендуем:</b>\n"
        f"Канал {CHANNEL_LINK} — Коран, хадисы, лекции, викторины!"
    )
    await m.answer(txt, disable_web_page_preview=False)

@dp.message(Command("menu"))
async def cmd_menu(m: types.Message):
    await m.answer("Главное меню:", reply_markup=MAIN_KB)

@dp.message(Command("further"))
async def cmd_further(m: types.Message):
    await m.answer(get_next_reminder())

@dp.message(Command("shuffle"))
async def cmd_shuffle(m: types.Message):
    await m.answer(random.choice(REMINDERS))

@dp.message(Command("status"))
async def cmd_status(m: types.Message):
    idx = load_json("counter", {"index": 0}).get("index", 0)
    await m.answer(f"📊 Напоминание №{idx+1} из {len(REMINDERS)}.\n\nСледующее:\n{REMINDERS[idx]}")

@dp.message(Command("daily"))
async def cmd_daily(m: types.Message):
    try:
        c = get_daily_content()
        await m.answer(f"<b>{c['title']}</b>\n\n{c['text']}")
    except Exception as e:
        logging.error(f"Ошибка /daily: {e}")
        await m.answer("Произошла ошибка при получении контента дня.")

@dp.message(Command("dua"))
async def cmd_dua(m: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=k) for k in list(DUAS.keys())[i:i+2]]
        for i in range(0, len(DUAS), 2)
    ] + [[KeyboardButton(text="↩️ Меню")]], resize_keyboard=True)
    await m.answer("<b>🤲 Выбери ситуацию:</b>", reply_markup=kb)

@dp.message(F.text.in_(list(DUAS.keys())))
async def dua_select(m: types.Message):
    text = m.text.strip()
    if text in DUAS:
        await m.answer(f"<b>{text}</b>\n\n{DUAS[text]}", reply_markup=BACK_BTN)
    else:
        await m.answer("Эта категория не найдена.", reply_markup=BACK_BTN)

@dp.message(Command("names"))
async def cmd_names(m: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=k) for k in list(ALLAH_NAMES.keys())[i:i+1]]
        for i in range(0, len(ALLAH_NAMES), 1)
    ] + [[KeyboardButton(text="↩️ Меню")]], resize_keyboard=True)
    await m.answer("<b>🕌 99 имён Аллаха:</b>\n\nВыбери имя:", reply_markup=kb)

@dp.message(F.text.in_(list(ALLAH_NAMES.keys())))
async def name_select(m: types.Message):
    text = m.text.strip()
    if text in ALLAH_NAMES:
        name = ALLAH_NAMES[text]
        await m.answer(
            f"<b>{text}</b>\n\n"
            f"📖 <b>Транслитерация:</b> {name['translit']}\n"
            f" <b>Значение:</b> {name['meaning']}\n\n"
            f"📚 <b>Описание:</b>\n{name['desc']}",
            reply_markup=BACK_BTN
        )
    else:
        await m.answer("Имя не найдено.", reply_markup=BACK_BTN)

@dp.message(Command("hadith40"))
async def cmd_hadith40(m: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=k) for k in list(NAWAWI_HADITHS.keys())[i:i+1]]
        for i in range(0, len(NAWAWI_HADITHS), 1)
    ] + [[KeyboardButton(text="↩️ Меню")]], resize_keyboard=True)
    await m.answer("<b> 40 хадисов имама ан-Навави:</b>\n\nВыбери хадис:", reply_markup=kb)

@dp.message(F.text.in_(list(NAWAWI_HADITHS.keys())))
async def hadith_select(m: types.Message):
    text = m.text.strip()
    if text in NAWAWI_HADITHS:
        await m.answer(NAWAWI_HADITHS[text], reply_markup=BACK_BTN)
    else:
        await m.answer("Хадис не найден.", reply_markup=BACK_BTN)

@dp.message(Command("prayer"))
async def cmd_prayer(m: types.Message):
    uid = m.from_user.id
    status = get_prayer_status(uid)
    
    # Создаём inline клавиатуру с галочками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{'✅' if status['fajr'] else ''} Фаджр",
            callback_data="prayer_fajr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['dhuhr'] else '⬜'} Зухр",
            callback_data="prayer_dhuhr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['asr'] else '⬜'} Аср",
            callback_data="prayer_asr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['maghrib'] else ''} Магриб",
            callback_data="prayer_maghrib"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['isha'] else ''} Иша",
            callback_data="prayer_isha"
        )],
        [InlineKeyboardButton(text="↩️ Меню", callback_data="back")]
    ])
    
    today = date.today().strftime("%d.%m.%Y")
    completed = sum([status['fajr'], status['dhuhr'], status['asr'], status['maghrib'], status['isha']])
    
    await m.answer(
        f"📅 <b>Трекер намазов</b>\n"
        f"Дата: {today}\n"
        f"Выполнено: {completed}/5\n\n"
        f"Нажми на намаз, чтобы отметить:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data.startswith("prayer_"))
async def prayer_callback(cb: types.CallbackQuery):
    prayer_name = cb.data.split("_")[1]
    uid = cb.from_user.id
    
    # Переключаем статус
    new_status = toggle_prayer(uid, prayer_name)
    
    # Обновляем сообщение
    status = get_prayer_status(uid)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{'✅' if status['fajr'] else '⬜'} Фаджр",
            callback_data="prayer_fajr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['dhuhr'] else '⬜'} Зухр",
            callback_data="prayer_dhuhr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['asr'] else '⬜'} Аср",
            callback_data="prayer_asr"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['maghrib'] else '⬜'} Магриб",
            callback_data="prayer_maghrib"
        )],
        [InlineKeyboardButton(
            text=f"{'✅' if status['isha'] else '⬜'} Иша",
            callback_data="prayer_isha"
        )],
        [InlineKeyboardButton(text="↩️ Меню", callback_data="back")]
    ])
    
    completed = sum([status['fajr'], status['dhuhr'], status['asr'], status['maghrib'], status['isha']])
    
    try:
        await cb.message.edit_text(
            f"📅 <b>Трекер намазов</b>\n"
            f"Дата: {date.today().strftime('%d.%m.%Y')}\n"
            f"Выполнено: {completed}/5\n\n"
            f"Нажми на намаз, чтобы отметить:",
            reply_markup=keyboard
        )
        await cb.answer()
    except:
        pass

@dp.message(Command("quran_duas"))
async def cmd_quran_duas(m: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=k) for k in list(QURAN_DUAS.keys())[i:i+1]]
        for i in range(0, len(QURAN_DUAS), 1)
    ] + [[KeyboardButton(text="️ Меню")]], resize_keyboard=True)
    await m.answer("<b>📖 Дуа пророков из Корана:</b>\n\nВыбери дуа:", reply_markup=kb)

@dp.message(F.text.in_(list(QURAN_DUAS.keys())))
async def quran_dua_select(m: types.Message):
    text = m.text.strip()
    if text in QURAN_DUAS:
        await m.answer(f"{text}\n\n{QURAN_DUAS[text]}", reply_markup=BACK_BTN)
    else:
        await m.answer("Дуа не найдено.", reply_markup=BACK_BTN)

# --- ВИКТОРИНА ---
async def send_quiz(bot_obj, chat_id, uid):
    seen = get_quiz_seen(uid)
    avail = [i for i in range(len(QUIZ_QUESTIONS)) if i not in seen]
    if not avail:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Заново", callback_data="reset_q")],
            [InlineKeyboardButton(text="↩️ Меню", callback_data="back")]
        ])
        await bot_obj.send_message(chat_id, "🎉 <b>МашаАллах!</b> Все 25 вопросов пройдены!\n\nХочешь повторить?", reply_markup=kb)
        return
    qi = random.choice(avail)
    q = QUIZ_QUESTIONS[qi]
    btns = [[InlineKeyboardButton(text=o, callback_data=f"q:{qi}:{i}")] for i, o in enumerate(q["o"])]
    btns.append([InlineKeyboardButton(text="↩️ Меню", callback_data="back")])
    await bot_obj.send_message(
        chat_id,
        f"❓ <b>Вопрос ({len(seen)+1}/25):</b>\n{q['q']}\n\nВыбери ответ:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )

@dp.message(Command("quiz"))
async def quiz_start(m: types.Message):
    try: await send_quiz(bot, m.chat.id, m.from_user.id)
    except Exception as e:
        logging.error(e)
        await m.answer("Ошибка викторины.")

@dp.callback_query(F.data.startswith("q:"))
async def quiz_ans(cb: types.CallbackQuery):
    try:
        _, qi, ai = cb.data.split(":")
        qi, ai = int(qi), int(ai)
        q = QUIZ_QUESTIONS[qi]
        seen = get_quiz_seen(cb.from_user.id)
        seen.add(qi)
        save_quiz_seen(cb.from_user.id, seen)
        ok = (ai == q["c"])
        res = f"✅ <b>Верно!</b> МашаАллах!\n\n💡 {q['e']}" if ok else f"❌ <b>Неверно.</b>\n\nОтвет: <b>{q['o'][q['c']]}</b>\n\n💡 {q['e']}"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Ещё вопрос", callback_data="next_q")],
            [InlineKeyboardButton(text="↩️ Меню", callback_data="back")]
        ])
        await cb.message.edit_text(res, reply_markup=kb)
        await cb.answer()
    except Exception as e:
        logging.error(e)
        await cb.answer("Ошибка.", show_alert=True)

@dp.callback_query(F.data == "next_q")
async def quiz_next(cb: types.CallbackQuery):
    await send_quiz(bot, cb.message.chat.id, cb.from_user.id)
    await cb.answer()

@dp.callback_query(F.data == "reset_q")
async def quiz_reset(cb: types.CallbackQuery):
    d = load_json("quiz", {})
    if str(cb.from_user.id) in d: del d[str(cb.from_user.id)]
    save_json("quiz", d)
    await send_quiz(bot, cb.message.chat.id, cb.from_user.id)
    await cb.answer()

@dp.callback_query(F.data == "back")
async def go_back(cb: types.CallbackQuery):
    try:
        await cb.message.delete()
        await cb.message.answer("Главное меню:", reply_markup=MAIN_KB)
        await cb.answer()
    except: pass

@dp.message(F.text == "↩️ Меню")
async def back_text(m: types.Message):
    await m.answer("Главное меню:", reply_markup=MAIN_KB)

@dp.message(F.text.regexp(r'^\d+$'))
async def num_handler(m: types.Message):
    n = int(m.text)
    if 1 <= n <= len(REMINDERS):
        await m.answer(f" №{n}:\n\n{REMINDERS[n-1]}")
    else:
        await m.answer(f"❌ Только 1–{len(REMINDERS)}.")

# ==========================================
# 5. ФОНОВАЯ РАССЫЛКА
# ==========================================
async def daily_reminder_task():
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:
            users = load_json("users")
            msg = (
                f"🌅 <b>Доброе утро!</b>\n\n"
                f"{get_daily_content()['title']}:\n{get_daily_content()['text']}\n\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"💡 <b>Напоминание:</b>\n{get_next_reminder()}"
            )
            for u in users:
                try: await bot.send_message(u, msg)
                except: pass
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)

# ==========================================
# 6. ВЕБ-СЕРВЕР ДЛЯ RENDER
# ==========================================
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"✅ Web server started on port {port}")

# ==========================================
# 7. ЗАПУСК
# ==========================================
async def main():
    await start_web_server()
    asyncio.create_task(daily_reminder_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
