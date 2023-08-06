from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections

class AdvancedDropdownKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def get_advanced_dropdown_container_by_title_xpath(self, text, index=1):
        xpath = 'xpath=(//div[contains(@class, "advance-select-box") and .//*[(local-name() = "span" and text() = "{0}") or (local-name() = "input" and @placeholder = "{0}")]])[{1}]'.format(text, index)
        count = self.get_element_count(xpath)
        if (count > 0):
            return xpath
        return ''
    
    def get_advanced_dropdown_container_by_first_value_xpath(self, text, index=1):
        xpath = 'xpath=(//div[contains(@class, "advance-select-options") and .//*[(local-name() = "li" and text() = "{0}")]])[{1}]'.format(text, index)
        count = self.get_element_count(xpath)
        if count > 0:
            ddlid = self.get_element_attribute(xpath, 'ddlid')
            return ddlid
        return ''

    def get_advanced_dropdown_container_by_label_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'div', 'contains(@class,"advance-select-box")', 4, index)

    def get_advanced_dropdown_container_xpath(self, text, index=1):
        container_locators = []
        container_locator = self.get_advanced_dropdown_container_by_title_xpath(text, index)
        if container_locator == '':
            container_locators.append(container_locator)

        container_locator = self.get_advanced_dropdown_container_by_first_value_xpath(text, index)
        if container_locator == '':
            container_locators.append(container_locator)

        container_locator = self.get_advanced_dropdown_container_by_label_xpath(text, index)
        if container_locator == '':
            container_locators.append(container_locator)

        return container_locators[0]

    #region contains

    @keyword
    def wait_until_page_contains_advanced_dropdown(self, text, timeout=None, error=None, index=1):
        xpath = '((//*[normalize-space(.) = "{0}" or (@placeholder = "{0}" and local-name() = "input")]/ancestor::*[position() < 4]//div)[contains(@class,"advance-select-box")] | //div[contains(@class, "advance-select-options") and .//li[text() = "{0}"]])'.format(text)
        self.wait_until_page_contains_element(text, xpath, timeout, error)

    @keyword
    def wait_until_page_does_not_contain_advanced_dropdown(self, text, timeout=None, error=None, index=1):
        xpath = '((//*[normalize-space(.) = "{0}" or (@placeholder = "{0}" and local-name() = "input")]/ancestor::*[position() < 4]//div)[contains(@class,"advance-select-box")] | //div[contains(@class, "advance-select-options") and .//li[text() = "{0}"]])'.format(text)
        self.wait_until_page_does_not_contain_element(text, xpath, timeout, error)

    #endregion

    #region value

    def get_value_of_advenced_dropdown_id(self, text, index=1):
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        hdd_value = self.get_element_attribute('xpath=//div[@ddlib="{0}"]'.format(id), 'hddvalue')
        selected_id = self.get_element_attribute('id={0}'.format(hdd_value), 'value')
        return selected_id        

    def get_value_of_advenced_dropdown_text(self, text, index=1):
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        hdd_value = self.get_element_attribute('xpath=//div[@ddlib="{0}"]'.format(id), 'hddvalue')
        selected_id = self.get_element_attribute('id={0}'.format(hdd_value), 'value')
        selected_value = self.get_element_attribute('xpath={0}//li[@vl="{1}"]'.format(container_xpath, selected_id), 'innerHtml')
        return selected_value

    @keyword('Value Of Advanced Dropdown Should Be (Id)')
    def value_of_advanced_dropdown_should_be_id(self, text, expected, message=None, ignore_case=False, index=1):
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        hdd_value = self.get_element_attribute('xpath=//div[@ddlib="{0}"]'.format(id), 'hddvalue')
        selected_id = self.get_element_attribute('id={0}'.format(hdd_value), 'value')
        BuiltIn().should_be_equal_as_strings(selected_id, expected, message, ignore_case)

    @keyword('Value Of Advanced Dropdown Should Be (Text)')
    def value_of_advanced_dropdown_should_be_text(self, text, expected, message=None, ignore_case=False, index=1):
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        hdd_value = self.get_element_attribute('xpath=//div[@ddlib="{0}"]'.format(id), 'hddvalue')
        selected_id = self.get_element_attribute('id={0}'.format(hdd_value), 'value')
        self.text_of_element_should_be('xpath={0}//li[@vl="{1}"]'.format(container_xpath, selected_id), expected, message, ignore_case)

    @keyword('Value Of Advanced Dropdown Should Contain (Text)')
    def value_of_advanced_dropdown_should_contain_text(self, text, expected, message=None, ignore_case=False, index=1):
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        hdd_value = self.get_element_attribute('xpath=//div[@ddlib="{0}"]'.format(id), 'hddvalue')
        selected_id = self.get_element_attribute('id={0}'.format(hdd_value), 'value')
        self.ctx.keywords['element_should_contain']('xpath={0}//li[@vl="{1}"]'.format(container_xpath, selected_id), expected, message, ignore_case)        

    #endregion

    #region visiable

    @keyword
    def wait_until_advanced_dropdown_is_not_visible(self, text, timeout=None, error=None, index=1):
        xpath = self.get_advanced_dropdown_container_xpath(text, index)
        self.wait_until_element_is_not_visible(text, xpath, timeout, error)

    @keyword
    def wait_until_advanced_dropdown_is_visible(self, text, timeout=None, error=None, index=1):
        xpath = self.get_advanced_dropdown_container_xpath(text, index)
        self.wait_until_element_is_visible(text, xpath, timeout, error)

    @keyword
    def advanced_dropdown_should_be_visible(self, text, message=None, index=1):
        xpath = self.get_advanced_dropdown_container_xpath(text, index)
        self.element_should_be_visible(text, xpath, message)

    @keyword
    def advanced_dropdown_should_not_be_visible(self, text, message=None, index=1):
        xpath = self.get_advanced_dropdown_container_xpath(text, index)
        self.element_should_not_be_visible(text, xpath, message)

    #endregion

    #region actions

    def wait_until_advanced_dropdown_is_useable(self, text, timeout=None, error=None, index=1):
        self.wait_until_page_contains_advanced_dropdown(text, timeout, error, index)

    def get_advanced_dropdown_items_text(self, text, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        list_items = self.ctx.keywords['get_webelements']('//div[@ddlid="{0}"]/ul[contains(@class, "advance-options")]/li'.format(id))
        result = []
        for item in list_items:
            temp = self.get_element_attribute(item, innerHTML)
            result.append(temp)

        return result

    def get_value_of_advanced_dropdown_id(self, text, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        container_xpath = self.get_advanced_dropdown_container_xpath(text, index)
        return self.get_element_attribute('{0}/input'.format(container_xpath), 'value')

    def open_advanced_popup(self, container_locator, index=1):
        self.execute_script('document.evaluate(''{0}/span[contains(@class, "select-text")]'', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'.format(container_locator))

    @keyword
    def select_advanced_dropdown(self, text, text_of_option, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        container_locator = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        self.open_advanced_popup(container_locator)
        li_locator = '//div[@ddlid="{0}"]/ul[contains(@class, "advance-options")]/li[contains(text(), "{1}")]',format(id, text_of_option)
        self.wait_until_page_contains_element(text_of_option, 'xpath={0}'.format(li_locator), 120, None)
        if self.get_element_count('xpath=//div[@ddlid="{0}"]/ul[contains(@class, "advance-options")]/li[normalize-space(.)="{1}"]'.format(id, text_of_option)) > 0:
            self.click_clickable_element_with_xpath('//div[@ddlid="{0}"]/ul[contains(@class, "advance-options")]/li[normalize-space(.)="{1}"]''.format(id, text_of_option)')
        else:
            self.click_clickable_element_with_xpath(li_locator)

    @keyword
    def set_min_value_of_advanced_dropdown(self, text, value, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        container_locator = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        self.open_advanced_popup(container_locator)
        min_value_input_locator = '(//div[@ddlid="{id}"]//input[contains(@class, "min-value")])[1]'.format(id)
        self.ctx.keywords['input_text'](min_value_input_locator, value)
        self.ctx.keywords['press_keys'](None, 'ENTER')

    @keyword
    def set_max_value_of_advanced_dropdown(self, text, value, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        container_locator = self.get_advanced_dropdown_container_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(container_xpath), 'id')
        self.open_advanced_popup(container_locator)
        min_value_input_locator = '(//div[@ddlid="{id}"]//input[contains(@class, "max-value")])[1]'.format(id)
        self.ctx.keywords['input_text'](min_value_input_locator, value)
        self.ctx.keywords['press_keys'](None, 'ENTER')

    @keyword('Advanced Dropdown Items Should Be Equal (Static Array)')
    def advanced_dropdown_items_should_be_equal_static_array(self, text, value, index=1):
        self.wait_until_advanced_dropdown_is_useable(text, 120, None, index)
        list_elements = self.get_advanced_dropdown_items_text(text, index)
        Collections().lists_should_be_equal(list_elements, value)

    #endregion