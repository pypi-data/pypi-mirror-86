from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.Collections import Collections

class SingleDropdownKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    #region supports

    def wait_until_single_dropdown_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_single_dropdown(text, timeout, None)
        self.wait_until_single_dropdown_is_visible(text, timeout, None)
        self.wait_until_single_dropdown_is_enabled(text, timeout, None)

    def get_single_dropdown_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'select', 'not(@multiple="true") and not(@multiple="multiple")', 4, index)

    #endregion

    #region enabled
    @keyword
    def wait_until_single_dropdown_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_enabled(text, self.get_single_dropdown_xpath(text, index), timeout, error)

    @keyword
    def single_dropdown_should_be_disabled(self, text, index=1):
        self.element_should_be_disabled(self.get_single_dropdown_xpath(text, index))

    @keyword
    def single_dropdown_should_be_enabled(self, text, index=1):
        self.element_should_be_enabled(self.get_single_dropdown_xpath(text, index))

    #endregion


    #region contains
    @keyword
    def wait_until_page_contains_single_dropdown(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'single_dropdown', '@type!="hidden"', 4, timeout, error)
    
    @keyword
    def wait_until_page_does_not_contain_single_dropdown(self, text, timeout=None, error=None):
        self.wait_until_page_does_not_contain_htmlelement_being_near_text(text, 'single_dropdown', '@type!="hidden"', 4, timeout, error)

    #endregion

    #region visible
    @keyword
    def wait_until_single_dropdown_is_not_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_not_visible(text, self.get_single_dropdown_xpath(text, index), timeout, error)

    @keyword
    def wait_until_single_dropdown_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, self.get_single_dropdown_xpath(text, index), timeout, error)

    @keyword
    def single_dropdown_should_be_visible(self, text, message=None, index=1):
        self.element_should_be_visible(text, self.get_single_dropdown_xpath(text, index), message)

    @keyword
    def single_dropdown_should_not_be_visible(self, text, message=None, index=1):
        self.element_should_not_be_visible(text, self.get_single_dropdown_xpath(text, index), message)

    #endregion
    

    #region value

    def get_value_of_single_dropdown_id(self, text, index=1):
        xpath = self.get_single_dropdown_xpath(text, index)
        return self.get_element_attribute(
            'xpath={0}/option[@value="{id}"]'.format(
                xpath,
                self.get_element_attribute('xpath={0}'.format(self.get_single_dropdown_xpath(text, index)), 'value')
            ),
            'innerHTML'
        )
        
    def get_value_of_single_dropdown_text(self, text, index=1):
        return self.get_element_attribute('xpath={0}'.format(self.get_single_dropdown_xpath(text, index)), 'value')

    @keyword('Value Of Single Dropdown Should Be (Id)')
    def value_of_single_dropdown_should_be_id(self, text, expected, message=None, index=1):
        self.textfield_value_should_be(text, self.get_input_xpath(text, index), expected, message)

    @keyword('Value Of Single Dropdown Should Be (Text)')
    def value_of_single_dropdown_should_be_text(self, text, expected, message=None, index=1):
        xpath = self.get_input_xpath(text, index)
        value = self.get_element_attribute('xpath={0}'.format(xpath), 'value')
        self.text_of_element_should_be(text, '{0}/option[@value="{1}"]'.format(xpath, value), expected, message)

    @keyword('Value Of Single Dropdown Should Contain (Text)')
    def value_of_single_dropdown_should_contain_text(self, text, expected, message=None, index=1):
        xpath = self.get_input_xpath(text, index)
        value = self.get_element_attribute('xpath={0}'.format(xpath), 'value')
        self.ctx.keywords['element_should_contain'](text, 'xpath={0}/option[@value="{1}"]'.format(xpath, value), expected, message)

    #endregion


    #region actions

    def wait_until_single_dropdown_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_single_dropdown(text, timeout)

    @keyword('Select Single Dropdown (Id)')
    def select_single_dropdown_id(self, text, value, index):
        self.wait_until_page_contains_single_dropdown(text, 120)
        xpath = self.get_single_dropdown_xpath(text, index)
        self.wait_until_page_contains_element(text, '{0}/option[@value = "{0}"]'.format(xpath, value), 120)
        self.ctx.keywords['select_from_list_by_value']('xpath={0}'.format(xpath), value)

    @keyword('Select Single Dropdown (Text)')
    def select_single_dropdown_text(self, text, text_of_option, index):
        self.wait_until_page_contains_single_dropdown(text, 120)
        xpath = self.get_single_dropdown_xpath(text, index)
        self.wait_until_page_contains_element(text, '{0}/option[contains(text(), "{0}"]'.format(xpath, text_of_option), 120)
        self.ctx.keywords['select_from_list_by_value']('xpath={0}'.format(xpath), text_of_option)
        
    @keyword('Get Single Dropdown Items (Id) [List Of String]')
    def get_single_dropdown_items_text_list_of_string(self, text, index=1):
        self.wait_until_page_contains_single_dropdown(text, 120)
        xpath = self.get_single_dropdown_xpath(text, index)
        elements = self.ctx.keywords['get_webelements']('xpath={0}/option'.format(xpath))
        results = []
        for element in elements:
            text = self.get_element_attribute(item, value)
            results.append(text)
        return results

    @keyword('Get Single Dropdown Items (Text) [List Of String]')
    def get_single_dropdown_items_text_list_of_string(self, text, index=1):
        self.wait_until_page_contains_single_dropdown(text, 120)
        xpath = self.get_single_dropdown_xpath(text, index)
        elements = self.ctx.keywords['get_webelements']('xpath={0}/option'.format(xpath))
        results = []
        for element in elements:
            text = self.get_element_attribute(item, innerHTML)
            results.append(text)
        return results

    @keyword
    def title_single_dropdown_should_be(self, text, expected, message=None, ignore_case=False, index=1):
        self.wait_until_page_contains_single_dropdown(text, 120)
        xpath = self.get_single_dropdown_xpath(text, index)
        xpath = '{0}/option[contains(text(), "{1}")]'.format(xpath, expected)
        self.page_should_contain_element(text, xpath, message, loglevel, limit)

    @keyword('Single Dropdown Items Should Be Equal (Text, Static Array)')
    def single_dropdown_items_should_be_equal_text_static_array(self, text, value, index=1):
        self.wait_until_page_contains_single_dropdown(text, 120)
        list_element = self.get_single_dropdown_items_text_list_of_string(text, index)
        Collections().lists_should_be_equal(list_element, value)

    #endregion