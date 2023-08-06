from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class InputKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    #region supports

    def wait_until_input_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_input(text, timeout, None)
        self.wait_until_input_is_visible(text, timeout, None)
        self.wait_until_input_is_enabled(text, timeout, None)

    def get_input_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'input', '@type!="hidden"', 4, index)

    #endregion

    #region enabled
    @keyword
    def wait_until_input_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_enabled(text, self.get_input_xpath(text, index), timeout, error)

    @keyword
    def input_should_be_disabled(self, text, index=1):
        self.element_should_be_disabled(self.get_input_xpath(text, index))

    @keyword
    def input_should_be_enabled(self, text, index=1):
        self.element_should_be_enabled(self.get_input_xpath(text, index))

    #endregion


    #region contains
    @keyword
    def wait_until_page_contains_input(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'input', '@type!="hidden"', 4, timeout, error)
    
    @keyword
    def wait_until_page_does_not_contain_input(self, text, timeout=None, error=None):
        self.wait_until_page_does_not_contain_htmlelement_being_near_text(text, 'input', '@type!="hidden"', 4, timeout, error)

    #endregion

    #region visible
    @keyword
    def wait_until_input_is_not_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_not_visible(text, self.get_input_xpath(text, index), timeout, error)

    @keyword
    def wait_until_input_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, self.get_input_xpath(text, index), timeout, error)

    @keyword
    def input_should_be_visible(self, text, message=None, index=1):
        self.element_should_be_visible(text, self.get_input_xpath(text, index), message)

    @keyword
    def input_should_not_be_visible(self, text, message=None, index=1):
        self.element_should_not_be_visible(text, self.get_input_xpath(text, index), message)

    #endregion
    
    #region value

    @keyword
    def value_of_input_should_be(self, text, expected, message=None, index=1):
        self.textfield_value_should_be(text, self.get_input_xpath(text, index), expected, message)

    @keyword
    def value_of_input_should_contain(self, text, expected, message=None, index=1):
        self.textfield_should_contain(text, self.get_input_xpath(text, index), expected, message)

    #endregion


    #region actions

    @keyword
    def set_input(self, text, value, index=1):
        self.wait_until_input_is_useable(text, 120, index)
        xpath = self.get_input_xpath(text, index)
        self.ctx.keywords['input_text']('xpath={0}'.format(xpath), value)

    @keyword
    def click_input(self, text, value, index=1):
        self.wait_until_input_is_useable(text, 120, index)
        xpath = self.get_input_xpath(text, index)
        self.ctx.keywords['click_element']('xpath={0}'.format(xpath), value)

    @keyword('Get Value Of Input [String]')
    def get_value_of_input(self, text, index=1):
        self.wait_until_input_is_useable(text, 120, index)
        xpath = self.get_input_xpath(text, index)
        return self.get_element_attribute('xpath={0}'.format(xpath), 'value')

    #endregion
