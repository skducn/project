from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.jd.com/")
    page = context.new_page()

    page.goto("https://www.baidu.com/")

    page.locator("input[name=\"wd\"]").fill("qtp")

    page.locator("input[name=\"wd\"]").press("Enter")
    page.wait_for_url("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=qtp&fenlei=256&rsv_pq=0xface455c0029c097&rsv_t=9539kogfX2tYphq0tNqq8nxD8joJeHb8wvLc463bHvD4sH9Jgghellr86ZJf&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=3&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=2270&rsv_sug4=2270")

    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="qtp，自动测试工具，百度百科").click()
    page1 = popup_info.value
    page.wait_for_url("https://baike.baidu.com/item/QTP/2590838?fr=aladdin")

    page.close()

    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
