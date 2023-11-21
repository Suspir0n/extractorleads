from playwright.sync_api import sync_playwright
from src.models.business_model import Business, BusinessList


def browser_chromium(search_google_maps: str, total_data: int, is_csv: int, is_excel: int):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto('https://www.google.com/maps', timeout=60000)
        page.wait_for_timeout(5000)

        page.locator('//input[@id="searchboxinput"]').fill(search_google_maps)
        page.wait_for_timeout(3000)

        page.keyboard.press('Enter')
        page.wait_for_timeout(5000)

        page.hover('(//div[contains(@class, "Nv2PK")])[1]')

        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            if page.locator('//div[contains(@class, "Nv2PK")]').count() >= total_data:
                listings = page.locator('//div[contains(@class, "Nv2PK")]').all()[:total_data]
                print(f'Total Scraped: {len(listings)}')
                break
            else:
                print(f'Currently Scraped: ', page.locator('//div[contains(@class, "Nv2PK")]').count())

        business_list = BusinessList()

        for listing in listings:
            listing.click()
            page.wait_for_timeout(5000)

            name_xpath = '//h1[contains(@class, "lfPIob")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_span_xpath = '//span[@role="img"]'

            business = Business()

            if page.locator(name_xpath).count() > 0:
                business.name = page.locator(name_xpath).inner_text()
            else:
                business.name = ''

            if page.locator(address_xpath).count() > 0:
                business.address = page.locator(address_xpath).inner_text()
            else:
                business.address = ''

            if page.locator(website_xpath).count() > 0:
                business.website = page.locator(website_xpath).inner_text()
            else:
                business.website = ''

            if page.locator(phone_number_xpath).count() > 0:
                business.phone_number = page.locator(phone_number_xpath).inner_text()
            else:
                business.phone_number = ''

            if listing.locator(reviews_span_xpath).count() > 0:
                business.reviews_average = float(listing.locator(reviews_span_xpath).get_attribute('aria-label').split()[0].replace(',', '.').strip())
                business.reviews_count = int(listing.locator(reviews_span_xpath).get_attribute('aria-label').split()[2].strip())
            else:
                business.reviews_average = ''
                business.reviews_count = ''

            business_list.business_list.append(business)

        if is_excel == 1:
            business_list.save_to_excel(f'{search_google_maps.split()[0]}-leads')

        if is_csv == 1:
            business_list.save_to_csv(f'{search_google_maps.split()[0]}-leads')

        browser.close()
