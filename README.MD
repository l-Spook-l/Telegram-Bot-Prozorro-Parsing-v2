# Telegram Bot for Prozorro Parsing

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blueviolet)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=python)
![aiofiles](https://img.shields.io/badge/aiofiles-Async_File_Operations-yellowgreen)
![aiosmtplib](https://img.shields.io/badge/aiosmtplib-Async_Email-yellow)
![aiohttp](https://img.shields.io/badge/aiohttp-Async_HTTP-blue)

## Description

The bot is designed for convenient and swift retrieval of tender information directly within Telegram from the Prozorro system. Users can specify parameters to search for tenders, and the bot will send daily updates on the found tenders to the user's email.

## What's New in Version 2

In the second version of the bot, several improvements and new features have been added:

- **Migration to aiogram 3.x:**
  - The bot has been upgraded from aiogram version 2 to version 3, bringing better performance and new features.
- **Advanced Filter Modification:**
  - Users can now modify existing filters directly within the bot.
- **Step Back Feature:**
  - While creating a filter, users can now return to previous steps to make adjustments.
- **Bug Fixes:**
  - Fixed issues that allowed incorrect time and email inputs.
- **Improved Asynchronous Messaging:**
  - Added asynchronous message sending for cases where multiple filters are triggered at the same time.
- **Enhanced Code Structure:**
  - The codebase has been refactored for better readability and maintainability.

## Functionality

- Search for tenders based on specified parameters (e.g., keywords, region, tender type, etc.).
- Subscription to daily updates of found tenders via email.
- Modify existing filters and correct inputs while creating new filters.

## Usage

1. **Bot Startup:**
   - Install all dependencies, launch the bot on your server or locally.
   - Provide the Telegram API token and mail sending parameters.

2. **Interacting with the Bot:**
   - Users can use bot commands to search for tenders, subscribe to daily updates, and modify existing filters.
   - An example of a filter for tenders
   - - ДК021:2015: 09300000-2"
   - - Статус: період уточнень
   - - Вид закупівлі: спрощена закупівля"
   - - Регіон: київська область"
   - - Час відправлення: 18:08"

## Installation Requirements

- Python 3.x
- Installed packages from `requirements.txt`

## Developers

- https://github.com/l-Spook-l

## Contact

If you have any questions or suggestions for improving the project, please contact uaspookua@gmail.com.
