from loguru import logger


def configure_logging() -> None:
    # Keep logging simple and deterministic for auditing.
    logger.remove()
    logger.add(
        "agent.log",
        rotation="1 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}",
    )

