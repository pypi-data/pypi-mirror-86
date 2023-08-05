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
v1.0.0
pas_l10n/l10n.py
"""

from os import path
from threading import local
import os
import re

from dpt_runtime.binary import Binary
from dpt_runtime.io_exception import IOException
from dpt_runtime.value_exception import ValueException
from dpt_settings import Settings
from dpt_threading.instance_lock import InstanceLock

from .l10n_instance import L10nInstance

class L10n(object):
    """
Provides static l10n (localization) methods.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: l10n
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_SPECIAL_CHARACTERS = re.compile("\\W+")
    """
RegExp to find non-word characters
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    default_lang = None
    """
Default application language
    """
    _instances = { }
    """
L10n instances
    """
    _instances_lock = InstanceLock()
    """
Thread safety instances lock
    """
    _local = local()
    """
Local data handle
    """

    @staticmethod
    def format_number(number, fractional_digits = -1, lang = None):
        """
Returns a formatted number.

:param number: Number as int or float
:param fractional_digits: Fractional digits to return
:param lang: Language code

:return: (str) Formatted value
:since:  v1.0.0
        """

        return L10n.get_instance(lang).format_number(number, fractional_digits)
    #

    @staticmethod
    def get(key = None, default = None, lang = None):
        """
Returns the value with the specified key or the default one if undefined.

:param key: L10n key
:param default: Default value if not translated
:param lang: Language code

:return: (str) Value
:since:  v1.0.0
        """

        return L10n.get_dict(lang).get(key, (key if (default is None) else default))
    #

    @staticmethod
    def get_base_path():
        """
Returns the base path to localization specific directories and files.

:return: (str) Localization base path
:since:  v1.0.0
        """

        _return = Settings.get("path_lang")

        if (_return is None):
            _return = (Binary.str(os.environ['PAS_PATH_LANG'])
                       if ("PAS_PATH_LANG" in os.environ) else
                       path.join(Settings.get("path_base"), "lang")
                      )

            Settings.set("path_lang", _return)
        #

        return _return
    #

    @staticmethod
    def get_default_lang():
        """
Returns the defined default language of the current task.

:return: (str) Language code
:since:  v1.0.0
        """

        _return = None

        if (hasattr(L10n._local, "lang")): _return = L10n._local.lang
        if (_return is None): _return = L10n.default_lang
        if (_return is None): _return = Settings.get("core_lang")

        return _return
    #

    @staticmethod
    def get_dict(lang = None):
        """
Returns all language strings for the given or default language currently
defined as a dict.

:param lang: Language code

:return: (dict) L10nInstance dict
:since:  v1.0.0
        """

        if (lang is None): lang = L10n.get_default_lang()
        elif (L10n.default_lang is None): L10n.default_lang = lang

        if (lang is None): raise ValueException("Language not defined and default language is undefined.")

        if (lang not in L10n._instances):
            with L10n._instances_lock:
                # Thread safe
                if (lang not in L10n._instances): L10n._instances[lang] = L10nInstance(lang)
            #
        #

        return L10n._instances[lang]
    #

    @staticmethod
    def get_instance(lang = None):
        """
Get the L10n dict instance of the given or default language.

:param lang: Language code

:return: (object) L10nInstance
:since:  v1.0.0
        """

        return L10n.get_dict(lang)
    #

    @staticmethod
    def get_relative_file_path_name(file_id):
        """
Returns the relative file path and name for the file ID given.

:param file_id: L10n file ID

:return: (str) File path and name
:since:  v1.0.0
        """

        file_id = Binary.str(file_id)

        file_id_elements = file_id.split(".")
        _return = ""

        for file_id_element in file_id_elements:
            if (file_id_element):
                file_id_element = L10n.RE_SPECIAL_CHARACTERS.sub(" ", file_id_element)
                _return += ("/" if (len(_return) > 0) else "") + file_id_element
            #
        #

        return _return
    #

    @staticmethod
    def init(file_id, lang = None):
        """
Load the given language section.

:param file_id: L10n file ID

:since: v1.0.0
        """

        base_path = L10n.get_base_path()

        instance = L10n.get_instance(lang)
        relative_file_path_name = L10n.get_relative_file_path_name(file_id)

        file_path_name = "{0}/{1}/{2}.json".format(base_path, instance.lang, relative_file_path_name)

        try: instance.read_file(file_path_name, True)
        except ( IOException, ValueException ):
            fallback_lang = (Settings.get("core_lang") if (L10n.default_lang is None) else L10n.default_lang)

            file_path_name = "{0}/{1}/{2}.json".format(base_path, fallback_lang, relative_file_path_name)
            instance.read_file(file_path_name)
        #
    #

    @staticmethod
    def is_defined(key, lang = None):
        """
Checks if a given key is a defined language string.

:param key: L10n key
:param lang: Language code

:return: (bool) True if defined
:since:  v1.0.0
        """

        try: _dict = L10n.get_dict(lang)
        except ValueException: _dict = { }

        return (key in _dict)
    #

    @staticmethod
    def set_default_lang(lang):
        """
Defines the default language of the application.

:param lang: Language code

:since: v1.0.0
        """

        L10n.default_lang = lang
    #

    @staticmethod
    def set_thread_lang(lang):
        """
Defines a default language for the calling thread.

:param lang: Language code

:since: v1.0.0
        """

        L10n._local.lang = lang
    #
#
