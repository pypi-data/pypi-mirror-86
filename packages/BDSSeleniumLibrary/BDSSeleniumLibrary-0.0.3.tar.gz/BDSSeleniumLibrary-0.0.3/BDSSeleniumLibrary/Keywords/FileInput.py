from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent

class FileInputKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    @keyword
    def upload_file(self, text, url, index=1):
        self.ctx.keywords['choose_file']('xpath={0}'.format(self.get_htmlelement_is_near_text(text, 'input', '@type="file"', 4, 1)), url)

    @keyword
    def file_upload_button_should_not_be_visible(self, text, index=1):
        self.wait_until_element_is_not_visible(text, '{0}/ancestor::div[contains(@class, "spanButtonPlaceholder")]'.format(self.get_htmlelement_is_near_text(text, 'input', '@type="file"', 4, 1)), 2)