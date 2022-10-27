from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
    # context = browser.new_context(**playwright.devices["iPhone 12"])

    page = browser.new_page()

    page.goto("https://www.baidu.com/")

    page.screenshot(path=f'screenshot-.png')
    print(page.title())

    # page.locator("label").click()

    page.get_by_placeholder("输入搜索词").fill("你好")

    page.get_by_role("button", name="你好世界").click()
    page.wait_for_url("https://wappass.baidu.com/static/captcha/tuxing.html?&logid=8796723789916231123&ak=248b24c134a6b4f52ee85f8b9577d4a8&backurl=https%3A%2F%2Fm.baidu.com%2Ffrom%3D844b%2Fs%3Fword%3D%25E4%25BD%25A0%25E5%25A5%25BD%25E4%25B8%2596%25E7%2595%258C%26ts%3D0%26t_kt%3D0%26ie%3Dutf-8%26fm_kl%3D021394be2f%26rsv_iqid%3D2155910652%26rsv_t%3Da7c3qzNU7wJqrcr0DcQUfhWd59npNDFdm54QzgNSpxMESxPKeRYk57gQ6w%26sa%3Dis_7%26ms%3D1%26rsv_pq%3D2155910652%26tj%3D1%26rsv_sug4%3D1666833948886%26inputT%3D1666833954994%26sugid%3D139655590260482%26ss%3D100%26rq%3D%25E4%25BD%25A0%25E5%25A5%25BD%26from%3D844b%26vit%3Dfps&signature=7cc422e94092aa0130a41d5dbf4d7c2e&timestamp=1666833959")

    page.get_by_text("拖动左侧滑块使图片为正").click()

    page.get_by_text("拖动左侧滑块使图片为正").click()

    page.locator("#vcode-spin-bottom990").click()

    page.locator("#vcode-spin-bottom990").click()

    page.get_by_text("拖动左侧滑块使图片为正").click()

    page.locator("#vcode-spin-faceboder990").click()

    page.locator("#vcode-spin-bottom990").click()

    # ---------------------

    browser.close()


with sync_playwright() as playwright:
    run(playwright)



