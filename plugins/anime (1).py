# Use Your Own Api In This or Face thousand's of error

# Created By AniShin (@iTz_Anayokoji)
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot

# Function to fetch anime data from the API
def fetch_anime_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

# Function to get top anime
def get_top_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    data = fetch_anime_data(url)
    top_anime_list = data.get("data", [])
    return top_anime_list

# Function to get weekly anime
def get_weekly_anime():
    url = "https://api.jikan.moe/v4/seasons/now"
    data = fetch_anime_data(url)
    weekly_anime_list = data.get("data", [])
    return weekly_anime_list

# Function to search for anime
def search_anime(query):
    url = f"https://api.jikan.moe/v4/anime?q={query}&page=1"
    data = fetch_anime_data(url)
    search_results = data.get("data", [])
    return search_results

# Cool font style for the anime title
def style_anime_title(title):
    return f"**{title}**".replace("A", "𝔸").replace("B", "𝔹").replace("C", "ℂ").replace("D", "𝔻").replace("E", "𝔼").replace("F", "𝔽").replace("G", "𝔾").replace("H", "ℍ").replace("I", "𝕀").replace("J", "𝕁").replace("K", "𝕂").replace("L", "𝕃").replace("M", "𝕄").replace("N", "ℕ").replace("O", "𝕆").replace("P", "ℙ").replace("Q", "ℚ").replace("R", "ℝ").replace("S", "𝕊").replace("T", "𝕋").replace("U", "𝕌").replace("V", "𝕍").replace("W", "𝕎").replace("X", "𝕏").replace("Y", "𝕐").replace("Z", "ℤ")

# Get an emoji based on the anime title
def get_anime_emoji(title):
    emojis = ["✨", "🌟", "💫", "🔥", "💥", "🌸", "🎉", "🎇", "🎆", "⚡"]
    return emojis[hash(title) % len(emojis)]

# Handler to display top anime with buttons
@Bot.on_message(filters.command('top') & filters.private)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = get_top_anime()
        if not top_anime_list:
            await message.reply("No top anime found at the moment.")
            return

        keyboard = [[InlineKeyboardButton(f"{style_anime_title(anime.get('title'))}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in top_anime_list[:10]]
        keyboard.append([InlineKeyboardButton("✖️✨ 𝕮𝖑𝖔𝖘𝖊 ✨✖️", callback_data='close')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "✨ *Top Anime* ✨",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Handler to display weekly anime with buttons
@Bot.on_message(filters.command('weekly') & filters.private)
async def weekly_anime_command(client: Client, message: Message):
    try:
        weekly_anime_list = get_weekly_anime()
        if not weekly_anime_list:
            await message.reply("No weekly anime found at the moment.")
            return

        keyboard = [[InlineKeyboardButton(f"{style_anime_title(anime.get('title'))}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in weekly_anime_list[:10]]
        keyboard.append([InlineKeyboardButton("✖️✨ 𝕮𝖑𝖔𝖘𝖊 ✨✖️", callback_data='close')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "📅 *Weekly Anime* 📅",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Handler to search for anime with buttons
@Bot.on_message(filters.command('search') & filters.private)
async def search_anime_command(client: Client, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply("Please provide a search query.")
        return

    try:
        search_results = search_anime(query)
        if not search_results:
            await message.reply("No anime found for the search query.")
            return

        keyboard = [[InlineKeyboardButton(f"{get_anime_emoji(anime.get('title'))} {anime.get('title')}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in search_results[:10]]
        keyboard.append([InlineKeyboardButton("✖️✨ 𝕮𝖑𝖔𝖘𝖊 ✨✖️", callback_data='close')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            f"🔍 *Search Results for '{query}'* 🔍",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Callback handler for detail and close button
@Bot.on_callback_query()
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    if callback_query.data.startswith("detail_"):
        mal_id = callback_query.data.split("_")[1]
        url = f"https://api.jikan.moe/v4/anime/{mal_id}"
        data = fetch_anime_data(url)

        if data:
            anime = data.get("data", {})
            details = (
                f"**Title:** {style_anime_title(anime.get('title'))}\n"
                f"**Type:** {anime.get('type')}\n"
                f"**Episodes:** {anime.get('episodes')}\n"
                f"**Score:** {anime.get('score')}\n"
                f"**Synopsis:** {anime.get('synopsis')}\n"
                f"**URL:** [MyAnimeList]({anime.get('url')})"
            )
            await callback_query.message.edit_text(
                details,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✖️✨ 𝕮𝖑𝖔𝖘𝖊 ✨✖️", callback_data='close')]]
                ),
                parse_mode=ParseMode.MARKDOWN
            )
    elif callback_query.data == 'close':
        await callback_query.message.delete()
# This script is not so cool if you see my eyes then you will understand how diffucult is it to make 
# If Any one will betray me i will not make him my enemy cause i want to make friend i am alone right now
# Also if this happen rembember Karma do exist

