"""
Convert MS streams subtitles(vtt) to human readable text.

To conver all vtt files inside a directory:
find . -name "*.vtt" -exec python vtt2text.py {} \;
"""

import sys
import re

tags = [
        r'</v>',
        r'<v .*>',
        r'<v\w{2}>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',
        r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',
        r'(\d{2}:\d{2}):\d{2}\.\d{3} --> (\d{2}:\d{2}):\d{2}\.\d{3}'
    ]

def remove_tags(text, tags):
    """
    Remove vtt markup tags
    """
    for pat in tags:
        text = re.sub(pat, '', text)
        print(pat)
        print(len(text))

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)

    return text

def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in ('##', 'Language: en', 'WEBVTT', 'NOTE'):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match('^\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            yield '\n' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer

def remove_meta_data(vtt_file, keepSpeakers):
    if keepSpeakers:
        if (r'<v .*>') in tags:
            tags.remove(r'<v .*>')
    else:
        if (r'<v .*>') not in tags:
            tags.append(r'<v .*>')

    text = remove_tags(vtt_file, tags)
    lines = text.splitlines()
    lines = remove_header(lines)
    lines = merge_duplicates(lines)
    lines = list(lines)
    lines = [x for x in lines if not x.startswith("NOTE Confidence:")]
    #lines = merge_short_lines(lines)
    lines = list(lines)
    return lines

def main():
    vtt_file_name = sys.argv[1]
    txt_name =  re.sub(r'.vtt$', '.txt', vtt_file_name)
    with open(vtt_file_name) as f:
        text = f.read()

    lines = remove_meta_data(text, False)
    #print(lines)
    with open(txt_name, 'w') as f:
        for line in lines:
            f.write(line)
            f.write("\n")

if __name__ == "__main__":
    main()