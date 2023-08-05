# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;l10n

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasL10nVersion)#
#echo(__FILEPATH__)#
"""

from os import path
import os
import unittest

from pas_l10n import L10n
from dpt_runtime.environment import Environment

try: from dpt_vfs import WatcherImplementation
except ImportError: WatcherImplementation = None

class TestL10n(unittest.TestCase):
    """
UnitTest for L10n

:since: v1.0.0
    """

    def setUp(self):
        Environment.set_base_path(path.sep.join(path.abspath(__file__).split(path.sep)[:-2]))
        if (WatcherImplementation is not None): WatcherImplementation.disable()

        self.de_dict = L10n.get_dict("de")
        L10n.init("pas", "de")
        L10n.init("pas", "en")
    #

    def test_format_number(self):
        """
One key tests everything :)
        """

        self.assertEqual("1234.568", L10n.format_number(1234567.895, 0))
        self.assertEqual("1234.567,90", L10n.format_number(1234567.895, 2))
        self.assertEqual("1234.567,123456", L10n.format_number(1234567.123456))
        self.assertEqual("1234,568", L10n.format_number(1234567.895, 0, lang = "en"))
        self.assertEqual("1234,567.90", L10n.format_number(1234567.895, 2, lang = "en"))
        self.assertEqual("1,235", L10n.format_number(1.234567895, 3))
    #

    def test_value(self):
        """
One key tests everything :)
        """

        self.assertEqual("de-DE", self.de_dict.get("lang_rfc_region"))
        self.assertEqual("en-US", L10n.get("lang_rfc_region", lang = "en"))
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
