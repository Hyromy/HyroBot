from datetime import datetime
from os import listdir
from os.path import isdir, join, sep
from re import search
from shutil import get_terminal_size

from colorama import init, Fore
from discord.ext.commands import Bot
from playwright.async_api import async_playwright
from pytz import timezone

init(autoreset = True)

async def header(Hyromy:Bot, font = "Isometric2"):
    html_id = "#taag_output_text"
    async with async_playwright() as pl:
        browser = await pl.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"https://patorjk.com/software/taag/#p=display&f={font}&t={Hyromy.user.name.upper()}")

        await page.wait_for_selector(html_id, timeout = 10000)

        element = await page.query_selector(html_id)
        text = await element.inner_text()

        result = await _prepare_header(text)
        await browser.close()

    return result

async def _prepare_header(text:str):
    text = text.split("\n")
    console_width = get_terminal_size().columns
    tz = timezone("America/Mexico_City")
    date = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")

    result = []
    result.append(f"\n{Fore.CYAN + ("[ Developed by: Hyromy ]").center(console_width, "=")}")
    result.extend(f"{Fore.CYAN}{line.center(console_width)}" for line in text)
    result.append(f"\n{Fore.CYAN + ("[ " + date + " ]").center(console_width, "=")}")
    
    return "\n".join(result)

async def load_cogs(Hyromy:Bot, dir = "cogs"):
    for item in listdir(dir):
        if not search(r"^__.*__.*$", item):
            if isdir(join(dir, item)):
                await load_cogs(Hyromy, join(dir, item))

            elif item.endswith(".py"):
                cog_path = f"{dir.replace(sep, ".")}.{item[:-3]}"
                print(f"Cargando: {cog_path}")                

                try:
                    await Hyromy.load_extension(cog_path)
                except Exception as e:
                    print("\033[F\033[K", end = "")
                    print(f"{Fore.RED}(X) No se pudo cargar el cog: {item[:-3]} -> {e}")
                else:
                    print("\033[F\033[K", end = "")
                    print(f"{Fore.GREEN}(OK) Cog cargado: {item[:-3]}")

    print()
    print(f"{len(Hyromy.cogs)} cogs cargados")
    print(f"{len(Hyromy.commands)} comandos cargados")
    print(f"{len(Hyromy.extra_events)} eventos cargados")
