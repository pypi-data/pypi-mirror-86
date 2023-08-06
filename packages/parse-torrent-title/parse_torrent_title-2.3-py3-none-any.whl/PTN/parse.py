#!/usr/bin/env python
from . import re
from .post import post_processing_before_excess, post_processing_after_excess
from .patterns import patterns, types, delimiters, patterns_ordered
from .extras import exceptions, patterns_ignore_title, link_patterns, langs, genres


class PTN(object):
    def __init__(self):
        self.torrent_name = None
        self.parts = None
        self.part_slices = None
        self.match_slices = None
        self.standardise = None

        self.post_title_pattern = '(?:{}|{})'.format(link_patterns(patterns['season']),
                                                     link_patterns(patterns['year']))

    def _part(self, name, match_slice, clean, overwrite=False):
        if overwrite or name not in self.parts:
            if isinstance(clean, list) and len(clean) == 1:
                clean = clean[0]  # Avoids making a list if it only has 1 element
            self.parts[name] = clean
            self.part_slices[name] = match_slice

        # Ignored patterns will still be considered 'matched' to remove them from excess.
        if match_slice:
            self.match_slices.append(match_slice)

    @staticmethod
    def _clean_string(string):
        clean = re.sub(r'^( -|\(|\[)', '', string)
        if clean.find(' ') == -1 and clean.find('.') != -1:
            clean = re.sub(r'\.', ' ', clean)
        clean = re.sub(r'_', ' ', clean)
        clean = re.sub(r'([\[)_\]]|- )$', '', clean).strip()
        clean = clean.strip(' _-')

        return clean

    def parse(self, name, standardise):
        name = name.strip()
        self.parts = dict()
        self.part_slices = dict()
        self.torrent_name = name
        self.match_slices = list()
        self.standardise = standardise

        for key, pattern_options in [(key, patterns[key]) for key in patterns_ordered]:
            pattern_options = self.normalise_pattern_options(pattern_options)

            for (pattern, replace, transforms) in pattern_options:
                if key not in ('season', 'episode', 'website', 'language', 'genre'):
                    pattern = r'\b(?:{})\b'.format(pattern)

                clean_name = re.sub(r'_', ' ', self.torrent_name)
                matches = self.get_matches(pattern, clean_name, key)

                if not matches:
                    continue

                # With multiple matches, we will usually want to use the first match.
                # For 'year', we instead use the last instance of a year match since,
                # if a title includes a year, we don't want to use this for the year field.
                match_index = 0
                if key == 'year':
                    match_index = -1

                match = matches[match_index]['match']
                match_start, match_end = matches[match_index]['start'], matches[match_index]['end']
                if key in self.parts:  # We can skip ahead if we already have a matched part
                    self._part(key, (match_start, match_end), None, overwrite=False)
                    continue

                index = self.get_match_indexes(match)

                if key in ('season', 'episode'):
                    clean = self.get_season_episode(match)
                elif key == 'subtitles':
                    clean = self.get_subtitles(match)
                elif key in ('language', 'genre'):
                    clean = self.split_multi(match)
                elif key in types.keys() and types[key] == 'boolean':
                    clean = True
                else:
                    clean = match[index['clean']]
                    if key in types.keys() and types[key] == 'integer':
                        clean = int(clean)

                if self.standardise:
                    clean = self.standardise_clean(clean, key, replace, transforms)

                self._part(key, (match_start, match_end), clean)

        self.process_title()
        self.fix_known_exceptions()

        unmatched = self.get_unmatched()
        for f in post_processing_before_excess:
            unmatched = f(self, unmatched)

        # clean_unmatched() depends on the before_excess methods adding more match slices.
        cleaned_unmatched = self.clean_unmatched()
        if cleaned_unmatched:
            self._part('excess', None, cleaned_unmatched)

        for f in post_processing_after_excess:
            f(self)

        return self.parts

    # Handles all the optional/missing tuple elements into a consistent list.
    @staticmethod
    def normalise_pattern_options(pattern_options):
        pattern_options_norm = list()

        if isinstance(pattern_options, tuple):
            pattern_options = [pattern_options]
        elif not isinstance(pattern_options, list):
            pattern_options = [(pattern_options, None, None)]
        for options in pattern_options:
            if len(options) == 2:  # No transformation
                pattern_options_norm.append(options + (None,))
            elif isinstance(options, tuple):
                if isinstance(options[2], tuple):
                    pattern_options_norm.append(tuple(list(options[:2]) + [[options[2]]]))
                elif isinstance(options[2], list):
                    pattern_options_norm.append(options)
                else:
                    pattern_options_norm.append(tuple(list(options[:2]) + [[(options[2], [])]]))

            else:
                pattern_options_norm.append((options, None, None))
        pattern_options = pattern_options_norm
        return pattern_options

    def get_matches(self, pattern, clean_name, key):
        grouped_matches = list()
        matches = list(re.finditer(pattern, clean_name, re.IGNORECASE))
        for m in matches:
            if m.start() < self.ignore_before_index(clean_name, key):
                continue
            groups = m.groups()
            if not groups:
                grouped_matches.append((m.group(), m.start(), m.end()))
            else:
                grouped_matches.append((groups, m.start(), m.end()))

        parsed_matches = list()
        for match in grouped_matches:
            m = match[0]
            if isinstance(m, tuple):
                m = list(m)
            else:
                m = [m]
            parsed_matches.append({'match': m,
                                   'start': match[1],
                                   'end': match[2]})
        return parsed_matches

    # Only use part of the torrent name after the (guessed) title (split at a season or year)
    # to avoid matching certain patterns that could show up in a release title.
    def ignore_before_index(self, clean_name, key):
        match = None
        if key in patterns_ignore_title:
            patterns_ignored = patterns_ignore_title[key]
            if not patterns_ignored:
                match = re.search(self.post_title_pattern, clean_name, re.IGNORECASE)
            else:
                for ignore_pattern in patterns_ignored:
                    if re.findall(ignore_pattern, clean_name, re.IGNORECASE):
                        match = re.search(self.post_title_pattern, clean_name, re.IGNORECASE)

        if match:
            return match.start()
        return 0

    @staticmethod
    def get_match_indexes(match):
        index = {'raw': 0, 'clean': 0}

        if len(match) > 1:
            # for season we might have it in index 1 or index 2
            # e.g. "5x09"
            for i in range(1, len(match)):
                if match[i]:
                    index['clean'] = i
                    break

        return index

    @staticmethod
    def get_season_episode(match):
        clean = None
        m = re.findall(r'[0-9]+', match[0])
        if m and len(m) > 1:
            clean = list(range(int(m[0]), int(m[-1]) + 1))
        elif m:
            clean = int(m[0])
        return clean

    @staticmethod
    def split_multi(match):
        # handle multi languages
        m = re.split(r'{}+'.format(delimiters), match[0])
        clean = list(filter(None, m))

        return clean

    @staticmethod
    def get_subtitles(match):
        # handle multi subtitles
        m = re.split(r'{}+'.format(delimiters), match[0])
        m = list(filter(None, m))
        clean = list()
        # If it's only 1 result, it's fine if it's just 'subs'.
        if len(m) == 1:
            clean = m
        else:
            for x in m:
                if not re.match('subs?|soft', x, re.I):
                    clean.append(x)

        return clean

    def standardise_clean(self, clean, key, replace, transforms):
        if replace:
            clean = replace
        if transforms:
            for transform in filter(lambda t: t[0], transforms):
                # For python2 compatibility, we're not able to simply pass functions as str.upper
                # means different things in 2.7 and 3.5.
                clean = getattr(clean, transform[0])(*transform[1])
        if key == 'language' or key == 'subtitles':
            clean = self.standardise_languages(clean)
            if not clean:
                clean = 'Available'
        if key == 'genre':
            clean = self.standardise_genres(clean)
        return clean

    @staticmethod
    def standardise_languages(clean):
        cleaned_langs = list()
        for lang in clean:
            for (lang_regex, lang_clean) in langs:
                if re.match(lang_regex, re.sub(link_patterns(patterns['subtitles'][2:]), '', lang, flags=re.I),
                            re.IGNORECASE):
                    cleaned_langs.append(lang_clean)
                    break
        clean = cleaned_langs
        return clean

    @staticmethod
    def standardise_genres(clean):
        standard_genres = list()
        for genre in clean:
            for (regex, clean) in genres:
                if re.match(regex, genre, re.IGNORECASE):
                    standard_genres.append(clean)
                    break
        return standard_genres

    # Merge all the match slices (such as when they overlap), then remove
    # them from excess.
    def merge_match_slices(self):
        matches = sorted(self.match_slices, key=lambda match: match[0])

        i = 0
        slices = list()
        while i < len(matches):
            start, end = matches[i]
            i += 1
            for (next_start, next_end) in matches[i:]:
                if next_start <= end:
                    end = max(end, next_end)
                    i += 1
                else:
                    break
            slices.append((start, end))

        self.match_slices = slices

    def process_title(self):
        unmatched = self.unmatched_list(keep_punctuation=False)

        # Use the first one as the title
        if unmatched:
            title_start, title_end = unmatched[0][0], unmatched[0][1]

            # If our unmatched is after the first 3 matches, we assume the title is missing
            # (or more likely got parsed as something else), as no torrents have it that
            # far away from the beginning of the release title.
            if title_start > sorted(self.part_slices.values(), key=lambda s: s[0])[min(3, len(self.part_slices)-1)][0]:
                self._part('title', None, '')

            raw = self.torrent_name[title_start:title_end]
            if '(' in raw:
                title_end = self.torrent_name.index('(', title_start)
                raw = raw.split('(')[0]
            clean = self._clean_string(raw)
            self._part('title', (title_start, title_end), clean)
        else:
            self._part('title', None, '')

    def unmatched_list(self, keep_punctuation=True):
        self.merge_match_slices()
        unmatched = list()
        prev_start = 0
        end = len(self.torrent_name)  # A default so the last append won't crash if nothing has matched
        # Find all unmatched strings that aren't just punctuation
        for (start, end) in self.match_slices:
            if keep_punctuation or not re.match(delimiters + r'*\Z', self.torrent_name[prev_start:start]):
                unmatched.append((prev_start, start))
            prev_start = end

        # Add the last unmatched slice
        if keep_punctuation or not re.match(delimiters + r'*\Z', self.torrent_name[end:]):
            unmatched.append((end, len(self.torrent_name)))

        return unmatched

    def fix_known_exceptions(self):
        # Considerations for results that are known to cause issues, such
        # as media with years in them but without a release year.
        for exception in exceptions:
            incorrect_key, incorrect_value = exception['incorrect_parse']
            if (self.parts['title'] == exception['parsed_title'] and
                incorrect_key in self.parts and self.parts[incorrect_key] == incorrect_value):
                self.parts.pop(incorrect_key)
                self._part('title', None, exception['actual_title'], overwrite=True)

    def get_unmatched(self):
        unmatched = ''
        for (start, end) in self.unmatched_list():
            unmatched += self.torrent_name[start:end]

        return unmatched

    def clean_unmatched(self):
        unmatched = list()
        for (start, end) in self.unmatched_list():
            unmatched.append(self.torrent_name[start:end])

        unmatched_clean = list()
        for raw in unmatched:
            clean = re.sub(r'(^[-_.\s(),]+)|([-.\s,]+$)', '', raw)
            clean = re.sub(r'[()/]', ' ', clean)
            unmatched_clean += re.split(r'\.\.+|\s+', clean)

        filtered = list()
        for extra in unmatched_clean:
            # re.fullmatch() is not available in python 2.7, so we manually do it with \Z.
            if not re.match(r'(?:Complete|Season|Full)?[\]\[,.+\- ]*(?:Complete|Season|Full)?\Z', extra, re.IGNORECASE):
                filtered.append(extra)
        return filtered
