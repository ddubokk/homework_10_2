import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("mastercard 7158300734726758", "Mastercard 7158 30** **** 6758"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 64686473678894779589", "Счет **9589"),
    ],
)
def test_mask_account_card_valid(info: str, expected: str) -> None:
    """Тестирование маскирования разных типов карт и счетов."""
    assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "info, expected_error",
    [
        ("", "Ошибка: некорректный формат ввода!"),
        ("VisaPlatinum7000792289606361", "Ошибка: некорректный формат ввода!"),
        ("Личный счет 73654108430135874305", "Ошибка: для счета должно быть передано строго два слова!"),
    ],
)
def test_mask_account_card_format_errors(info: str, expected_error: str) -> None:
    """Проверка возврата текстовых ошибок при нарушении формата строки."""
    assert mask_account_card(info) == expected_error


@pytest.mark.parametrize(
    "invalid_number_info",
    [
        "Visa Platinum 1234",
        "Счет 12",
        "Maestro abcdefghijklmnop",
    ],
)
def test_mask_account_card_invalid_numbers(invalid_number_info: str) -> None:
    """Проверка выброса ValueError при некорректном номере карты или счета."""
    with pytest.raises(ValueError):
        mask_account_card(invalid_number_info)


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2023-12-31", "31.12.2023"),
    ],
)
def test_get_date_valid(date_str: str, expected: str) -> None:
    """Тестирование корректного преобразования даты в формат ДД.ММ.ГГГГ."""
    assert get_date(date_str) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "",
        "просто текст без даты",
        "11.03.2024",
        "2024-13-45T00:00:00",
    ],
)
def test_get_date_invalid(invalid_date: str) -> None:
    """Проверка выброса ValueError при отсутствии даты или неверном формате."""
    with pytest.raises(ValueError):
        get_date(invalid_date)
