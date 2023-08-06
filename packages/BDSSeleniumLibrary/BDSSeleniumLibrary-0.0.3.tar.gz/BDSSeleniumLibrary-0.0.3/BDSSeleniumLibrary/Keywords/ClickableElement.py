from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String

class ClickableElementKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    #region supports
    
    def wait_until_clickable_element_is_useable(self, text, timeout=None, error=None, index=1):
        self.wait_until_page_contains_clickable_element(text, timeout, error, index)
        self.wait_until_clickable_element_is_visible(text, timeout, error, index)
        self.wait_until_clickable_element_is_enabled(text, timeout, error, index)

    #endregion


    #region get xpath
    
    def get_clickable_element_xpath(self, text, index):
        a_xpath = '((local-name()= "a" or local-name() = "img") and (@title="{0}" or contains(@src, "{0}") or ./img[contains(@src, "{0}")] or contains(normalize-space(.), "{0}")))'.format(text)
        a_contains_img_xpath = '(local-name()= "a" and ./img and contains(text(), "{0}"))'.format(text)
        input_xpath = '(local-name() = "input" and (((@type="submit" or @type="button") and @value="{0}") or (@type="image" and contains(@src, "{0}"))))'.format(text)
        button_xpath = '((local-name() = "button" or local-name() = "span") and contains(normalize-space(.), "{0}"))'.format(text)
        td_xpath = '(local-name() = "td" and normalize-space(text()) = "{0}")'.format(text)
        div_xpath = '((//div[contains(., "{0}")]/text()[contains(., "{0}")])[{1}])/ancestor::div[1]'.format(text, index)
        return self.fix_xpath('(//*[{0} or {1} or {2} or {3} or {4} or @id="{5}"])[{6}]'.format(a_xpath, input_xpath, button_xpath, td_xpath, a_contains_img_xpath, text, index), text)

    def get_clickable_element_near_text_xpath(self, text, locator, index=1):
        a_xpath = '((local-name()= "a" or local-name() = "img") and (@title="{0}" or contains(@src, "{0}") or ./img[contains(@src, "{0}")] or contains(normalize-space(.), "{0}")))'.format(locator)
        input_xpath = '(local-name() = "input" and (((@type="submit" or @type="button") and @value="{0}") or (@type="image" and contains(@src, "{0}"))))'.format(locator)
        button_xpath = '((local-name() = "button" or local-name() = "span") and contains(normalize-space(.), "{0}"))'.format(locator)
        xpath = self.get_htmlelement_is_near_text(text, '*', '{0} or {1} or {2}'.format(a_xpath, input_xpath, button_xpath), 4, index)
        return self.fix_xpath(self.fix_xpath(xpath, text), locator)

    #endregion

    #region page contains
    
    @keyword
    def wait_until_page_contains_clickable_element(self, text, timeout=None, error=None, index=1):
        self.wait_until_page_contains_element(text, self.get_clickable_element_xpath(text, index), timeout, error)

    @keyword
    def wait_until_page_does_not_contain_clickable_element(self, text, timeout=None, error=None, index=1):
        self.wait_until_page_does_not_contain_element(text, self.get_clickable_element_xpath(text, index), timeout, error)

    @keyword
    def wait_until_page_contains_clickable_element_near_text(self, text, locator, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, '*',
            '((local-name()= "a" or local-name() = "img") and (@title="{0}" or contains(@src, "{0}") or ./img[contains(@src, "{0}")] or contains(normalize-space(.), "{0}"))) or (local-name() = "input" and @type="submit" and @value="{locator}") or ((local-name() = "button" or local-name() = "span") and contains(normalize-space(.), "{0}"))'.format(locator),
            4,
            timeout,
            error
        )

    #endregion


    #region visible

    @keyword
    def wait_until_clickable_element_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, self.get_clickable_element_xpath(text, index), timeout, error)

    @keyword
    def clickable_element_should_be_visible(self, text, message=None, index=1):
        self.element_should_be_visible(text, self.get_clickable_element_xpath(text, index), message)

    @keyword
    def clickable_element_should_not_be_visible(self, text, message=None, index=1):
        self.element_should_not_be_visible(text, self.get_clickable_element_xpath(text, index), message)

    #endregion

    #region enabled

    @keyword
    def wait_until_clickable_element_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_enabled(text, self.get_clickable_element_xpath(text, index), timeout, error)

    @keyword
    def clickable_element_should_be_disabled(self, text, index=1):
        self.element_should_be_disabled(self.get_clickable_element_xpath(text, index))

    @keyword
    def clickable_element_should_be_enabled(self, text, index=1):
        self.element_should_be_enabled(self.get_clickable_element_xpath(text, index))

    #endregion

    #region Url

    @keyword
    def get_url_of_clickable_element(self, text, index=1):
        self.wait_until_page_contains_clickable_element(text, 120)
        xpath = self.get_clickable_element_xpath(text, index)
        return self.get_element_attribute('xpath={0}'.format(xpath), 'href')

    @keyword
    def url_of_clickable_element_should_be(self, url, message=None, index=1):
        if message == None:
            message = 'Đường dẫn của element "{0}" không phải là {1}'.format(text, url)

        BuiltIn().should_be_equal_as_strings(self.get_url_of_clickable_element(text, index), url, message)

    @keyword
    def url_of_clickable_element_should_contain(self, url, message=None, index=1):
        if message == None:
            message = 'Đường dẫn của element "{0}" không chứa {1}'.format(text, url)

        BuiltIn().should_match_regexp(self.get_url_of_clickable_element(text, index), '.*url*.', message)

    #endregion


    #region click

    @keyword
    def click_clickable_element_near_text(self, text, locator, index=1):
        self.click_clickable_element_with_xpath(self.get_clickable_element_near_text_xpath(text, locator, index))

    @keyword
    def click(self, text, index=1):
        self.click_clickable_element(text, index)

    @keyword
    def click_clickable_element(self, text, index=1):
        xpath = self.get_clickable_element_xpath(text, index)
        self.wait_until_clickable_element_is_useable(text, 120, None, 1)
        self.click_clickable_element_with_xpath(xpath)
        self.log('Click on element \'xpath={0}\''.format(xpath))

    @keyword
    def double_click(self, text, index=1):
        self.double_click_clickable_element(text, index)

    @keyword
    def double_click_clickable_element(self, text, index=1):
        xpath = self.get_clickable_element_xpath(text, index)
        self.ctx.keywords['double_click_element']('xpath={0}'.format(xpath))

    #endregion
