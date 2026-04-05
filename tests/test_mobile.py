import re
import pytest
from playwright.sync_api import Page, expect

def test_mobile_filters(mobile_page: Page):
    page = mobile_page
    page.goto("/", wait_until="domcontentloaded")
    
    page.select_option('select[class*="_filters__select"]', label="Недвижимость")
    
    page.fill('input[placeholder="От"]', "1000")
    page.fill('input[placeholder="До"]', "50000")
    
    page.press('input[placeholder*="Введите название"]', "Enter")
    page.wait_for_load_state("networkidle")

    expect(page.locator('div[class*="_card_"]').first).to_be_visible()

def test_mobile_urgent_toggle(mobile_page: Page):
    page = mobile_page
    page.goto("/", wait_until="domcontentloaded")
    
    # На фото видно переключатель "Только срочные" сверху. Кликаем по тексту.
    page.click('text="Только срочные"')
    
    page.wait_for_load_state("networkidle")
    
    # Проверяем наличие оранжевой плашки "Срочно"
    expect(page.locator('div[class*="_card_"] » text="Срочно"').first).to_be_visible()
