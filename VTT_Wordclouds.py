"""
Using frequency
===============

Using a dictionary of word frequency.
"""

import multidict as multidict

import os
import re
from os import path
from wordcloud import WordCloud

from vtt2text import remove_meta_data

OUTPUT_ = "static/"

def get_speakers_stats_dicts(lines):

    speakers_text_dict = get_speakers_text_dict(lines)

    times_spoken_dict = {}
    word_count_dict = {}
    word_length_dict = {}
    sum_stats_dict = {}

    for key in speakers_text_dict.keys():
        times_spoken_dict[key] = len(speakers_text_dict.getall(key))

        all_words_spoken = ''.join(speakers_text_dict.getall(key))
        word_count_dict[key] = len(all_words_spoken.split())
        word_length_dict[key] = len(all_words_spoken)
        sum_stats_dict[key] = times_spoken_dict[key] + 2 * word_count_dict[key] + 3 * word_length_dict[key]

    return times_spoken_dict, word_count_dict, word_length_dict, sum_stats_dict

def get_speakers_text_dict(lines):
    speakers_dict = multidict.MultiDict()

    for speaker_line in lines:
        speaker = re.search('<v (.*)>', speaker_line).group(1)
        speaker_text = speaker_line.split('>')[1]
        speakers_dict.add(speaker, speaker_text)

    return speakers_dict

def make_image_from_dict(dict, imageName):
    # generate word cloud
    wc = WordCloud(max_font_size=200, relative_scaling=0.7).generate_from_frequencies(frequencies=dict)
    image = wc.to_image()
    image.save(OUTPUT_ + imageName + ".png", "PNG")

def  make_image_from_lines(lines, imageName):
    text = ' '.join(lines)
    wc = WordCloud(max_font_size=80, min_word_length=3).generate(text)
    image = wc.to_image()
    image.save(OUTPUT_ + imageName + ".png", "PNG")

def make_wordclouds(filename):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    vtt = open(path.join(d, 'uploads/' + filename)).read()
    lines = remove_meta_data(vtt, False)
    make_image_from_lines(lines, 'VTT wordcloud')

    speakersLines = remove_meta_data(vtt, True)
    timesSpokenDict, wordCountDict, wordLengthDict, sumStatsDict = get_speakers_stats_dicts(speakersLines)
    make_image_from_dict(timesSpokenDict, 'VTT number of times the speaker spoke')
    make_image_from_dict(wordCountDict, 'VTT number of words the speaker spoke')
    make_image_from_dict(wordLengthDict, 'VTT length of words the speaker spoke')
    make_image_from_dict(sumStatsDict, 'VTT combined stats of speaker')

if __name__ == '__main__':
    make_wordclouds()



