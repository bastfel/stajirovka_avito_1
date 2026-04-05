import re
import pytest
from playwright.sync_api import Page, expect

T = 15000 

def test_price_range_filter(page: Page):
    page.goto("/", wait_until="commit", timeout=60000)
    page.get_by_placeholder("От").fill("1000")
    page.get_by_placeholder("До").fill("100000")
    page.keyboard.press("Enter")
    
    cards = page.locator('div[class*="_card_"]')
    expect(cards.first).to_be_visible(timeout=T)
    
    for price_el in cards.locator('b').all():
        price_text = price_el.inner_text()
        if "₽" in price_text:
            price = int(re.sub(r'\D', '', price_text))
            assert 1000 <= price <= 100000, f"Баг: Цена {price} вне диапазона!"

def test_category_filter(page: Page):
    page.goto("/", wait_until="commit")
    category_select = page.locator('div:has(> label:text-is("Категория")) select, select').last
    category_select.select_option(index=1) 
    
    page.wait_for_timeout(2000)
    expect(page.locator('div[class*="_card_"]').first).to_be_visible(timeout=T)

def test_urgent_toggle(page: Page):
    page.goto("/", wait_until="commit")
    page.click('text="Только срочные"', timeout=T)
    page.wait_for_timeout(2000)
    
    expect(page.locator('text="Срочно"').first).to_be_visible()

def test_price_sorting(page: Page):
    page.goto("/", wait_until="commit")
    sort_select = page.locator('select').first
    sort_select.select_option(label="По убыванию")
    page.wait_for_timeout(3000)
    
    prices = []
    for price_el in page.locator('div[class*="_card_"] b').all()[:5]:
        prices.append(int(re.sub(r'\D', '', price_el.inner_text())))
    
    if len(prices) > 1:
        assert prices == sorted(prices, reverse=True), f"Баг сортировки: {prices}"

def test_statistics_timer(page: Page):
    page.goto("/statistics", wait_until="domcontentloaded")
    timer = page.locator('text=/\\d+:\\d+/').first
    expect(timer).to_be_visible(timeout=T)
    
    page.click('button:has-text("Заблок"), button:has-text("Пауза")')
    t_fixed = timer.inner_text()
    page.wait_for_timeout(2000)
    assert timer.inner_text() == t_fixed
    
    page.click('button:has-text("Старт"), button:has-text("Запуск")')
    page.wait_for_timeout(2500)
    assert timer.inner_text() != t_fixed
