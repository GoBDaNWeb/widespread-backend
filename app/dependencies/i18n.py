from fastapi import Header

SUPPORTED_LANGUAGES = {"ru", "en"}
DEFAULT_LANGUAGE = "ru"


def get_language(accept_language: str | None = Header(default=None)) -> str:
    """Определить язык ответа по заголовку Accept-Language.

    Принимает значения вида "ru-RU,ru;q=0.9,en;q=0.8" и возвращает первый
    поддерживаемый код языка ("ru" или "en"). Если ничего не подошло — DEFAULT_LANGUAGE.
    """
    if not accept_language:
        return DEFAULT_LANGUAGE

    for part in accept_language.split(","):
        code = part.split(";")[0].strip().lower()[:2]
        if code in SUPPORTED_LANGUAGES:
            return code

    return DEFAULT_LANGUAGE
