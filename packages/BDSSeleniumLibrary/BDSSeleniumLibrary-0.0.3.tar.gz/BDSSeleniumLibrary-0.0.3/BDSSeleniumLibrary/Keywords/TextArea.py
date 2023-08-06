from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class TextAreaKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    #region supports

    def wait_until_text_area_is_useable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_text_area(text, timeout, None)
        # self.wait_until_text_area_is_visible(text, timeout, None)
        # self.wait_until_text_area_is_enabled(text, timeout, None)

    def get_text_area_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'textarea', '1=1', 4, index)

    #endregion

    #region enabled
    @keyword
    def wait_until_text_area_is_enabled(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_enabled(text, self.get_text_area_xpath(text, index), timeout, error)

    @keyword
    def text_area_should_be_disabled(self, text, index=1):
        self.element_should_be_disabled(self.get_text_area_xpath(text, index))

    @keyword
    def text_area_should_be_enabled(self, text, index=1):
        self.element_should_be_enabled(self.get_text_area_xpath(text, index))

    #endregion


    #region contains
    @keyword
    def wait_until_page_contains_text_area(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'textarea', '1=1', 4, timeout, error)
    
    @keyword
    def wait_until_page_does_not_contain_text_area(self, text, timeout=None, error=None):
        self.wait_until_page_does_not_contain_htmlelement_being_near_text(text, 'textarea', '1=1', 4, timeout, error)
    
    #endregion

    #region visible
    @keyword
    def wait_until_text_area_is_not_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_not_visible(text, self.get_text_area_xpath(text, index), timeout, error)

    @keyword
    def wait_until_text_area_is_visible(self, text, timeout=None, error=None, index=1):
        self.wait_until_element_is_visible(text, self.get_text_area_xpath(text, index), timeout, error)

    @keyword
    def text_area_should_be_visible(self, text, message=None, index=1):
        self.element_should_be_visible(text, self.get_text_area_xpath(text, index), message)

    @keyword
    def text_area_should_not_be_visible(self, text, message=None, index=1):
        self.element_should_not_be_visible(text, self.get_text_area_xpath(text, index), message)

    #endregion


    #region value
    
    # @keyword('Get Value Of Text Area [String]')
    # def get_value_of_text_area(self, text, value, index=1):
    #     self.wait_until_text_area_is_useable(text, 120, index)
    #     xpath = self.get_text_area_xpath(text, index)
    #     id = self.get_element_attribute('xpath={0}'.format(xpath), 'id')
    #     is_ckeditor = self.execute_script('return window.CKEDITOR != undefined && CKEDITOR.instances["{id}"] != undefined')
    #     is_cleditor = self.get_element_count('xpath={0}/../div[@class = "cleditorToolbar"]'.format(xpath)) > 0

    #     if is_ckeditor:
    #         return self.execute_script('return CKEDITOR.instances["{0}"].getData()")'.format(id))
    #     else if is_cleditor:
    #         return self.execute_script('return $("{id}").cleditor()[0].$area.val()'.format(id))
    #     else:
    #         return self.get_element_attribute('xpath={0}'.format(xpath), 'innerHTML')

    @keyword
    def value_of_text_area_should_be(self, text, expected, message=None, index=1):
        self.textfield_value_should_be(text, self.get_text_area_xpath(text, index), expected, message)

    @keyword
    def value_of_text_area_should_contain(self, text, expected, message=None, index=1):
        self.textfield_should_contain(text, self.get_text_area_xpath(text, index), expected, message)

    #endregion
    

    #region actions
    
    @keyword
    def set_text_area(self, text, value, index=1):
        self.wait_until_text_area_is_useable(text, 120, index)
        xpath = self.get_text_area_xpath(text, index)
        id = self.get_element_attribute('xpath={0}'.format(xpath), 'id')
        is_ckeditor = self.execute_script('return window.CKEDITOR != undefined && CKEDITOR.instances["{id}"] != undefined')
        is_cleditor = self.get_element_count('xpath={0}/../div[@class = "cleditorToolbar"]'.format(xpath)) > 0

        if is_ckeditor:
            self.execute_script('CKEDITOR.instances["{0}"].setData("{1}")'.format(id, value))
        elif is_cleditor:
            self.execute_script('$("#{0}").cleditor()[0].$area.val("{1}");$("#{0}").cleditor()[0].updateFrame();'.format(id, value))
        else:
            self.ctx.keywords['input_text']('xpath={0}'.format(xpath), value)


    #endregion
