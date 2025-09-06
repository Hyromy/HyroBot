import logging
import logging.handlers

def set_logger():
    """Set up the logger for the bot."""

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename = 'discord.log',
        encoding = 'utf-8',
        maxBytes = 32 * 1024 * 1024,
        backupCount = 5,
    )

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style = '{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
