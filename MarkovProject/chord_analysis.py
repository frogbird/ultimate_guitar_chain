# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:57:54 2018

@author: Matthew Paras
"""
import json
import os
from sklearn.linear_model import LogisticRegression
import numpy as np
from random import shuffle

# Contains interval information for each mode, as well as a "modes" list
class Mode(object):
    harmonic_minor = [0, 2, 3, 5, 7, 8, 11, 12]
    jazz_minor = [0, 2, 3, 5, 7, 9, 11, 12]

    ionian = [0, 2, 4, 5, 7, 9, 11, 12]
    dorian = [2, 4, 5, 7, 9, 11, 12, 2]
    phrygian = [4, 5, 7, 9, 11, 12, 2, 4]
    lydian = [5, 7, 9, 11, 12, 2, 4, 5]
    mixolydian = [7, 9, 11, 12, 2, 4, 5, 7]
    aeolian = [9, 11, 12, 2, 4, 5, 7, 9]
    locrian = [11, 12, 2, 4, 5, 7, 9, 11]

    modes = [ionian, dorian, phrygian, lydian, mixolydian, aeolian, locrian]


# basic keyboard information for creating chords and playback
class Notes(object):
    flats = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


class Chord(object):
    def __init__(self, list_of_notes, name):
        self.name = name
        self.list_of_notes = list_of_notes
        self.root = list_of_notes[0]

    def add_note_to_beginning(self, note):
        self.list_of_notes.insert(0, note)

    def make_flats(self):
        for note in self.list_of_notes:
            if note in Notes.sharps:
                temp = Notes.sharps.index(note)
                note = Notes.flats[temp]


class CustomProgression(object):
    def __init__(self, list_of_names):
        self.names = list_of_names
        self.chords = self.generate_notes()
        self.modes = self.map_chords_modes()

    def generate_notes(self):
        chord_output = [give_notes(name, Notes.flats) for name in self.names]
        return chord_output

    def map_chords_modes(self):
        mode_output = [chord_to_mode(name for name in self.names)]
        return mode_output

    def display(self):
        for i in range(0, len(self.modes)):
            print(self.names[i], self.modes[i])


# Progression Class:
class Progression(object):
    def __init__(self, key, style, notes, chords, triads="normal"):
        self.key = key
        self.style = style
        self.notes = notes
        self.chords = chords  # list
        self.modes = self.generate_modes()
        self.triads = self.generate_triads(triads)
        self.names = self.give_names()

    def add_chords_to_progression(self, chords):
        for number in chords:
            self.chords.append(number)
            # update chords

    def generate_modes(self):
        if self.style == "minor" or self.style == "Minor":
            scale = minor(self.key, self.notes)
            new_modes = []
            for chords in self.chords:
                new_modes.append(scale[chords - 1])
            return new_modes

        elif self.style == "mixolydian" or self.style == "Mixolydian":
            scale = give_mixolydian(self.key, self.notes)
            new_modes = []
            for chords in self.chords:
                new_modes.append(scale[chords - 1])
            return new_modes

        elif self.style == "phrygian" or self.style == "Phrygian":
            scale = give_phyrgian(self.key, self.notes)
            new_modes = []
            for chords in self.chords:
                new_modes.append(scale[chords - 1])
            return new_modes

        elif self.style == "Jazz Minor" or self.style == "jazz minor":
            scale = give_jazz_minor(self.key, self.notes)
            new_modes = []
            for chords in self.chords:
                new_modes.append(scale[chords - 1])
            return new_modes

        else:
            scale = major(self.key, self.notes)
            new_modes = []
            for chords in self.chords:
                new_modes.append(scale[chords - 1])
            return new_modes

    def generate_triads(self, style):
        new_triads = []
        if style == "seventh":
            for mode in self.modes:
                new_triads.append(jazz_triad_7th(mode))
            return new_triads
        else:
            for mode in self.modes:
                new_triads.append(simple_triad(mode))
        return new_triads

    def give_names(self):
        new_names = []
        for chord in self.triads:
            new_names.append(give_chord_name(chord, self.notes))
        return new_names

    def display(self):
        print(self.key + ' ' + self.style)
        for i in range(0, len(self.modes)):
            print(self.chords[i], self.names[i], self.triads[i])


# Functions for creating scales and modes
def give_mode(name, notes, mode):
    i = notes.index(name)
    scale = [notes[((i + interval) % 12)] for interval in mode]
    return scale


def major(key, notes):
    prog = [give_mode(key, notes, mode) for mode in Mode.modes]
    return prog


def minor(key, notes):
    i = notes.index(key)
    newKey = notes[(i + 3) % 12]
    startIndex = Mode.modes.index(Mode.aeolian)
    rotatedModes = Mode.modes[startIndex:] + Mode.modes[:startIndex]
    prog = [give_mode(newKey, notes, mode) for mode in rotatedModes]
    return prog


def give_jazz_minor(key, notes):
    temp = Mode.modes
    temp[0] = Mode.jazz_minor
    for mode in temp:
        mode = [3 if x == 4 else x for x in mode]
    prog = [give_mode(key, notes, mode) for mode in temp]
    return prog


def give_mixolydian(key, notes):
    i = notes.index(key)
    newKey = notes[(i + 5) % 12]
    startIndex = Mode.modes.index(Mode.mixolydian)
    rotatedModes = Mode.modes[startIndex:] + Mode.modes[:startIndex]
    prog = [give_mode(newKey, notes, mode) for mode in rotatedModes]
    return prog


def give_phyrgian(key, notes):
    i = notes.index(key)
    newKey = notes[(i + 8) % 12]
    startIndex = Mode.modes.index(Mode.phrygian)
    rotatedModes = Mode.modes[startIndex:] + Mode.modes[:startIndex]
    prog = [give_mode(newKey, notes, mode) for mode in rotatedModes]
    return prog


def simple_triad(scale):
    chord = [scale[0],
             scale[2],
             scale[4]]
    return chord


def jazz_triad_7th(scale):
    chord = [scale[0],
             scale[2],
             scale[4],
             scale[6]]
    return chord


class ChordDict(object):
    '''Dictionaries for naming chords'''

    Name_Dictionary = {(0, 3, 7): "Minor",
                       (0, 3, 6): "Dim",
                       (0, 4, 7): "Major",
                       (0, 4, 8): "Aug",
                       (0, 4, 7, 10): "Dominant Seven",
                       (0, 3, 7, 10): "Minor Seven",
                       (0, 4, 7, 11): "Major Seven",
                       (0, 4, 8, 10): "Aug Minor Seven",
                       (0, 3, 6, 9): "Diminished Seven",
                       (0, 3, 6, 10): "Half-diminished Seven",
                       (0, 5, 7): "Sus4",
                       (0, 2, 7): "Sus2",
                       (0, 5, 10): "Quartal",
                       (0, 5, 7, 10): "7Sus4",
                       (0, 2, 7, 10): "7Sus2",
                       (0, 5, 7, 10, 2): "9Sus4",
                       (0, 4, 7, 9): "Major Sixth",
                       (0, 4, 7, 8): "Minor Sixth",
                       (0, 3, 7, 11): "Major Minor Seventh",
                       (0, 4, 7, 14): "Major Nine",
                       (0, 2, 4, 7): "add9",
                       (0, 3, 7, 2): "Minor Nine",
                       (0, 7): "5",
                       (0, 3, 7, 10, 14, 17): "Minor Eleventh",
                       (0, 4, 7, 11, 14, 17): "Major Eleventh",
                       (0, 4, 7, 10, 14, 17): "Dominant Eleventh",
                       (0, 4, 7, 10, 14, 17, 19): "Dominant Thirteenth",
                       (0, 2, 7, 11): "Major Seven Sus2",
                       (0, 5, 7, 11): "Major Seven Sus4",
                       (0, 4, 7, 11, 18): "Major Seven Sharp Eleven",
                       (0, 5, 7, 13): "Sus4 Flat9",
                       (0, 2, 3, 4): "add4"}

    Reverse_Dictionary = {"Minor": (0, 3, 7),
                          "Dim": (0, 3, 6),
                          "Major": (0, 4, 7),
                          "Aug": (0, 4, 8),
                          "Dominant Seven": (0, 4, 7, 10),
                          "Minor Seven": (0, 3, 7, 10),
                          "Major Seven": (0, 4, 7, 11),
                          "Aug Minor Seven": (0, 4, 8, 10),
                          "Diminished Seven": (0, 3, 6, 9),
                          "Half-diminished Seven": (0, 3, 6, 10),
                          "Sus4": (0, 5, 7),
                          "Sus2": (0, 2, 7),
                          "Quartal": (0, 5, 10),
                          "7Sus4": (0, 5, 7, 10),
                          "7Sus2": (0, 2, 7, 10),
                          "9Sus4": (0, 5, 7, 10, 2),
                          "Major Sixth": (0, 5, 7, 9),
                          "Minor Sixth": (0, 5, 7, 8),
                          "Major Minor Seventh": (0, 3, 7, 11),
                          "Major Nine": (0, 4, 7, 14),
                          "add9": (0, 2, 4, 7),
                          "Minor Nine": (0, 3, 7, 14),
                          "5": (0, 7),
                          "Minor Eleventh": (0, 3, 7, 10, 14, 17),
                          "Major Eleventh": (0, 4, 7, 11, 14, 17),
                          "Dominant Eleventh": (0, 4, 7, 10, 14, 17),
                          "Dominant Thirteenth": (0, 4, 7, 10, 14, 19),
                          "Major Seven Sus2": (0, 2, 7, 11),
                          "Major Seven Sus4": (0, 5, 7, 11),
                          "Major Seven Sharp Eleven": (0, 4, 7, 11, 18),
                          "Sus4 Flat9": (0, 5, 7, 13),
                          "add4": (0, 2, 3, 4)}

    chord_mode_dictionary = {"Minor": Mode.aeolian,
                             "Dominant Seven": Mode.mixolydian,
                             "Minor Seven": Mode.dorian,
                             "Major Seven": Mode.ionian,
                             "Major Seven Sharp Eleven": Mode.locrian,
                             "Sus4 flat9": Mode.phrygian,
                             "Half-diminished Seven": Mode.locrian}

    Unique_Name_Dictionary = {"m": "Minor",
                              "dim": "Dim",
                              '': "Major",
                              #(0, 4, 8): "Aug",
                              "7": "Dominant Seven",
                              "m7": "Minor Seven",
                              #(0, 4, 7, 11): "Major Seven",
                              #(0, 4, 8, 10): "Aug Minor Seven",
                              #(0, 3, 6, 9): "Diminished Seven",
                              #(0, 3, 6, 10): "Half-diminshed Seven",
                              "sus4": "Sus4",
                              "sus2": "Sus2",
                              "sus": "Sus4",
                              #(0, 5, 10): "Quartal",
                              "7sus4": "7Sus4",
                              "7sus": "7Sus4",
                              "9": "Major Nine",
                              "maj9": "Major Nine",
                              "m9": "Minor Nine",
                              "add9": "add9",
                              "maj7": "Major Seven",      
                              #(0, 5, 7, 10, 2): "9Sus4",
                              "6" : "Major Sixth",
                              "m6": "Minor Sixth",
                              "mmaj7": "Major Minor Seventh",
                              "M7": "Major Seven",
                              #"7M": "Major Seven",
                              "dim7": "Diminished Seven",
                              "5": "5",
                              "Maj9": "Nine",
                              "2": "Sus2",
                              "4": "Sus4",
                              "madd9": "Minor Nine",
                              "madd11": "Minor Eleventh",
                              "add11": "Major Eleventh",
                              "11": "Dominant Eleventh",
                              "13": "Dominant Thirteenth",
                              "m7add11": "Minor Eleventh",
                              "maj7sus2": "Major Seven Sus2",
                              "maj7sus4": "Major Seven Sus4",
                              "7Sus2": "7Sus2",
                              "7sus2": "7Sus2",
                              "add4": "add4"}





# Give name of a chord based on input of notes
# chord->[list of notes]
# notes->[white and black keys (flat or sharp)]
# Add something to deal with input of something that isnt a chord????
def give_chord_name(chord, notes):
    i = notes.index(chord[0])
    intervals = []
    for note in chord:
        j = i
        temp_interval = 0
        while(notes[j] != note):
            j = (j + 1) % 12
            temp_interval = temp_interval + 1
        intervals.append(temp_interval)
    tup_int = tuple(intervals)
    temp = Mode.Name_Dictionary[tup_int]
    return chord[0] + " " + temp


def give_chord_numbers(key, style, notes, list_of_chord_names):
    prog = Progression(key, style, notes, [1, 2, 3, 4, 5, 6, 7])
    chord_num = [prog.names.index(chord) + 1 for chord in list_of_chord_names]
    return chord_num


def give_notes(chord_name, notes):
    temp = chord_name.partition(" ")
    key = temp[0]
    chord_type = temp[2]
    i = notes.index(key)
    temp2 = ChordDict.Reverse_Dictionary[chord_type]
    final = [notes[((i + interval) % 12)] for interval in temp2]
    return final


def chord_to_mode(chord_name):
    temp = chord_name.partition(" ")
    key = temp[0]
    chord_type = temp[2]
    temp2 = ChordDict.chord_mode_dictionary[chord_type]
    return give_mode(key, Notes.flats, temp2)


def Special_Name(chord_name):
    slash = False
    if '/' in chord_name:
        slash = True
        split_chord = chord_name.partition('/')
        root = split_chord[-1]
        if root in Notes.sharps:
            new_index = Notes.sharps.index(root)
            root = Notes.flats[new_index]
        chord_name = split_chord[0]
    unique = []
    #########################
    modifiers = ['di', 'm', 'M', 'aj', 'add', '5', '6', '7', '9', '11', '13','sus', '2', '4']
    for modifier in modifiers:
        if modifier != '' and modifier in chord_name:
            if modifier == 'm' and 'mm' in chord_name:
                unique.append('mm')
            else:
                unique.append(modifier)
    new_name = ''.join(unique)
    chord_type = ChordDict.Unique_Name_Dictionary[new_name]
    key = chord_name.replace(new_name, '')
    if key in Notes.sharps:
        i = Notes.sharps.index(key)    
    else:
        i = Notes.flats.index(key)
    temp2 = ChordDict.Reverse_Dictionary[chord_type]
    final = [Notes.flats[((i + interval) % 12)] for interval in temp2]
    chord_object = Chord(final, chord_name)


    # put key identifier function here 
    # make note if it is slash on the object
    # when determining the key->check if the root is the root, if not  

    if(slash):
        chord_object.add_note_to_beginning(root)

    chord_object.make_flats()

    return chord_object


def transpose_and_store(progression):
    #test_data = {name -> progression}
    key = progression.key
    key_note = key.partition(' ')[0]
    chord_list = []
    for chord in progression.chords:
        new_chord = chord
        new_chord.make_flats
        chord_list.append(new_chord)
    final = []
    i = Notes.flats.index(key_note)
    for chord in chord_list:
        intervals = []
        for note in chord.list_of_notes:
            if note not in Notes.flats:
                raise Exception('For some reason, this chord had notes that did not exist!')
            j = i
            temp_interval = 0
            while(Notes.flats[j] != note):
                j = (j + 1) % 12
                temp_interval = temp_interval + 1
            intervals.append(temp_interval)
        intervals = tuple(intervals)
        set_of_final = (intervals)
        final.append(set_of_final)
    return final


def open_file(path):
    json1_file = open(path)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    return json1_data


def build_feature_vector(progression):
    reference = {}
    total_count = 1
    for n in Notes.flats:
        reference[n] = 0
    for chord in progression:
        for note in chord:
            reference[note] += 1
            total_count += 1
    feature = np.array([reference[key] for key in reference])
    return feature


def combine_files(path):
    data = []
    for file in os.listdir(path):
        data += open_file(path + "/" + file)
    return data


def combine_folders(path):
    data = []
    for folder in os.listdir(path):
        data += combine_files(path + "/" + folder)
    return data


def parse_prog(data):
    output = []
    labels = []
    error_count = 0
    minor_flats = [x + 'm' for x in Notes.flats]
    minor_sharps = [x + 'm' for x in Notes.sharps]
    flats = Notes.flats + minor_flats
    sharps = Notes.sharps + minor_sharps
    for i in range(len(data)):
        try:
            parsed = [Special_Name(chord).list_of_notes for chord in data[i]['chord_progression']]
            feature = build_feature_vector(parsed)   
            try:
                if data[i]['tonality_name'] in flats:
                    labels.append(flats.index(data[i]['tonality_name']))
                else:
                    labels.append(sharps.index(data[i]['tonality_name']))
                output.append(feature)
            except:
                pass

        except (KeyError, ValueError) as e:
            #print(data[i]['chord_progression'])
            #print("error")
            error_count += 1
            #pass
    
    print(error_count)
    return np.array(output), np.array(labels)


def songs_with_keys(data):
    return [x for x in data if x["tonality_name"] != '']


def find_unique(data):
    unique_dict = {}
    output = []
    for song in data:
        if song['id'] not in unique_dict:
            unique_dict[song['id']] = True
            output.append(song)
    return output

def build_regression(data):
    x, y = parse_prog(data)
    logisticRegr = LogisticRegression(solver = "newton-cg", multi_class = "multinomial")
    print(y)
    logisticRegr.fit(x, y)
    print(logisticRegr.score(x, y))
    return logisticRegr




if __name__ == '__main__':
    
    path = 'f:/WebCrawlers/RockMusic'
    
    #data = combine_folders(path)
    

    #no_duplicates = find_unique(data)
    
    
    #keys = songs_with_keys(no_duplicates)
    
    build_regression(keys)
    
    #print(Special_Name('Ab').list_of_notes)
    
    
    
    #parse_prog(total_data)
    #print(data[0])
    
    #test = Special_Name('Dbm')
    #print(test.name, test.list_of_notes)
    
    #for chord in data[0]['chord_progression']:
        #test = Special_Name(chord)
        #print(test.name, test.list_of_notes)
        
    #total_data = data + data2 + data3

    

    
    #x, y = parse_prog(keys)
    
    #logisticRegr = LogisticRegression(solver = "newton-cg", multi_class = "multinomial")
    

    
    #print(y)
    
    #logisticRegr.fit(x, y)
    
    
    #print(logisticRegr.score(x, y))
    
    
    #print(build_feature_vector(test))
    
    # print(os.listdir())
    
#    for song in data3:
#        if song["tonality_name"] != '':
#            print(song["song_name"], song["tonality_name"])



























