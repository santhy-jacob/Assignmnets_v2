"""Task 14 - collections: count, first, last, nth, iteration (+ matrix row: Search/sort)."""
import re

from playwright.sync_api import expect

from utils.data_loader import load_json

DATA = load_json("products.json")


def test_collection_handling(inventory_page):
    items = inventory_page.items
    print("item count:", items.count())
    expect(items).to_have_count(DATA["item_count"])
    expect(inventory_page.names.first).to_have_text(DATA["first_item"])
    expect(inventory_page.names.last).to_have_text(DATA["last_item"])
    expect(inventory_page.names.nth(2)).to_be_visible()
    for i, name in enumerate(inventory_page.names.all_inner_texts()):
        print(i, name)
    inventory_page.items.nth(1).get_by_role("button", name="Add to cart").click()
    expect(inventory_page.cart_badge).to_have_text("1")


def test_sort_products_by_price(inventory_page):
    inventory_page.sort_by("Price (low to high)")
    expect(inventory_page.names.first).to_have_text(DATA["cheapest_item"])
    prices = [float(re.sub(r"[^\d.]", "", p)) for p in inventory_page.prices.all_inner_texts()]
    assert prices == sorted(prices)
