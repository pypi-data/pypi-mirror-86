"""
Module with class to process dumped mails
"""
# Standard library imports
import os
import logging

# Third party imports
from char import char
from . import mail_listener

# Local imports

LOGGER = logging.getLogger("outlook_mail_loader")


class DumpedMails(object):
    pass

    @char
    def __init__(
            self,
            str_path_dir_with_mails="mails",
    ):
        """Init object

        Args:
            str_path_dir_with_mails (str, optional): Dir. from where to load
        """
        pass

    @char
    def get_last_n_letters(self, int_letters_to_get):
        """"""
        pass

    def print_stats_about_dumped_mails(self):
        """"""
        list_datetimes = []
        
        mail_listener.print_stats_about_dumped_mails(list_datetimes)
