# HyroBot
Discord bot desarrollado en [discord.py](https://discordpy.readthedocs.io/en/stable)

_HyroBot depende de [HyroApi](https://github.com/Hyromy/HyroApi) o alguna otra api para funcionar correctamente_

## Requisitos
- Python 3.12
- pip

## Estructura del proyecto
```sh
cogs/               # módulos del bot
utils/              # utilidades
main.py             # script de ejecución
requirements.txt    # dependencias
```

## Variables de entorno
```sh
# api
API_URL="url de api"                   # obligatorio para consultas externas

# debug
DEBUG="True"

# discord
DISCORD_BOT_TOKEN="TOKEN"              # obligatorio para DEBUG="FALSE"
DEBUG_DISCORD_BOT_TOKEN="TOKEN"        # obligatorio
HOME_GUILD="ID servidor de discord"    # obligatorio
OWNER_ID="ID usuario de discord"       # opcional para algunos comandos

# auto deploy (cybrancee)
PTERODACTYL_API_KEY="api key"
SERVER_ID="id server"
```

## Instalación
1. Crear y activar un entorno virtual:
    ```sh
    python -m venv env
    env\Scripts\activate  # Windows
    ```

2. Instalar dependencias
    ```sh
    pip install -r requirements.txt
    ```    

## Despliegue
```sh
python main.py
```

## Licencia
[Licencia MIT](LICENSE)
