"""
This is a simple Markdown to HTML preprocessor that doesn't require third-party modules.
"""

import re

# Initialize constants and compile RegEx.
REGEX_BLOCKQUOTE = re.compile(r"""
    ^           # Match line start.
    \ *         # Match between 0 and ∞ whitespaces.
    (>+)        # CAPTURE GROUP (blockquote level) | Match between 1 and ∞ ">".
    \ *         # Match between 0 and ∞ whitespaces.
    ([^\s>].*?) # CAPTURE GROUP (blockquote contents) | Match first character that is not
                # ">" or a whitespace, then match between 0 and ∞ characters, as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    $           # Match line end.""", re.VERBOSE)

REGEX_BOLD = re.compile(r"""
    (?<!\\)         # Ensure there's no escaping backslash.
    \*{2}           # Match "*" twice.
    ([^\s*].*?)     # CAPTURE GROUP | Match first character that is not "*" or a whitespace,
                    # then match between 0 and ∞ characters, as few times as possible.
    (?<![\\\s*])    # Ensure there's no escaping backslash, whitespace, or "*".
    \*{2}           # Match "*" twice.
    |               # OR
    (?<!\\)         # Ensure there's no escaping backslash.
    _{2}            # Match "_" twice.
    ([^\s_].*?)     # CAPTURE GROUP | Match first character that is not "_" or a whitespace,
                    # then match between 0 and ∞ characters, as few times as possible.
    (?<![\\\s_])    # Ensure there's no escaping backslash, whitespace, or "_".
    _{2}            # Match "_" twice.""", re.VERBOSE)

REGEX_CODE = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    `{2}        # Match "`" twice.
    \ *         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP | Match between 1 and ∞ characters, as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    (?<!\\)     # Ensure there's no escaping backslash.
    `{2}        # Match "`" twice.
    (?=[^`]|$)  # Make sure there is a line end or a character other than "`" ahead.
    |           # OR
    (?<!\\)     # Ensure there's no escaping backslash.
    `           # Match "`" once.
    \ *         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP | Match between 1 and ∞ characters, as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    (?<!\\)     # Ensure there's no escaping backslash.
    `           # Match "`" once.
    (?=[^`]|$)  # Make sure there is a line end or a character other than "`" ahead.""", re.VERBOSE)

REGEX_ESCAPED_CHARACTER = re.compile(r"""
    \\  # Match "\" once.
    (.) # Match any character once.""", re.VERBOSE)

REGEX_HEADING = re.compile(r"""
    ((^|>|-|[0-9][.)])\ *)  # CAPTURE GROUP | Match either line start, ">", "-", or a number followed by "." or ")",
                            # then, match between 0 and ∞ whitespaces.
    (\#{1,6})               # CAPTURE GROUP | Match "#" between 1 and 6 times.
    \ +                     # Match between 1 and ∞ whitespaces.
    ([^\s].*?)              # CAPTURE GROUP | Match first character that is not a whitespace,
                            # then match between 0 and ∞ characters, as few times as possible.
    (\ *)                   # Match between 0 and ∞ whitespaces.
    $                       # Match line end.""", re.VERBOSE)

REGEX_HORIZONTAL_RULE = re.compile(r"""
    ^       # Match line start.
    \ *     # Match between 0 and ∞ whitespaces.
    \*{3,}  # Match "*" at least 3 times.
    \ *     # Match between 0 and ∞ whitespaces.
    $       # Match line end.
    |       # OR
    ^       # Match line start.
    \ *     # Match between 0 and ∞ whitespaces.
    -{3,}   # Match "-" at least 3 times.
    \ *     # Match between 0 and ∞ whitespaces.
    $       # Match line end.
    |       # OR
    ^       # Match line start.
    \ *     # Match between 0 and ∞ whitespaces.
    _{3,}   # Match "_" at least 3 times.
    \ *     # Match between 0 and ∞ whitespaces.
    $       # Match line end.""", re.VERBOSE)

REGEX_IMAGE = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    !           # Match "!" once.
    \[          # Match "[" once.
    \ *         # Match between 0 and ∞ whitespaces.
    ([^]]+?)    # CAPTURE GROUP | Match between 1 and ∞ characters,
                # as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    ]           # Match "]" once.
    \(          # Match "(" once.
    \ *         # Match between 0 and ∞ whitespaces.
    ([^)]+?)    # CAPTURE GROUP | Match between 1 and ∞ characters,
                # as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    [\"']       # Match either "'" or '"' once.
    (.+?)       # CAPTURE GROUP | Match between 1 and ∞ characters,
                # as few times as possible.
    [\"']       # Match either "'" or '"' once.
    \ *         # Match between 0 and ∞ whitespaces.
    \)          # Match ")" once.
    |           # OR
    (?<!\\)     # Ensure there's no escaping backslash.
    !           # Match "!" once.
    \[          # Match "[" once.
    \ *         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP | Match between 1 and ∞ characters,
                # as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    ]           # Match "]" once.
    \(          # Match "(" once.
    \ *         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP | Match between 1 and ∞ characters,
                # as few times as possible.
    \ *         # Match between 0 and ∞ whitespaces.
    \)          # Match ")" once.""", re.VERBOSE)

REGEX_ITALIC = re.compile(r"""
    (?<!\\)         # Ensure there's no escaping backslash.
    \*              # Match "*" once.
    ([^\s*].*?)     # CAPTURE GROUP | Match first character that is not "*" or a whitespace,
                    # then match between 0 and ∞ characters, as few times as possible.
    (?<![\\\s*])    # Ensure there's no escaping backslash, whitespace, or "*".
    \*              # Match "*" once.
    |               # OR
    (?<!\\)         # Ensure there's no escaping backslash.
    _               # Match "_" once.
    ([^\s_].*?)     # CAPTURE GROUP | Match first character that is not "_" or a whitespace,
                    # then match between 0 and ∞ characters, as few times as possible.
    (?<![\\\s_])    # Ensure there's no escaping backslash, whitespace, or "_".
    _               # Match "_" once.""", re.VERBOSE)

REGEX_LINK = re.compile(r"""
    (?<!\\) # Ensure there's no escaping backslash.
    \[      # Match "[" once.
    \ *     # Match between 0 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    ]       # Match "]" once.
    \(      # Match "(" once.
    \ *     # Match between 0 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    [\"']   # Match either '"' or "'" once.
    \ *     # Match between 0 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    [\"']   # Match either '"' or "'" once.
    \ *     # Match between 0 and ∞ whitespaces.
    \)      # Match ")" once.
    |       # OR
    (?<!\\) # Ensure there's no escaping backslash.
    \[      # Match "[" once.
    \ *     # Match between 0 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    ]       # Match "]" once.
    \(      # Match "(" once.
    \ *     # Match between 0 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    \)      # Match ")" once.""", re.VERBOSE)

REGEX_ORDERED_LIST = re.compile(r"""
    ^       # Match line start.
    (\ +)?  # CAPTURE GROUP | Match between 1 and ∞ whitespaces,
            # as many times as possible, as either one or zero matches.
    [0-9]+  # Match between 1 and ∞ numbers.
    [.)]    # Match either "." or ")" once.
    \ +     # Match between 1 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    $       # Match line end.""", re.VERBOSE)

REGEX_UNORDERED_LIST = re.compile(r"""
    ^       # Match line start.
    (\ +)?  # CAPTURE GROUP | Match between 1 and ∞ whitespaces,
            # as many times as possible, as either one or zero matches.
    [-*+]+  # Match between 1 and ∞ "-", "*", or "+".
    \ +     # Match between 1 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP | Match between 1 and ∞ characters,
            # as few times as possible.
    \ *     # Match between 0 and ∞ whitespaces.
    $       # Match line end.""", re.VERBOSE)

# Tags that do not need be enclosed in <p> tags:
INDEPENDENT_TAGS = (
    "<h",           # Headings and horizontal rules.
    "<a",           # Links.
    "<img",         # Images.
    "<code",        # Code.
    "<blockquote",  # Blockquotes.
)


# Class for nested tags, such as <ol>, <ul>, and <blockquote>.
class NestedTag:
    """
    An HTML tag that may have multiple levels of nesting.

    E.g.,
    <ul>
        <ul>
            <ul>
                <li>This is a list item.</li>
            </ul>
        </ul>
    </ul>
    """

    def __init__(self, regex, opening_tag, inner_opening_tag):
        """
        Initialize a new nested tag.

        Args:
            regex (re.Pattern): RegEx to use. E.g., re.compile(r"^.*$").
            opening_tag (str): Main, outer opening tag. E.g., "<ul>".
            inner_opening_tag (str): Secondary, inner opening tag. E.g., "<li>".
        """

        self.levels = []
        self.regex = regex
        self.opening_tag = opening_tag
        self.closing_tag = opening_tag.replace("<", "</")
        self.inner_opening_tag = inner_opening_tag
        self.inner_closing_tag = inner_opening_tag.replace("<", "</")


# Initialize nested tags.
TAG_BLOCKQUOTE = NestedTag(REGEX_BLOCKQUOTE, "<blockquote>", "<p>")
TAG_ORDERED_LIST = NestedTag(REGEX_ORDERED_LIST, "<ol>", "<li>")
TAG_UNORDERED_LIST = NestedTag(REGEX_UNORDERED_LIST, "<ul>", "<li>")


def open_nested_tag(line, tag):
    """
    Converts Markdown into HTML for nested tags, based on the level of the last
    consecutive element using the same tag, opening a new tag if current level is greater
    than the last, and closing last tag if current level is lesser than the last.

    E.g.,
        > Quote Level 1
        Becomes:

        <blockquote>
            <p>Quote Level 1</p>

        > Quote Level 1
        >> Quote Level 2
        > Quote Level 1
        Becomes (after function runs on the three lines):

        <blockquote>
            <p>Quote Level 1</p>
            <blockquote>
                <p>Quote Level 2</p>
            </blockquote>
            <p>Quote Level 1</p>

        > Quote Level 1
        >> Quote Level 2
        >>> Quote Level 3
        >>>> Quote Level 4
        Becomes (after function runs on the four lines):

        <blockquote>
            <p>Quote Level 1</p>
            <blockquote>
                <p>Quote Level 2</p>
                <blockquote>
                    <p>Quote Level 3</p>
                    <blockquote>
                        <p>Quote Level 4</p>

    Args:
        line (str): Line to convert. E.g., "> Quote Level 1".
        tag (NestedTag): Tag to use. E.g., `TAG_BLOCKQUOTE`.

    Returns:
        new_line (str) : Converted string.
    """

    new_line = ""

    # Initialize last and current levels.
    try:
        last_level = tag.levels[-1]
    except IndexError:
        last_level = 0
    try:
        # 1 is added to ensure current level is never less than 1.
        current_level = len(tag.regex.match(line)[1]) + 1
    except TypeError:
        current_level = 1

    # If current level is greater than last level,
    # add main opening tag along with inner tags to line, and append current level to levels.
    if current_level > last_level:
        new_line = tag.regex.sub(
            f"{tag.opening_tag}{tag.inner_opening_tag}\\2{tag.inner_closing_tag}", line)
        tag.levels.append(current_level)

    # If current level is lesser than last level,
    # go through levels, closing tags until a level is not greater than current level.
    elif current_level < last_level:
        for level in reversed(tag.levels):
            if level > current_level:
                new_line += tag.closing_tag
                tag.levels.remove(level)
            else:
                break
        new_line += tag.regex.sub(
            f"{tag.inner_opening_tag}\\2{tag.inner_closing_tag}", line)

    # If current level is the same as last level,
    # just add inner tags to the line.
    else:
        new_line = tag.regex.sub(
            f"{tag.inner_opening_tag}\\2{tag.inner_closing_tag}", line)
    return new_line


def close_nested_tag(tag):
    """
    Returns line with required amount of closing tags based on level of the last
    element using the same tag and clears tag level.

    E.g.,
                    </blockquote>
                </blockquote>
            </blockquote>
        </blockquote>

    Args:
        tag (NestedTag): Tag to use. E.g., TAG_BLOCKQUOTE.

    Returns:
        new_line (str): Closing tags.
    """

    new_line = len(tag.levels) * tag.closing_tag
    tag.levels[:] = []
    return new_line


def line_is_paragraph(line):
    """
    Checks if a line is a paragraph.

    Args:
        line (str): Line to check.

    Returns:
        bool: Whether or not the line is a paragraph.
    """

    # A paragraph can start with a "<br>", but not just be a "<br>".
    return line.strip() not in ("", "<br>") and not line.lstrip().startswith(INDEPENDENT_TAGS)


def convert(string):
    """
    Converts Markdown into HTML.

    Args:
        string (str): Markdown code to be converted.

    Returns:
        new_string (str): HTML code.
    """

    # If string is empty, just return it.
    if string.strip() == "":
        return ""

    # Initialize variables.
    new_string = ""
    open_paragraph = False
    add_line_break = False

    # Ensure string ends with a newline, this prevents inconsistencies.
    while string.splitlines()[-1] != "":
        string += "\n"

    # For each line in string:
    for line in string.splitlines():
        # Reset `new_line`.
        new_line = ""

        # Add horizontal rules.
        line = REGEX_HORIZONTAL_RULE.sub("<hr>", line)

        # Add emphasis.
        # The order here is important, otherwise "**bold**" would be converted to
        # "*<em>bold</em>*", instead of "<strong>bold</strong>".
        line = REGEX_BOLD.sub("<strong>\\1\\2</strong>", line)
        line = REGEX_ITALIC.sub("<em>\\1\\2</em>", line)

        # Add code.
        line = REGEX_CODE.sub("<code>\\1\\2</code>", line)

        # Add images and links.
        # The order here is important, otherwise images wouldn't work.
        if REGEX_IMAGE.search(line):
            # Check if image has a title.
            if REGEX_IMAGE.search(line)[3]:
                line = REGEX_IMAGE.sub(
                    "<img src=\"\\2\\5\" alt=\"\\1\\4\" title=\"\\3\">", line)
            else:
                line = REGEX_IMAGE.sub(
                    "<img src=\"\\2\\5\" alt=\"\\1\\4\">", line)
        if REGEX_LINK.search(line):
            # Check if link has a title.
            if REGEX_LINK.search(line)[3]:
                line = REGEX_LINK.sub(
                    "<a href=\"\\2\\5\" title=\"\\3\">\\1\\4</a>", line)
            else:
                line = REGEX_LINK.sub("<a href=\"\\2\\5\">\\1\\4</a>", line)

        # Add headings.
        if REGEX_HEADING.search(line):
            heading_level = len(REGEX_HEADING.search(line.lstrip())[3])
            line = REGEX_HEADING.sub(
                f"\\1<h{heading_level}>\\4</h{heading_level}>\\5", line)

        # Line is an unordered list.
        if REGEX_UNORDERED_LIST.search(line.lstrip()):
            new_line = open_nested_tag(line, TAG_UNORDERED_LIST)

        # Line is not an unordered list, but there are still open <ul> tags.
        elif len(TAG_UNORDERED_LIST.levels) > 0:
            new_line = close_nested_tag(
                TAG_UNORDERED_LIST) + (f"<p>{line}</p>"if line_is_paragraph(line) else line)

        # Line is an ordered list.
        elif REGEX_ORDERED_LIST.search(line):
            new_line = open_nested_tag(line, TAG_ORDERED_LIST)

        # Line is not an ordered list, but there are still open <ol> tags.
        elif len(TAG_ORDERED_LIST.levels) > 0:
            new_line = close_nested_tag(
                TAG_ORDERED_LIST) + (f"<p>{line}</p>"if line_is_paragraph(line) else line)

        # Line is a blockquote.
        elif REGEX_BLOCKQUOTE.search(line):
            new_line = open_nested_tag(line, TAG_BLOCKQUOTE)

        # Line is not a blockquote, but there are still open <blockquote> tags.
        elif len(TAG_BLOCKQUOTE.levels) > 0:
            new_line = close_nested_tag(
                TAG_BLOCKQUOTE) + (f"<p>{line}</p>"if line_is_paragraph(line) else line)

        # Line is a paragraph.
        elif line_is_paragraph(line):
            if not open_paragraph:
                open_paragraph = True
                new_line = f"<p>{line.lstrip()}"
            else:
                new_line = line

        # Nothing above applies.
        else:
            new_line += line

        # Escape characters.
        if REGEX_ESCAPED_CHARACTER.search(new_line):
            new_line = REGEX_ESCAPED_CHARACTER.sub("\\1", new_line)

        # Add line breaks.
        if add_line_break:
            new_line = "<br>" + new_line
            add_line_break = False

        # Check if a line break should be added.
        if line.lstrip().endswith("  "):
            new_line = new_line.rstrip()
            add_line_break = True

        # Close paragraph.
        if open_paragraph and not line_is_paragraph(new_line):
            open_paragraph = False
            new_line = "</p>" + new_line

        new_string += new_line
    return new_string.strip()


def convert_file(file):
    """
    Opens a Markdown file and returns converted results.

    Args:
        file (TextIO): Markdown file to be converted.

    Returns:
        str: HTML code.
    """

    with open(file) as f:
        return convert(f.read())
