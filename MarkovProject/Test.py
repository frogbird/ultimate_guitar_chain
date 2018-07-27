from pydub import AudioSegment
from pydub.playback import play


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

    big_keyboard = ['A0', 'Bb0', 'B0', 'C1', 'Db1', 'D1', 'Eb1', 'E1',
                    'F1', 'Gb1', 'G1', 'Ab1', 'A1', 'Bb1', 'B1', 'C2',
                    'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2',
                    'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3',
                    'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 'C4',
                    'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4',
                    'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5',
                    'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 'C6',
                    'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6',
                    'A6', 'Bb6', 'B6', 'C7', 'Db7', 'D7', 'Eb7', 'E7',
                    'F7', 'Gb7', 'G7', 'Ab7', 'A7', 'Bb7', 'B7', 'C8']


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

    def play(self, tempo = 200):
        play_progression(self.chords, Notes.flats, tempo)


    def display(self):

        for i in range(0, len(self.modes)):
            print self.names[i], self.modes[i]



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
            new_names.append(chord_name(chord, self.notes))
        return new_names

    def display(self):

        print self.key + ' ' + self.style

        i = 0

        while(i < len(self.modes)):

            print self.chords[i], self.names[i], self.triads[i]

            i = i + 1


    def play(self, tempo = 200):
        play_progression(self.triads, self.notes, tempo)


'''
Functions for creating scales and modes
'''


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
    chord = [
        scale[0],
        scale[2],
        scale[4]]

    return chord


def jazz_triad_7th(scale):
    chord = [
        scale[0],
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
                       (0, 5, 7, 13): "Sus4 Flat9"}

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
                          "Sus4 Flat9": (0, 5, 7, 13)}


    chord_mode_dictionary = {"Minor": Mode.aeolian,
                             "Dominant Seven": Mode.mixolydian,
                             "Minor Seven": Mode.dorian,
                             "Major Seven": Mode.ionian,
                             "Major Seven Sharp Eleven": Mode.locrian,
                             "Sus4 flat9": Mode.phrygian,
                             "Half-diminished Seven": Mode.locrian}





# Add something to deal with input of something that isnt a chord????
def chord_name(chord, notes):
    i = notes.index(chord[0])

    intervals = []

    for note in chord:
        j = i
        temp_interval = 0
        while (notes[j] != note):
            j = (j + 1) % 12
            temp_interval = temp_interval + 1
        intervals.append(temp_interval)

    tup_int = tuple(intervals)
    temp = ChordDict.Name_Dictionary[tup_int]

    return chord[0] + " " + temp


def keyboard_chord(chord, notes):
    i = notes.index(chord[0])

    intervals = []

    for note in chord:
        j = i
        temp_interval = 0
        while notes[j] != note:
            j = (j + 1) % 12
            temp_interval = temp_interval + 1
        intervals.append(temp_interval)

    # intervals
    # find starting note
    new_chord = []
    starting_index = Notes.big_keyboard.index(chord[0] + '3')

    for interval in intervals:
        new_chord.append(Notes.big_keyboard[starting_index + interval])

    return new_chord


def give_chord_numbers(key, style, notes, list_of_chord_names):
    prog = Progression(key, style, notes, [1, 2, 3, 4, 5, 6, 7])
    temp = []

    for chord in list_of_chord_names:
        i = prog.names.index(chord)
        temp.append(i + 1)

    return temp


def give_notes(chord_name, notes):
    temp = chord_name.partition(" ")

    key = temp[0]
    chord_type = temp[2]

    i = notes.index(key)
    temp2 = ChordDict.Reverse_Dictionary[chord_type]

    final = [notes[((i + interval) % 12)] for interval in temp2]

    return final



# make the sequence of chords all start in the lower octave and then continue up to the higher octave
# voicings are more accurate


'''Sound Stuff'''


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0  # ms
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size

    return trim_ms


def remove_leading_silence(sound):
    start_trim = detect_leading_silence(sound)
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration]
    return trimmed_sound


'''Creates fixed length chord'''


def create_playable_chord_generic(chord, tempo):
    # make adjustment here #
    sounds = []
    adjusted_chord = keyboard_chord(chord, Notes.flats)
    for note in adjusted_chord:
        path = "/Users/mwparas/Documents/Python/Chord_Project/Pitches2/" + note + ".wav"
        sounds.append(AudioSegment.from_file(path))

    # sounds = [remove_leading_silence(sound) for sound in sounds]

    first = sounds.pop(0)

    while len(sounds) > 0:
        temp = sounds.pop(0)
        first = first.overlay(temp)

    whole_note = 4 / (tempo / 60)

    silence = AudioSegment.silent(duration=whole_note * 1000)
    final = silence.overlay(first)

    return final


def play_progression(progression, notes, tempo = 200):
    chords = []
    for chord in progression:
        print chord_name(chord, Notes.flats), chord
        # print chord.list_of_notes, chord.name
        chords.append(create_playable_chord_generic(chord, tempo))

    first = chords.pop(0)

    while len(chords) > 0:
        temp = chords.pop(0)
        first = first.append(temp, crossfade=0)

    play(first)



# Cost Function
# Moves from chord to chord and creates a recommended set of notes to use
# Next set of notes is dependent on what was previously played, to create something that logistically makes sense


# Enter Chord progression

# Give options for something simple, like Bb blues

# Display possible notes in each of the chords

# Provide interactive experience, select notes that want to start and end on

# Create cost function for possible notes, as in create weighting that changes from measure to measure


def chord_to_mode(chord_name):
    temp = chord_name.partition(" ")

    key = temp[0]
    chord_type = temp[2]

    temp2 = ChordDict.chord_mode_dictionary[chord_type]

    return give_mode(key, Notes.flats, temp2)








if __name__ == '__main__':

    test = CustomProgression(["Bb Minor Seven", "G Dominant Seven", "C Minor Seven", "F Dominant Seven"])

    test.display()

    #test.play()

    #test2 = Progression("A", "Mixolydian", Notes.flats, [1, 5, 6, 3, 4, 1, 4, 5, 1])

    #test2.display()

    #test2.play()


