import abc
import argparse
import logging

from phonemizer import phonemize
from wai.logging import LOGGING_WARNING

from adc.api import Phonemizer


class BasePhonemizer(Phonemizer, abc.ABC):
    """
    Base phonemizer class.
    """

    def __init__(self, language: str = None, strip: bool = None,
                 preserve_empty_lines: bool = None, preserve_punctuation: bool = None, njobs: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the phonemizer.

        :param language: the language to use
        :type language: str
        :param strip: whether to omit the last word and phone separators of a token
        :type strip: bool
        :param preserve_punctuation: whether to preserve punctuation
        :type preserve_punctuation: bool
        :param preserve_empty_lines: whether to preserve empty lines
        :type preserve_empty_lines: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.language = language
        self.strip = strip
        self.preserve_empty_lines = preserve_empty_lines
        self.preserve_punctuation = preserve_punctuation
        self.njobs = njobs
        self._backend = None

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-L", "--language", type=str, help="The language of the speech data, e.g., 'en-us'.", required=False, default="en-us")
        parser.add_argument("--strip", action="store_true", help="Whether to omit the last word and phone separators of a token.")
        parser.add_argument("--preserve_empty_lines", action="store_true", help="Whether to keep empty lines.")
        parser.add_argument("--preserve_punctuation", action="store_true", help="Whether to keep punctuation.")
        parser.add_argument("--njobs", type=int, help="The number of jobs to execute in parallel.", required=False, default=1)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.language = ns.language
        self.strip = ns.strip
        self.preserve_empty_lines = ns.preserve_empty_lines
        self.preserve_punctuation = ns.preserve_punctuation
        self.njobs = ns.njobs

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.language is None:
            self.language = "en-us"
            self.logger().warning("No language(s) defined, falling back on: %s" % self.language)
        if self.strip is None:
            self.strip = False
        if self.preserve_empty_lines is None:
            self.preserve_empty_lines = False
        if self.preserve_punctuation is None:
            self.preserve_punctuation = False
        if self.njobs is None:
            self.njobs = 1

    def _do_phonemize(self, text: str) -> str:
        """
        Applies the phonemizer algorithm to the supplied string.

        :param text: the string to process
        :type text: str
        :return: the processed string
        :rtype: str
        """
        resp = phonemize(
            text,
            language=self.language,
            backend=self._backend,
            strip=self.strip,
            preserve_punctuation=self.preserve_punctuation,
            preserve_empty_lines=self.preserve_empty_lines,
            njobs=self.njobs)
        result = str(resp)
        if self.logger().info(logging.INFO):
            self.logger().info(result)
        return result


class Espeak(BasePhonemizer):
    """
    Base phonemizer class.
    """

    def __init__(self, language: str = None, strip: bool = None,
                 preserve_empty_lines: bool = None, preserve_punctuation: bool = None, njobs: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the phonemizer.

        :param language: the language to use
        :type language: str
        :param strip: whether to omit the last word and phone separators of a token
        :type strip: bool
        :param preserve_punctuation: whether to preserve punctuation
        :type preserve_punctuation: bool
        :param preserve_empty_lines: whether to preserve empty lines
        :type preserve_empty_lines: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(language=language, strip=strip, preserve_empty_lines=preserve_empty_lines,
                         preserve_punctuation=preserve_punctuation, njobs=njobs,
                         logger_name=logger_name, logging_level=logging_level)
        self._backend = "espeak"

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "ph-espeak"

    def description(self) -> str:
        """
        Returns a description of the phonemizer.

        :return: the description
        :rtype: str
        """
        return "Uses the espeak backend of the phonemizer library: https://github.com/bootphon/phonemizer\nFor available languages see: https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md"
