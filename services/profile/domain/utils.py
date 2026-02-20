from string import ascii_letters

RU_LETTERS_LOWERCASE = "йцукеёнгшщзхъфывапролджэячсмитьбю"
RU_LETTERS = RU_LETTERS_LOWERCASE + RU_LETTERS_LOWERCASE.upper()
OTHER_SYMBOLS = "- .',()"
VALID_NAME_SYMBOLS = ascii_letters + OTHER_SYMBOLS + RU_LETTERS


def is_empty_string(s: str) -> bool:
    return not s.strip()


