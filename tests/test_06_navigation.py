"""Task 8 - core navigation & automation (+ matrix rows: Login, Navigation, Form Validation)."""
import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_valid_user(page, base_url, credentials):
    login = LoginPage(page, base_url).open()
    expect(page).to_have_title("Swag Labs")
    expect(page).to_have_url(re.compile(r"saucedemo\.com"))
    login.login(*credentials)
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(page.locator("[data-test='title']")).to_have_text("Products")


def test_navigation_back_forward_reload(inventory_page):
    page = inventory_page.page
    inventory_page.cart_link.click()
    expect(page).to_have_url(re.compile(r".*/cart\.html"))
    page.go_back()
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    page.go_forward()
    expect(page).to_have_url(re.compile(r".*/cart\.html"))
    page.reload()
    expect(page).to_have_url(re.compile(r".*/cart\.html"))
    expect(page.locator("[data-test='title']")).to_have_text("Your Cart")


@pytest.mark.regression
@pytest.mark.parametrize(
    "user, pwd, message",
    [
        ("", "", "Username is required"),
        ("someone", "", "Password is required"),
        ("not_a_user", "wrong", "do not match"),
    ],
    ids=["empty-form", "missing-password", "bad-credentials"],
)
def test_form_validation_messages(page, base_url, user, pwd, message):
    login = LoginPage(page, base_url).open()
    login.login(user, pwd)
    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text(message)
    expect(page).not_to_have_url(re.compile(r"inventory"))
