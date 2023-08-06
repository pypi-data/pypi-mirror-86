from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class CheckBoxKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def get_check_box_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'input', '@type="checkbox"', 4, index)

    def get_value_of_check_box_bool(self, text, index=1):
        xpath = self.get_check_box_xpath(text, index)
        checked = self.get_element_attribute('xpath={0}'.format(xpath), 'checked')
        return checked == 'true'

    @keyword
    def wait_until_page_contains_check_box(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'input', '@type="checkbox"', 4, timeout, error)

    @keyword
    def wait_until_check_box_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, self.get_check_box_xpath, timeout, error)

    @keyword
    def wait_until_check_box_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_enabled(text, self.get_check_box_xpath, timeout, error)

    @keyword
    def wait_until_check_box_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_check_box(text, timeout)
        self.wait_until_check_box_is_visible(text, timeout, None, index)
        self.wait_until_check_box_is_enabled(text, timeout, None, index)

    @keyword
    def click_check_box(self, text, index=1):
        self.wait_until_check_box_is_useable(text, 120, index)
        self.click_clickable_element_with_xpath(self.get_check_box_xpath(text, index))

    @keyword
    def uncheck_check_box(self, text, index=1):
        if self.get_value_of_check_box_bool(text, index):
            self.click_check_box(text, index)

    @keyword
    def check_check_box(self, text, index=1):
        if self.get_value_of_check_box_bool(text, index) == False:
            self.check_check_box(text, index)