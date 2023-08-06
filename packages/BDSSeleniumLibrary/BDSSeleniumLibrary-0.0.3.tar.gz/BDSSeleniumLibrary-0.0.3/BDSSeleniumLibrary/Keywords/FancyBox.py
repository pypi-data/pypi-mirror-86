from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn

class FancyBoxKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)
        self.xpath = '//*[contains(@class, "fancybox-opened")]'
        self.text = 'fancy box'

    @keyword
    def wait_until_page_contains_fancy_box(self, timeout=None, error=None):
        self.wait_until_page_contains_element(self.text, self.xpath, timeout, error)

    @keyword
    def wait_until_page_does_not_contain_fancy_box(self, timeout=None, error=None):
        self.wait_until_page_does_not_contain_element(self.text, self.xpath, timeout, error)

    @keyword
    def wait_until_fancy_box_is_not_visible(self, timeout=None, error=None):
        self.wait_until_element_is_not_visible(self.text, self.xpath, timeout, error)

    @keyword
    def wait_until_page_contains_close_btn_of_fancy_box(self, timeout=None, error=None):
        self.ctx.keywords['select_window']('MAIN', 120)
        self.wait_until_page_contains_element(self.text, '//*[@class="fancybox-item fancybox-close"]', timeout, error)

    @keyword
    def select_fancy_box(self):
        self.ctx.keywords['select_window']('MAIN', 120)
        self.wait_until_page_contains_fancy_box(120)
        xpath = '//iframe[@class = "fancybox-iframe"]'
        has_iframe = BuiltIn().run_keyword_and_return_status('wait_until_page_contains_element', 'xpath={0}'.format(xpath), 120)
        if has_iframe:
            self.ctx.keywords['select_frame']('xpath={0}'.format(xpath))

    @keyword
    def click_close_btn_of_fancy_box(self):
        self.wait_until_page_contains_close_btn_of_fancy_box(120, 'Không tìm thấy close button của fancy box')
        self.click_clickable_element_with_xpath('//*[@class="fancybox-item fancybox-close"]')
        self.ctx.keywords['select_window']('MAIN', 120)
