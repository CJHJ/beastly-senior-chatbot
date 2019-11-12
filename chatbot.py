# -*- coding: utf-8 -*-
import codecs
from random import randint

import pyaudio
import wave
import time
import os
import glob

import math as math
import random as random

import pygame as pg
import time

from pykakasi import kakasi
from pathlib import Path

# windows : change / into \\

# dictionary class


class DictChain(object):
    def __init__(self, curChain, nextChain, entry="", response=""):
        self.currentChain = curChain
        self.nextChain = nextChain
        self.entry = entry
        self.response = response

    def __repr__(self):
        return 'Entry(%r, %r, %r, %r)' % (self.currentChain, self.nextChain, self.entry, self.response)

# main chatbot class


class YugeChatBot(object):
    # initialize chatbot class
    def __init__(self):
        # username and last response
        self.userName = ""
        self.lastResponse = ""

        # Goodbye responses
        self.byeResponses = ["bye", "bye-bye", "バイバイ"]

        # dictionaries
        self.dictionaries = []
        self.dictionaryNumber = 0
        self.currentChain = "000"

        # angry dictionary
        self.angryDict = {}
        self.angryPercentage = 0.0

        # syllables sounds
        self.syllables = glob.glob("./sounds/*.wav")
        # clean syllables list
        self.syllables = [entry.replace("./sounds/", "").replace(
            ".wav", "") for entry in self.syllables]
        # put n into the very back to prevent it from being checked first
        nIndex = self.syllables.index("n")
        self.syllables.append(self.syllables.pop(nIndex))

        # Initiate pygame mixer
        pg.mixer.init()
        pg.init()

        self.player = {}

        for i in range(len(self.syllables)):
            self.player[self.syllables[i]] = pg.mixer.Sound(
                "./sounds/"+self.syllables[i]+".wav")

        pg.mixer.set_num_channels(50)

    # get saved dictionaries
    def getDictionary(self):
        self.dictionaries = []
        fileRelativePath = "./dictionary/"
        dictionaryFiles = [fileRelativePath+"dictionary01.txt", fileRelativePath+"dictionary02.txt",
                           fileRelativePath+"dictionary03.txt", fileRelativePath+"dictionary04.txt"]

        for dictionaryFile in dictionaryFiles:
            fileContent = codecs.open(
                dictionaryFile, 'rb', 'utf-8').readlines()

            # initialize dictionary and insert lines
            dictionary = []
            for lines in fileContent:
                entry = lines.replace(u'\ufeff', '').replace(
                    "\n", "").replace("\r", "").split("\t")
                print(entry)

                if entry[1].isdigit():
                    dictSingleChain = DictChain(
                        entry[0], entry[1], entry[2], entry[3])
                else:
                    dictSingleChain = DictChain(
                        entry[0], "end", entry[1], "end")

                dictionary.append(dictSingleChain)

            # append entry to global dictionary list
            self.dictionaries.append(dictionary)

        print(self.dictionaries)

        # populate angry dictionary
        angryFile = "angry.txt"
        angryFileContent = codecs.open(
            fileRelativePath+angryFile, 'rb', 'utf-8').readlines()
        for lines in angryFileContent:
            entry = lines.replace(u'\ufeff', '').replace(
                "\n", "").replace("\r", "").split("\t")
            print(entry)

            if str(entry[0]) not in self.angryDict:
                self.angryDict[str(entry[0])] = [entry[1]]
            else:
                self.angryDict[str(entry[0])].append(entry[1])

        print(self.angryDict)

    # sequence a speech from entry
    def makeSpeech(self, entry):
        # Converting text into romaji
        kakasiInstance = kakasi()
        kakasiInstance.setMode('H', 'a')
        kakasiInstance.setMode('K', 'a')
        kakasiInstance.setMode('J', 'a')
        kakasiInstance.setMode("r", "Kunrei")
        conv = kakasiInstance.getConverter()
        convertedText = conv.do(entry)
        print(convertedText)

        # search syllables and play corresponding sound
        # keep searching until string is exhausted
        while convertedText != "":
            # for every registered syllable
            syllableFound = False
            for syllable in self.syllables:
                if convertedText.startswith(syllable):
                    convertedText = convertedText[len(syllable):]
                    syllableFound = True

                    # play corresponding sound
                    # self.playSound(syllable)
                    self.player[syllable].play()
                    time.sleep(0.3)

                    break
            # prevent unregistered syllable from clogging the process
            if syllableFound == False:
                convertedText = convertedText[1:]

    # play dictionary sound
    def playDictionaryWave(self):

        # define stream chunk
        chunk = 1024

        dictNum = self.dictionaryNumber+1

        # open a wav format music
        f = wave.open(r"./sounds/dict"+str(dictNum) +
                      "/"+self.currentChain+".wav", "rb")

        # instantiate PyAudio
        p = pyaudio.PyAudio()

        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

    # play designated sound (using pyaudio)
    def playSound(self, syllables):

        # define stream chunk
        chunk = 1024

        # open a wav format music
        f = wave.open(r"./sounds/"+syllables+".wav", "rb")

        # instantiate PyAudio
        p = pyaudio.PyAudio()

        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()

    # start introduction
    def startIntro(self, name):
        # initialize dictionary
        self.getDictionary()

        # assign name
        self.userName = name

        # randomize a number and get random dictionary
        self.dictionaryNumber = randint(0, len(self.dictionaries)-1)

        self.makeSpeech(u"ほお、")
        self.currentChain = self.dictionaries[self.dictionaryNumber][0].currentChain
        soundFile = Path(
            "./sounds/dict"+str(self.dictionaryNumber+1)+"/"+self.currentChain+".wav")
        print(soundFile)
        if soundFile.is_file():
            self.playDictionaryWave()
        else:
            self.makeSpeech(self.dictionaries[self.dictionaryNumber][0].entry)

        reply = "ほお、"+self.userName+"、" + \
            self.dictionaries[self.dictionaryNumber][0].entry

        # start conversation loop
        return reply

    # get reply from inputted text
    # return end condition and response
    def getReply(self, inputText):
        self.lastResponse = inputText

        # check whether response is not in goodbye responses.
        # if not, run main response checker.
        if any(self.lastResponse.lower() in response for response in self.byeResponses):
            print("元気でな。")
            self.makeSpeech(u"元気でな。")
            return (True, "元気でな。")
        else:
            responseFoundFlag = False

            # find response and change current chain number
            for response in self.dictionaries[self.dictionaryNumber]:
                if self.lastResponse.lower() == response.response and self.currentChain == response.currentChain:
                    self.currentChain = response.nextChain
                    print("Debug >> chain number changed = "+response.nextChain)
                    responseFoundFlag = True
                    break

            # if response not found, get angry!
            if responseFoundFlag is False:
                # increase angry level!
                self.increaseAngry()

                angryString = self.angryResponse()
                print(angryString)
                self.makeSpeech(angryString)
                return (False, angryString)
            else:
                # decrease angry level!
                self.decreaseAngry()

                # init candidates
                candidates = []
                for response in self.dictionaries[self.dictionaryNumber]:
                    if self.currentChain == response.currentChain:
                        candidates.append(response)

                # print candidate entry
                print(candidates[0].entry)

                # play speech according to selected candidate
                # self.playSound("a")
                soundFile = Path(
                    "./sounds/dict"+str(self.dictionaryNumber+1)+"/"+self.currentChain+".wav")
                if soundFile.is_file():
                    self.playDictionaryWave()
                else:
                    self.makeSpeech(candidates[0].entry)

                # if candidate has no next chain
                if candidates[0].response == "end":
                    return (True, candidates[0].entry)

                return (False, candidates[0].entry)

    # return angry phrase
    def angryResponse(self):
        angryLevel = int(math.ceil(self.angryPercentage*5))

        print("angry level = "+str(angryLevel) +
              ", angry percentage = "+str(self.angryPercentage)+"%")

        return random.choice(self.angryDict[str(angryLevel)])

    # increase angry percentage
    def increaseAngry(self):
        if self.angryPercentage < 1.0:
            self.angryPercentage += 0.05
        else:
            self.angryPercentage = 1.0

    # decrease angry percentage
    def decreaseAngry(self):
        if self.angryPercentage > 0.0:
            self.angryPercentage -= 0.05
        else:
            self.angryPercentage = 0.0

    # start loop
    def startLoop(self):
        # keep looping chatbot
        while True:
            print('>> ', end="", flush=True)

            # get response
            self.lastResponse = input()
