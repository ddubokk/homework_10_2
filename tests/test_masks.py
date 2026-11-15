import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Тестирование корректного маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "",
        "   ",
        "123456789012345",
        "12345678901234567",
        "700079228960636a",
        "Visa Platinum",
    ],
)
def test_get_mask_card_number_invalid(invalid_card: str) -> None:
    """Проверка выброса ValueError при некорректном номере карты или пустой строке."""
    with pytest.raises(ValueError, match="Номер карты должен состоять строго из 16 цифр"):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4305", "**4305"),
        ("1234", "**1234"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str) -> None:
    """Тестирование корректного маскирования номера счета."""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account",
    [
        "",
        "   ",
        "123",
        "7365410843013587430a",
        "Счет",
    ],
)
def test_get_mask_account_invalid(invalid_account: str) -> None:
    """Проверка выброса ValueError при коротком номере счета или наличии букв."""
    with pytest.raises(ValueError, match="Номер счета должен состоять из цифр и содержать не менее 4 символов"):
        get_mask_account(invalid_account)
