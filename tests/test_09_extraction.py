"""Task 11 - extracting text and attributes."""
from playwright.sync_api import expect


def test_extract_text_and_attributes(page, base_url):
    page.goto(base_url)

    heading = page.locator(".login_logo").text_content()
    credentials_block = page.locator("[data-test='login-credentials']").inner_text()
    user = page.get_by_placeholder("Username")
    user.fill("extract_me")
    value = user.input_value()
    placeholder = user.get_attribute("placeholder")
    input_type = user.get_attribute("type")
    button_value = page.get_by_role("button", name="Login").get_attribute("value")

    print(f"heading={heading!r}\nplaceholder={placeholder!r} type={input_type!r} button_value={button_value!r}")
    print(f"credentials block ({len(credentials_block.splitlines())} lines):\n{credentials_block}")

    assert heading == "Swag Labs"
    assert value == "extract_me"
    assert placeholder == "Username"
    assert input_type == "text"
    assert button_value == "Login"
    assert "Accepted usernames" in credentials_block
    expect(user).to_have_attribute("placeholder", "Username")


def test_extract_href(inventory_page):
    href = inventory_page.page.locator("[data-test='social-linkedin']").get_attribute("href")
    assert href and href.startswith("https://")
