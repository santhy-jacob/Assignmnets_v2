from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.items = page.locator(".inventory_item")
        self.names = page.locator("[data-test='inventory-item-name']")
        self.prices = page.locator("[data-test='inventory-item-price']")
        self.sort = page.locator("[data-test='product-sort-container']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def sort_by(self, label: str) -> None:
        self.sort.select_option(label=label)

    def add_to_cart(self, index: int) -> None:
        self.items.nth(index).get_by_role("button", name="Add to cart").click()
