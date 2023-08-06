from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class TextKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)
    
    @keyword
    def wait_until_page_contains_text(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = 'Không thể tìm thấy text "{0}"'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)
        
    @keyword
    def wait_until_text_is_visible(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = '"{0}" không được hiển thị'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)

    @keyword
    def wait_until_page_does_not_contain_text(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = 'Vẫn thể tìm thấy text "{0}"'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)