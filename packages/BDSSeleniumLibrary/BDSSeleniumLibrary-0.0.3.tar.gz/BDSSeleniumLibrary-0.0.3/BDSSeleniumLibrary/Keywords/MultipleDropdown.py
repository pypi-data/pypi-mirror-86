from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.Collections import Collections
from robot.libraries.BuiltIn import BuiltIn

class MultipleDropdownKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    #region supports

    def wait_until_multiple_dropdown_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_multiple_dropdown(text, timeout, None)
        self.wait_until_multiple_dropdown_is_visible(text, timeout, None)
        self.wait_until_multiple_dropdown_is_enabled(text, timeout, None)

    def get_multiple_dropdown_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'select', '@multiple="true" or @multiple="multiple"', 4, index)

    #endregion

    #region enabled
    @keyword
    def wait_until_multiple_dropdown_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_page_contains_element(text, '{0}/following-sibling::div/button[@class="ms-choice"]'.format(self.get_multiple_dropdown_xpath(text, index)), timeout, error)

    @keyword
    def wait_until_multiple_dropdown_is_disabled(self, text, index=1):
        self.wait_until_page_contains_element(text, '{0}/following-sibling::div/button[@class="ms-choice disabled"]'.format(self.get_multiple_dropdown_xpath(text, index)), timeout, error)

    @keyword
    def multiple_dropdown_should_be_enabled(self, text, index=1):
        self.element_should_be_enabled('{0}/following-sibling::div/button[@class="ms-choice"]'.format(self.get_multiple_dropdown_xpath(text, index)))

    @keyword
    def multiple_dropdown_should_be_disabled(self, text, index=1):
        self.element_should_be_enabled('{0}/following-sibling::div/button[@class="ms-choice disabled"]'.format(self.get_multiple_dropdown_xpath(text, index)))

    #endregion


    #region contains
    @keyword
    def wait_until_page_contains_multiple_dropdown(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'textarea', '1=1', 4, timeout, error)
    
    @keyword
    def wait_until_page_does_not_contain_multiple_dropdown(self, text, timeout=None, error=None):
        self.wait_until_page_does_not_contain_htmlelement_being_near_text(text, 'textarea', '1=1', 4, timeout, error)

    #endregion

    #region visible
    @keyword
    def wait_until_multiple_dropdown_is_not_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_not_visible(text, '{0}/following-sibling::div[@class="ms-parent"]'.format(self.get_multiple_dropdown_xpath(text, index)), timeout, error)

    @keyword
    def wait_until_multiple_dropdown_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, '{0}/following-sibling::div[@class="ms-parent"]'.format(self.get_multiple_dropdown_xpath(text, index)), timeout, error)

    @keyword
    def multiple_dropdown_should_be_visible(self, text, message=None, index=1):
        self.element_should_be_visible(text, '{0}/following-sibling::div[@class="ms-parent"]'.format(self.get_multiple_dropdown_xpath(text, index)), message)

    @keyword
    def multiple_dropdown_should_not_be_visible(self, text, message=None, index=1):
        self.element_should_not_be_visible(text, '{0}/following-sibling::div[@class="ms-parent"]'.format(self.get_multiple_dropdown_xpath(text, index)), message)

    #endregion
    
    #region value

    def get_value_of_multiple_dropdown_id(self, text, index=1):
        xpath = self.get_multiple_dropdown_xpath(text, index)
        title = self.get_element_attribute('xpath={0}/following-sibling::div/button[@class="ms-choice"]'.format(xpath), title)
        result = []
        words = title.split(',')
        for word in words:
            word = word.strip()
            result.append(word)
        return result

    def get_value_of_multiple_dropdown_text(self, text, index=1):
        xpath = self.get_multiple_dropdown_xpath(text, index)
        title = self.get_element_attribute('xpath={0}/following-sibling::div/button[@class="ms-choice"]'.format(xpath), title)
        result = []
        words = title.split(',')
        for word in words:
            word = word.strip()
            value = self.get_element_attribute('xpath={0}/following-sibling::div/div[@class="ms-drop bottom"]/ul/li/label[@title="{1}"]/input'.format(xpath, word), value)
            result.append(value)
        return result

    @keyword('Value Of Multiple Dropdown Should Be (Id, Static Array)')
    def value_of_multiple_dropdown_should_be_id(self, text, expected, message=None, index=1):
        list_element = self.get_value_of_multiple_dropdown_id(text, index)
        Collections().lists_should_be_equal(list_element, expected, message)

    @keyword('Value Of Multiple Dropdown Should Be (Text, Static Array)')
    def value_of_multiple_dropdown_should_be_text(self, text, expected, message=None, index=1):
        list_element = self.get_value_of_multiple_dropdown_text(text, index)
        Collections().lists_should_be_equal(list_element, expected, message)

    #endregion


    #region actions

    def wait_until_multiple_dropdown_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_multiple_dropdown(text, timeout)

    def get_multiple_dropdown_items_text(self, text, index=1):
        self.wait_until_multiple_dropdown_is_useable(text, 120, None, index)

    @keyword
    def select_multiple_dropdown(self, text, text_of_option, index):
        self.wait_until_multiple_dropdown_is_useable(text, 120, None, index)
        xpath = self.get_multiple_dropdown_xpath(text, index)
        self.wait_until_page_contains_element(text, '{0}/..//ul/li/label[@title="{1}"]/input'.format(xpath, text_of_option), 120)
        input_js = 'document.evaluate(''{0}/..//ul/li/label[@title="{1}"]/input'', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'.format(xpath, text_of_option)
        condition_js = '!{0}.checked'.format(input_js)
        task_js = '{0}.click()'.format(input_js)
        self.execute_script('if({0})'.format(condition_js) + '{' + '{1}'.format(task_js) + '}')
        
    @keyword
    def unselect_multiple_dropdown(self, text, text_of_option, index):
        self.wait_until_multiple_dropdown_is_useable(text, 120, None, index)
        xpath = self.get_multiple_dropdown_xpath(text, index)
        self.wait_until_page_contains_element(text, '{0}/..//ul/li/label[@title="{1}"]/input'.format(xpath, text_of_option), 120)
        input_js = 'document.evaluate(''{0}/..//ul/li/label[@title="{1}"]/input'', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'.format(xpath, text_of_option)
        condition_js = '{0}.checked'.format(input_js)
        task_js = '{0}.click()'.format(input_js)
        self.execute_script('if({0})'.format(condition_js) + '{' + '{1}'.format(task_js) + '}')

    @keyword
    def title_multiple_dropdown_should_be(self, text, expected, message=None, ignore_case=False, index=1):
        self.wait_until_multiple_dropdown_is_useable(text, 120, None, index)
        xpath = self.get_multiple_dropdown_xpath(text, index)
        xpath = '{0}/option[@value="" and normalize-space(.) = "{1}"]'.format(xpath, expected)
        self.ctx.keywords['element_should_contain'](xpath, expected, message, ignore_case)

    @keyword('Multiple Dropdown Items Should Be Equal (Text, Static Array)')
    def multiple_dropdown_items_should_be_equal_text_static_array(self, text, value, index=1):
        self.wait_until_multiple_dropdown_is_useable(text, 120, None, index)
        list_element = self.get_multiple_dropdown_items_text_list_of_string(text, index)
        Collections().lists_should_be_equal(list_element, value)

    #endregion