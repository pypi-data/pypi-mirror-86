from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class RadioKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def get_radio_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'input', '@type="radio" and ./following::*[position() < 3 and (normalize-space(.) = "{0}" or text())]'.format(text), 4, index)

    @keyword
    def wait_until_page_contains_radio(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'input', '@type="radio"', 4, timeout, error)

    @keyword
    def wait_until_radio_is_visible(self, text, timeout, error, index=1):
        self.wait_until_element_is_visible(text, self.get_radio_xpath(text, index), timeout, error)

    @keyword
    def wait_until_radio_is_enabled(self, text, timeout, error, index=1):
        self.wait_until_element_is_enabled(text, self.get_radio_xpath(text, index), timeout, error)
        
    @keyword
    def wait_until_radio_is_useable(self, text, timeout, error, index=1):
        self.wait_until_page_contains_radio(text, timeout, None)
        self.wait_until_radio_is_visible(text, timeout, None, index)
        self.wait_until_radio_is_enabled(text, timeout, None, index)
    
    @keyword
    def click_radio(self, text, index=1):
        self.wait_until_radio_is_useable(text, 120, None, index)
        self.click_clickable_element_with_xpath(self.get_radio_xpath(text, index))