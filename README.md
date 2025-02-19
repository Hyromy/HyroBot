# HyromyBot
HyromyBot es un bot de discord programado en Python con la libreria [discord.py](https://discordpy.readthedocs.io/en/stable/).

Por el momento, el projecto no tiene un interés o dirección particular a corto, medio o largo plazo. Sin hembargo se buscar hacer un aporte (aunque sea mínimo) a la comunidad de bots de discord y, en la medida de lo posible servir como apoyo, inspiración o ejemplo para futuros desarrollos y desarrolladores.

> [!IMPORTANT]
> La presente documentación esta sujeta a cambios

## INSTALACIÓN

### Clonar repositorio

Puedes clonar este repositorio con el siguiente comando

```bash
git clone https://github.com/Hyromy/HyromyBot.git
```

---

### Variables de entorno

Por seguridad el bot esta configurado con variables de entorno las cuales no se incluyen en el repositorio.

Para que el bot funcione es necesario declarar `DISCORD_BOT_TOKEN` con un token válido. Puedes conseguir tu token en [Discord Developer Portal](https://discord.com/developers).

Las variables de entorno deberán estar guardadas en un archivo llamado `.env` para su funcionamiento, Este archivo deberá de verse así:

```env
DISCORD_BOT_TOKEN="Your Token"
```

> [!WARNING]
> El bot usa más variables de entorno por lo que la usencia de ellas puede provocar que el funcionamiento del bot sea parcial o reducido

---

### Entorno virtual (opcional)

Si bien, no es necesario aislar el projecto en un entorno virtual es recomendable hacerlo para evitar problemas con otras dependencias o sobrecargar tus dependencias globales de Python.

Puedes crear un entorno virtual con el siguiente comando

```bash
python -m venv env
```

Python creará una carpeta llamada `env` haciendo que el proyecto este aislado de otros.

---

### Dependencias

El projecto usa varias dependencias las cuales se encuentran en el archivo `requeriments.txt` para instalarlas escribe el siguiente comando

```bash
python install -r requirements.txt
```

esto instalará todas las dependencias necesarias para el funcionamiento del bot

---

### Verificación

para comprobar que el bot funciona correctamente ejecuta el archivo `main.py` en tu entorno de desarrollo o escribe el siguiente comando para comenzar con la ejecución del bot

```bash
python main.py
```

En la terminal de tu entorno de desarrollo apareceran algunos mensajes sobre algunos procesos en ejecución. El bot estará listo cuando el último mensaje sea un [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) azul.

## USO

Por defecto el bot usa el prefijo de comandos `.` por lo que en el canal donde el bot tenga acceso, se recomienda escribir el comando `ping` para verificar que el bot este en funcionamiento.

> [!TIP]
> Si alguna vez olvidas el prefijo puedes mencionar al bot seguido de la palabra `prefix` para que este muestre su prefijo
