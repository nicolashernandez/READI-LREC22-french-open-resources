"""
The common_scores module contains functions allowing to calculate readability scores that use simple formulas: GFI, ARI, FRE, FKGL, SMOG, and REL.

The origin of these formulas, alongside a quick description of what they're meant to measure is presented in each function's documentation.
Functions start with the uppercase acronym, and the suffix '_score'.
"""
import math
import pandas as pd

from ..utils import utils


# Text "must" be a list of sentences, which are lists of words.
def GFI_score(text, statistics=None):
    """
    Outputs the Gunning fog index, a 1952 readability test estimating the years of formal education needed to understand a text on the first reading.
    The scale goes from 6 to 18, starting at the sixth grade in the United States.
    The formula is : 0.4 * ( (words/sentences) + 100 * (complex words / words) )
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Gunning fog index of the current text
    :rtype: float
    """
    # FIXME : this score is wrong since we divided by totalSentences instead of totalWords for the second ratio. Leaving as-is for now.
    if statistics is not None:
        return 0.4*((statistics["totalWords"]/statistics["totalSentences"]) + 100*statistics["totalLongWords"]/statistics["totalSentences"])
    totalWords = 0
    totalSentences = len(text)
    totalLongWords = 0
    for sent in text:
        totalWords += len(sent)
        totalLongWords += len([token for token in sent if len(token)>6])
    if totalWords < 101:
        #print("WARNING : Number of words is less than 100, This score is inaccurate")
        pass
    
    score = 0.4*((totalWords/totalSentences) + 100*totalLongWords/totalSentences)
    return score

def ARI_score(text, statistics=None):
    """
    Outputs the Automated readability index, a 1967 readability test estimating the US grade level needed to comprehend a text
    The scale goes from 1 to 14, corresponding to age 5 to 18.
    The formula is 4.71 * (characters / words) + 0.5 (words / sentences) - 21.43
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Automated readability index of the current text
    :rtype: float
    """
    #FIXME : this score is wrong since we multiplied each ratio by 4.71 instead of doing it only for the first one.
    if statistics is not None:
        return 4.71*((statistics["totalCharacters"]/statistics["totalWords"]) + 0.5*statistics["totalWords"]/statistics["totalSentences"])-21.43
    totalWords = 0
    totalSentences = len(text)
    totalCharacters = 0
    for sent in text:
        totalWords += len(sent)
        totalCharacters += sum(len(token) for token in sent)
    score = 4.71*((totalCharacters/totalWords) + 0.5*totalWords/totalSentences)-21.43
    return score

def FRE_score(text, statistics=None):
    """
    Outputs the Flesch reading ease, a 1975 readability test estimating the US school level needed to comprehend a text
    The scale goes from 100 to 0, corresponding to Grade 5 at score 100, up to post-college below score 30.
    The formula is 206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Flesch reading ease of the current text
    :rtype: float
    """
    if statistics is not None:
        return 206.835-1.015*(statistics["totalWords"]/statistics["totalSentences"])-84.6*(statistics["totalSyllables"]/statistics["totalWords"])
    totalWords = 0
    totalSentences = len(text)
    totalSyllables = 0
    for sent in text:
        totalWords += len(sent)
        totalSyllables += sum(utils.syllablesplit(word) for word in sent)
    score_FRE = 206.835-1.015*(totalWords/totalSentences)-84.6*(totalSyllables/totalWords)
    return(score_FRE)

def FKGL_score(text, statistics=None):
    """
    Outputs the Flesch–Kincaid grade level, a 1975 readability test estimating the US grade level needed to comprehend a text
    The scale is meant to be a one to one representation, a score of 5 means that the text should be appropriate for fifth graders.
    The formula is 0.39 * (total words / total sentences)+11.8*(total syllables / total words) - 15.59
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Flesch–Kincaid grade level of the current text
    :rtype: float
    """
    if statistics is not None:
        return 0.39*(statistics["totalWords"]/statistics["totalSentences"])+11.8*(statistics["totalSyllables"]/statistics["totalWords"])-15.59
    totalWords = 0
    totalSentences = len(text)
    totalSyllables = 0
    for sent in text:
        totalWords += len(sent)
        totalSyllables += sum(utils.syllablesplit(word) for word in sent)
    score_FKGL = 0.39*(totalWords/totalSentences)+11.8*(totalSyllables/totalWords)-15.59
    return(score_FKGL)

def SMOG_score(text, statistics=None):
    """
    Outputs the Simple Measure of Gobbledygook, a 1969 readability test estimating the years of education needed to understand a text
    The scale is meant to be a one to one representation, a score of 5 means that the text should be appropriate for fifth graders.
    The formula is 1.043 * Square root (Number of polysyllables * (30 / number of sentences)) + 3.1291
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Simple Measure of Gobbledygook of the current text
    :rtype: float
    """
    # FIXME : the nbPolysyllables erroneously returns their own number of syllables instead of incrementing the counter by one.
    # Keeping as is for now
    if statistics is not None:
        return 1.043*math.sqrt(statistics["nbPolysyllables"]*(30/statistics["totalSentences"]))+3.1291
    totalSentences = len(text)
    nbPolysyllables = 0
    for sent in text:
        nbPolysyllables += sum(utils.syllablesplit(word) for word in sent if utils.syllablesplit(word)>=3)
        #nbPolysyllables += sum(1 for word in sent if utils.syllablesplit(word)>=3)
    score_SMOG = 1.043*math.sqrt(nbPolysyllables*(30/totalSentences))+3.1291
    return(score_SMOG)

def REL_score(text, statistics=None):
    """
    Outputs the Reading Ease Level, an adaptation of Flesch's reading ease for the French language,
    with changes to the coefficients taking into account the difference in length between French and English words.
    The formula is 207 - 1.015 * (Number of words / Number of sentences) - 73.6 * (Number of syllables / Number of words)
        
    :param text: Content of a text, distincting between sentences.
    :type text: list(list(str)) or str 
    :param statistics: Refers to a readability.Statistics attribute, containing various pre-calculated information such as totalWords.
    :type statistics: readability.Statistics
    :return: The Simple Measure of Gobbledygook of the current text
    :rtype: float
    """
    if statistics is not None:
        return 207-1.015*(statistics["totalWords"]/statistics["totalSentences"])-73.6*(statistics["totalSyllables"]/statistics["totalWords"])
    totalWords = 0
    totalSentences = len(text)
    totalSyllables = 0
    for sent in text:
        totalWords += len(sent)
        totalSyllables += sum(utils.syllablesplit(word) for word in sent)
    score_REL = 207-1.015*(totalWords/totalSentences)-73.6*(totalSyllables/totalWords)
    return(score_REL)