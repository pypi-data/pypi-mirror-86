# -*- coding: utf-8 -*-
"""This module contains the tokenizer."""

import codecs
import logging
import re

from .path import ASCII_FOLDING_DICT_PATH

logger = logging.getLogger(__name__)


class Tokenizer:
    """The Tokenizer class encapsulates all the functionality for normalizing and tokenizing a
    given piece of text"""
    ASCII_CUTOFF = ord('\u0080')

    def __init__(self, exclude_from_norm=None):
        """Initializes the tokenizer.

        Args:
            exclude_from_norm (optional) - list of chars to exclude from normalization
        """

        self.ascii_folding_table = self.load_ascii_folding_table()
        self.exclude_from_norm = exclude_from_norm or []
        self._init_regex()

    def _init_regex(self):
        # List of regex's for matching and tokenizing when keep_special_chars=False
        regex_list = []
        # List of regex's for matching and tokenizing when keep_special_chars=True
        keep_special_regex_list = []

        exception_chars = "\@\[\]\|\{\}'"

        # This is more of a tactical fix at this moment. Will probably need a more generic way
        # to handle all currency symbols.
        currency_symbols = "$¥"
        to_exclude = currency_symbols + ''.join(self.exclude_from_norm)

        letter_pattern_str = "[^\W\d_]+"

        # Make keep special regex list
        keep_special_regex_list.append("?P<start>^[^\w\d&" + to_exclude + exception_chars + "]+")
        keep_special_regex_list.append("?P<end>[^\w\d&" + to_exclude + exception_chars + "]+$")
        keep_special_regex_list.append("?P<pattern1>(?P<pattern1_replace>" + letter_pattern_str
                                       + ")" + "[^\w\d\s&" + exception_chars + "]+(?=[\d]+)")
        keep_special_regex_list.append("?P<pattern2>(?P<pattern2_replace>[\d]+)[^\w\d\s&" +
                                       exception_chars + "]+" + "u(?=" + letter_pattern_str + ")")
        keep_special_regex_list.append("?P<pattern3>(?P<pattern3_replace>" + letter_pattern_str +
                                       ")" + "[^\w\d\s&" + exception_chars + "]+" +
                                       "(?=" + letter_pattern_str + ")")
        keep_special_regex_list.append("?P<escape1>(?P<escape1_replace>[\w\d]+)" +
                                       "[^\w\d\s" + exception_chars + "]+" + "(?=\|)")
        keep_special_regex_list.append("?P<escape2>(?P<escape2_replace>[\]\}]+)" +
                                       "[^\w\d\s" + exception_chars + "]+(?=s)")

        # Make regex list
        regex_list.append("?P<start>^[^\w\d&" + to_exclude + "]+")
        regex_list.append("?P<end>[^\w\d&" + to_exclude + "]+$")
        regex_list.append("?P<pattern1>(?P<pattern1_replace>" + letter_pattern_str +
                          ")" + "[^\w\d\s&]+(?=[\d]+)")
        regex_list.append("?P<pattern2>(?P<pattern2_replace>[\d]+)[^\w\d\s&]+(?=" +
                          letter_pattern_str + ")")
        regex_list.append("?P<pattern3>(?P<pattern3_replace>" + letter_pattern_str + ")" +
                          "[^\w\d\s&]+(?=" + letter_pattern_str + ")")

        # commonalities between lists
        regex_list.append("?P<underscore>_")
        keep_special_regex_list.append("?P<underscore>_")

        regex_list.append("?P<begspace>^\s+")
        keep_special_regex_list.append("?P<begspace>^\s+")

        regex_list.append("?P<trailspace>\s+$")
        keep_special_regex_list.append("?P<trailspace>\s+$")

        regex_list.append("?P<spaceplus>\s+")
        keep_special_regex_list.append("?P<spaceplus>\s+")

        keep_special_regex_list.append("?P<bar> '|' ")
        regex_list.append("?P<bar> '|' ")

        keep_special_regex_list.append("?P<apos_s>(?<=[^\\s])'[sS]")
        regex_list.append("?P<apos_s>(?<=[^\\s])'[sS]")

        # handle the apostrophes used at the end of a possessive form, e.g. dennis'
        keep_special_regex_list.append("?P<apos_poss>(?<=[^\\s])'$")
        regex_list.append("?P<apos_poss>(?<=[^\\s])'$")

        # Replace lookup based on regex
        self.replace_lookup = {'apos_s': (" 's", None),
                               'apos_poss': ("", None),
                               'bar': (' ', None),
                               'begspace': ('', None),
                               'end': (' ', None),
                               'escape1': ('{0}', 'escape1_replace'),
                               'escape2': ('{0} ', 'escape2_replace'),
                               'pattern1': ('{0} ', 'pattern1_replace'),
                               'pattern2': ('{0} ', 'pattern2_replace'),
                               'pattern3': ('{0} ', 'pattern3_replace'),
                               'spaceplus': (' ', None),
                               'start': (' ', None),
                               'trailspace': ('', None),
                               'underscore': (' ', None),
                               'apostrophe': (' ', None)}

        # Create a regular expression  from the dictionary keys
        self.keep_special_compiled = re.compile("(%s)" % ")|(".join(
                                                keep_special_regex_list), re.UNICODE)
        self.compiled = re.compile("(%s)" % ")|(".join(regex_list), re.UNICODE)

    # Needed for train-roles where queries are deep copied (and thus tokenizer).
    # Pre compiled patterns don't deepcopy natively. Bug introduced past python 2.5
    # TODO investigate necessity of deepcopy in train-roles
    def __deepcopy__(self, memo):
        # TODO: optimize this
        return Tokenizer(exclude_from_norm=self.exclude_from_norm)

    def load_ascii_folding_table(self):
        logger.debug('Loading ascii folding mapping from file: ' + ASCII_FOLDING_DICT_PATH)

        ascii_folding_table = {}

        with codecs.open(ASCII_FOLDING_DICT_PATH, 'r', encoding='unicode_escape') as mapping_file:
            for line in mapping_file:
                tokens = line.split()
                codepoint = tokens[0]
                ascii_char = tokens[1]
                ascii_folding_table[ord(codepoint)] = ascii_char

        return ascii_folding_table

    # Helper function for for multiple replace. Takes match object and looks up replacement
    def _one_xlat(self, match_object):
        replace_str, format_str = self.replace_lookup[match_object.lastgroup]
        if format_str:
            replace_str = replace_str.format(match_object.groupdict()[format_str])
        return replace_str

    # Takes text and compiled pattern, does lookup for multi re match
    def multiple_replace(self, text, compiled):
        # For each match, look-up corresponding value in dictionary
        return compiled.sub(self._one_xlat, text)

    def normalize(self, text, keep_special_chars=True):
        norm_tokens = self.tokenize(text, keep_special_chars)
        normalized_text = " ".join(t['entity'] for t in norm_tokens)

        return normalized_text

    def tokenize(self, text, keep_special_chars=True):
        """Tokenizes the input text, normalizes the token text and returns normalized tokens.

        Currently it does the following during normalization:
        1. remove leading special characters except dollar sign and ampersand
        2. remove trailing special characters except ampersand
        3. remove special characters except ampersand when the preceding character is a letter and
        the following characters is a number
        4. remove special characters except ampersand when the preceding character is a number and
        the following character is a letter
        5. remove special characters except ampersand when both preceding and following characters
        are letters
        6. remove special character except ampersand when the following character is '|'
        7. remove diacritics and replace it with equivalent ascii character when possible

        Note that the tokenizer also excludes a list of special characters used in annotations when
        the flag keep_special_chars is set to True
        """

        raw_tokens = self.tokenize_raw(text)

        norm_tokens = []
        for i, raw_token in enumerate(raw_tokens):
            if not raw_token['text'] or len(raw_token['text']) == 0:
                continue

            norm_token_start = len(norm_tokens)
            norm_token_text = raw_token['text']

            if keep_special_chars:
                norm_token_text = self.multiple_replace(norm_token_text, self.keep_special_compiled)
            else:
                norm_token_text = self.multiple_replace(norm_token_text, self.compiled)

            # fold to ascii
            norm_token_text = self.fold_str_to_ascii(norm_token_text)

            norm_token_text = norm_token_text.lower()

            norm_token_count = 0
            if len(norm_token_text) > 0:
                # remove diacritics and fold the character to equivalent ascii character if possible
                for text in norm_token_text.split():
                    norm_token = {}
                    norm_token['entity'] = text
                    norm_token['raw_entity'] = raw_token['text']
                    norm_token['raw_token_index'] = i
                    norm_token['raw_start'] = raw_token['start']
                    norm_tokens.append(norm_token)
                    norm_token_count += 1

            raw_token['norm_token_start'] = norm_token_start
            raw_token['norm_token_count'] = norm_token_count

        return norm_tokens

    def tokenize_raw(self, text):
        tokens = []
        token = None
        token_text = ''
        for i, char in enumerate(text):
            if char.isspace():
                if token and token_text:
                    token['text'] = token_text
                    tokens.append(token)
                token = None
                token_text = ''
                continue
            if not token_text:
                token = {'start': i}
            token_text += char

        if token and token_text:
            token['text'] = token_text
            tokens.append(token)

        return tokens

    def get_char_index_map(self, raw_text, normalized_text):
        """
        Generates character index mapping from normalized query to raw query. The entity model
        always operates on normalized query during NLP processing but for entity output we need
        to generate indexes based on raw query.

        The mapping is generated by calculating edit distance and backtrack to get the
        proper alignment.

        :param raw_text: raw query text
        :param normalized_text: normalized query text
        :return: (dict) a mapping of character indexes from normalized query to raw query
        """

        text = raw_text.lower()
        text = self.fold_str_to_ascii(text)

        m = len(raw_text)
        n = len(normalized_text)

        # handle case where normalized text is the empty string
        if n == 0:
            raw_to_norm_mapping = dict([(i, 0) for i in range(m)])
            return raw_to_norm_mapping, {0: 0}

        # handle case where normalized text and raw text are identical
        if m == n and raw_text == normalized_text:
            mapping = {i: i for i in range(n)}
            return mapping, mapping

        edit_dis = []
        for i in range(0, n+1):
            edit_dis.append([0] * (m+1))
        edit_dis[0] = list(range(0, m+1))
        for i in range(0, n+1):
            edit_dis[i][0] = i

        directions = []
        for i in range(0, n+1):
            directions.append([''] * (m+1))

        for i in range(1, n+1):
            for j in range(1, m+1):
                dis = 999
                direction = None

                diag_dis = edit_dis[i-1][j-1]
                if normalized_text[i-1] != text[j-1]:
                    diag_dis += 1

                # dis from going down
                down_dis = edit_dis[i-1][j] + 1

                # dis from going right
                right_dis = edit_dis[i][j-1] + 1

                if down_dis < dis:
                    dis = down_dis
                    direction = '↓'
                if right_dis < dis:
                    dis = right_dis
                    direction = '→'
                if diag_dis < dis:
                    dis = diag_dis
                    direction = '↘'

                edit_dis[i][j] = dis
                directions[i][j] = direction

        mapping = {}

        # backtrack
        m_idx = m
        n_idx = n
        while m_idx > 0 and n_idx > 0:
            if directions[n_idx][m_idx] == '↘':
                mapping[n_idx-1] = m_idx-1
                m_idx -= 1
                n_idx -= 1
            elif directions[n_idx][m_idx] == '→':
                m_idx -= 1
            elif directions[n_idx][m_idx] == '↓':
                n_idx -= 1

        # initialize the forward mapping (raw to normalized text)
        raw_to_norm_mapping = {0: 0}

        # naive approach for generating forward mapping. this is naive and probably not robust.
        # all leading special characters will get mapped to index position 0 in normalized text.
        raw_to_norm_mapping.update({v: k for k, v in mapping.items()})
        for i in range(0, m):
            if i not in raw_to_norm_mapping:
                raw_to_norm_mapping[i] = raw_to_norm_mapping[i-1]

        return raw_to_norm_mapping, mapping

    def fold_char_to_ascii(self, char):
        char_ord = ord(char)
        if char_ord < self.ASCII_CUTOFF:
            return char

        try:
            return self.ascii_folding_table[char_ord]
        except KeyError:
            return char

    def fold_str_to_ascii(self, text):
        folded_str = ''
        for char in text:
            folded_str += self.fold_char_to_ascii(char)

        return folded_str

    def __repr__(self):
        return "<Tokenizer exclude_from_norm: {}>".format(self.exclude_from_norm.__repr__())

    @staticmethod
    def create_tokenizer(app_path=None):
        """Creates the preprocessor for the app at app path

        Args:
            app_path (str, Optional): The path to the directory containing the
                app's data. If None is passed, a default tokenizer will be
                returned.

        Returns:
            Tokenizer: a tokenizer
        """
        return Tokenizer()
