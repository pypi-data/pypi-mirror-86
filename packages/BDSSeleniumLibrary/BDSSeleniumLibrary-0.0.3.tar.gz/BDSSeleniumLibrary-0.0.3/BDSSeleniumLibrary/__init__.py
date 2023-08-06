from SeleniumLibrary import SeleniumLibrary
from .Keywords import (
    InputKeywords,
    ClickableElementKeywords,
    TextAreaKeywords,
    FileInputKeywords,
    TextKeywords,
    SingleDropdownKeywords,
    FancyBoxKeywords,
    RadioKeywords,
    CheckBoxKeywords,
    MultipleDropdownKeywords,
    AdvancedDropdownKeywords
)

class BDSSeleniumLibrary(SeleniumLibrary):
    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None, plugins=None,
                 event_firing_webdriver=None):
        SeleniumLibrary.__init__(
            self, timeout, implicit_wait, 
            run_on_failure, 
            screenshot_root_directory, plugins,
            event_firing_webdriver)
        
        self.add_library_components([
            InputKeywords(self),
            ClickableElementKeywords(self),
            TextAreaKeywords(self),
            FileInputKeywords(self),
            TextKeywords(self),
            SingleDropdownKeywords(self),
            FancyBoxKeywords(self),
            RadioKeywords(self),
            CheckBoxKeywords(self),
            MultipleDropdownKeywords(self),
            AdvancedDropdownKeywords(self)
        ])