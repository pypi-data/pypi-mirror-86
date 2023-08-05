# -*- coding: utf-8 -*-

"""
melenium.webdriver
~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ChromeCapabilities', 'ChromeDriver', 'ChromeSWB']

from selenium.webdriver import Chrome as SeChrome

from seleniumwire.webdriver import Chrome as SwChrome
from seleniumwire.webdriver.request import InspectRequestsMixin
from seleniumwire.proxy.client import AdminClient

import pyaction as pa
import pickle

from .wait_for import WaitFor
from .common.capabilities import ChromeCapabilities

try:
    from bs4 import BeautifulSoup as BS
except ImportError:
    from beautifulsoup4 import BeautifulSoup as BS

#-----------------------------------------------------------------------------

class Chrome(SeChrome):

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):

        """
        Creates a new instance of the chrome driver.

        Starts the service and then creates new instance of chrome driver.

        :Args:
         - executable_path - path to the executable. If the default is used it assumes the executable is in the $PATH
         - port - port you would like the service to run, if left as 0, a free port will be found.
         - options - this takes an instance of ChromeOptions
         - service_args - List of args to pass to the driver service
         - desired_capabilities - Dictionary object with non-browser specific
           capabilities only, such as "proxy" or "loggingPref".
         - service_log_path - Where to log information from the driver.
         - chrome_options - Deprecated argument for options
         - keep_alive - Whether to configure ChromeRemoteConnection to use HTTP keep-alive.
        """

        super().__init__(executable_path, port, options, service_args, desired_capabilities, service_log_path, chrome_options, keep_alive)
        self._wait_for = WaitFor(self)

    def find(self, *argv, **kwargs):
        bs_element = BS(self.page_source, features = 'html.parser').find(*argv, **kwargs)

        if bs_element != None:
            xpath = pa.get_xpath(bs_element)
            return self.find_element_by_xpath(xpath)

        else:
            return None

    def find_element_by_bs(self, bs_element):
        if bs_element != None:
            xpath = pa.get_xpath(bs_element)
            return self.find_element_by_xpath(xpath)

        else:
            return None

    def upload_cookies(self, cookies_file, exclude=['expiry']):
        for cookie in pickle.load(open(cookies_file, "rb")):

            for key_ in exlude:
                if key_ in cookie:
                    del cookie[key_]

            self.add_cookie(cookie)

    @property
    def wait_for(self):
        return self._wait_for

#-----------------------------------------------------------------------------

class ChromeSWB(InspectRequestsMixin, Chrome):

    def __init__(self, *args, seleniumwire_options=None, **kwargs):

        if seleniumwire_options is None:
            seleniumwire_options = {}

        self._client = AdminClient()
        addr, port = self._client.create_proxy(
            port=seleniumwire_options.pop('port', 0),
            options=seleniumwire_options
        )

        if 'port' not in seleniumwire_options:
            try:
                capabilities = kwargs.pop('desired_capabilities')
            except KeyError:
                capabilities = ChromeCapabilities('empty').desired

            capabilities['proxy'] = {
                'proxyType': 'manual',
                'httpProxy': '{}:{}'.format(addr, port),
                'sslProxy': '{}:{}'.format(addr, port),
                'noProxy': ''
            }
            capabilities['acceptInsecureCerts'] = True

            kwargs['desired_capabilities'] = capabilities

        kwargs['desired_capabilities']['goog:chromeOptions']['args'].append('proxy-bypass-list=<-loopback>')

        super().__init__(*args, **kwargs)

    def quit(self):
        self._client.destroy_proxy()
        super().quit()

#-----------------------------------------------------------------------------
