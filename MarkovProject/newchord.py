from __future__ import division
import random 
from markov_thing import create_probabilities

from numpy.random import choice
import pickle


'''
Fixed Database information for reference
'''

Notes_Flats = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

Notes_Sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

Big_Keyboard = ['A0', 'Bb0', 'B0', 'C1', 'Db1', 'D1', 'Eb1', 'E1', 
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

harmonic_minor = [0, 2, 3, 5, 7, 8, 11 ,12]
jazz_minor = [0, 2, 3, 5, 7, 9, 11, 12]

ionian = [0, 2, 4, 5, 7, 9, 11 ,12]
dorian = [2, 4, 5, 7, 9, 11 ,12, 2]
phyrgian = [4, 5, 7, 9, 11 ,12, 2, 4]
lydian = [5, 7, 9, 11 ,12, 2, 4, 5]
mixolydian = [7, 9, 11 ,12, 2, 4, 5, 7]
aeolian = [9, 11 ,12, 2, 4, 5, 7, 9]
locrian = [11 ,12, 2, 4, 5, 7, 9, 11]

modes = [ionian, dorian, phyrgian, lydian, mixolydian, aeolian, locrian]


'''
Functions for creating scales and modes
'''
def Give_Mode(name, notes, mode):

	i = notes.index(name)

	scale = [notes[((i + interval) % 12)] for interval in mode]

	return scale

def Major(key, notes):

	prog = [Give_Mode(key, notes, mode) for mode in modes]

	return prog

def Minor(key, notes):
	i = notes.index(key)
	newKey = notes[(i + 3) % 12]

	startIndex = modes.index(aeolian)
	rotatedModes = modes[startIndex: ] + modes[:startIndex]

	prog = [Give_Mode(newKey, notes, mode) for mode in rotatedModes]

	return prog 

def Jazz_Minor(key, notes):
	i = notes.index(key)

	temp = modes

	temp[0] = jazz_minor

	for mode in temp:
		mode = [3 if x==4 else x for x in mode]

	prog = [Give_Mode(key, notes, mode) for mode in temp]

	return prog 

	# create new mode set with adjusted minor third
'''
def Harmonic_Minor(key, notes):
	i = notes.index(key)

	temp = modes

	temp[0] = jazz_minor

	for mode in temp:
		mode = [3 if x==4 else x for x in mode]

	prog = [Give_Mode(key, notes, mode) for mode in temp]

	return prog 
'''


def Mixolydian(key, notes):
	i = notes.index(key)
	newKey = notes[(i + 5) % 12]

	startIndex = modes.index(mixolydian)
	rotatedModes = modes[startIndex: ] + modes[:startIndex]

	prog = [Give_Mode(newKey, notes, mode) for mode in rotatedModes]

	return prog 

def Phyrgian(key, notes):
	i = notes.index(key)
	newKey = notes[(i + 8) % 12]

	startIndex = modes.index(phyrgian)
	rotatedModes = modes[startIndex: ] + modes[:startIndex]

	prog = [Give_Mode(newKey, notes, mode) for mode in rotatedModes]

	return prog 


def Simple_Triad(scale):
	chord = [
		scale[0],
		scale[2],
		scale[4]]

	return chord

def Jazz_Triad_7th(scale):
	chord = [
		scale[0],
		scale[2],
		scale[4],
		scale[6]]

	return chord




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
					(0, 3, 6, 10): "Half-diminshed Seven",
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
					(0, 4, 7, 11, 18): "Major Seven Sharp Eleven"}

Reverse_Dictionary = {"Minor": (0, 3, 7),
					"Dim": (0, 3, 6),
					"Major": (0, 4, 7),
					"Aug": (0, 4, 8),
					"Dominant Seven": (0, 4, 7, 10),
					"Minor Seven": (0, 3, 7, 10),
					"Major Seven": (0, 4, 7, 11),
					"Aug Minor Seven": (0, 4, 8, 10),
					"Diminished Seven": (0, 3, 6, 9),
					"Half-diminshed Seven": (0, 3, 6, 10),
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
					"Major Seven Sharp Eleven": (0, 4, 7, 11, 18)}

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
						"7sus2": "7Sus2"}

# Give name of a chord based on input of notes
# chord->[list of notes]
# notes->[white and black keys (flat or sharp)]


# Add something to deal with input of something that isnt a chord????
def Chord_name(chord, notes):

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
	temp = Name_Dictionary[tup_int]

	return chord[0] + " " + temp

def Keyboard_Chord(chord, notes):

	i = notes.index(chord[0])

	intervals = []

	for note in chord:
		j = i
		temp_interval = 0
		while(notes[j] != note):
			j = (j + 1) % 12
			temp_interval = temp_interval + 1
		intervals.append(temp_interval)

	# intervals
	# find starting note
	new_chord = []
	starting_index = Big_Keyboard.index(chord[0] + '3')

	for interval in intervals:
		new_chord.append(Big_Keyboard[starting_index + interval])

	return new_chord


def Create_Prog(key, style, notes, chords, seventh):
	temp = Progression(key, style, notes, chords)
	temp.generate_modes()
	temp.generate_triads(seventh)
	temp.give_names()

	return temp


def Give_Chord_Numbers(key, style, notes, list_of_chord_names):
	prog = Create_Prog(key, style, notes, [1, 2, 3, 4, 5, 6, 7])
	temp = []

	for chord in list_of_chord_names:
		i = prog.names.index(chord)
		temp.append(i + 1)

	return temp


def Give_Notes(chord_name, notes):

	temp = chord_name.partition(" ")

	key = temp[0]
	chord_type = temp[2]


	i = notes.index(key)
	temp2 = Reverse_Dictionary[chord_type]

	final = [notes[((i + interval) % 12)] for interval in temp2]


	return final 

def Special_Name(chord_name):

	slash = False

	if '/' in chord_name:

		slash = True

		temp = chord_name.partition('/')

		root = temp[-1]

		if root in Notes_Sharps:

			new_index = Notes_Sharps.index(root)

			root = Notes_Flats[new_index]


		chord_name = temp[0]

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

	chord_type = Unique_Name_Dictionary[new_name]

	key = chord_name.replace(new_name, '')

	if key in Notes_Sharps:

		i = Notes_Sharps.index(key)
	
	else:

		i = Notes_Flats.index(key)

	temp2 = Reverse_Dictionary[chord_type]

	final = [Notes_Flats[((i + interval) % 12)] for interval in temp2]

	chord_object = Chord(final, chord_name)


	# put key identifier function here 
	# make note if it is slash on the object
	# when determining the key->check if the root is the root, if not  

	if(slash):
		chord_object.add_note_to_beginning(root)

	chord_object.make_flats()

	return chord_object


def Generator_1(number):
	temp = [2, 3, 4, 5, 6, 7]
	output = []

	i = number - 3

	while(i > 0):
		output.append(random.choice(temp))
		i = i - 1

	output.insert(0, 1)
	output.append(5)
	output.append(1)

	return output

def Generator_2():
	temp = [1, 2, 3, 4, 5, 6, 7]

	return random.choice(temp)

'''
def Create_Melody(prog):
	output = []
	for mode in prog.modes:
		output.append(mode[Generator_2()])
	return output
'''


class Chord:
	def __init__ (self, list_of_notes, name):
		self.name = name
		self.list_of_notes = list_of_notes
		self.root = list_of_notes[0]

	def add_note_to_beginning(self, note):
		self.list_of_notes.insert(0, note)

	def make_flats(self):

		for note in self.list_of_notes:

			if note in Notes_Sharps:

				temp = Notes_Sharps.index(note)

				note = Notes_Flats[temp]


class Ultimate_Guitar_Progression:

	def __init__(self, chord_objects, key, numerals):

		self.chords = chord_objects

		self.key = key

		self.numerals = numerals


	def add_progression(self, url):

		self.url = url

	def play(self, tempo):

		play_progression(self.chords, Notes_Flats, tempo)

	def add_probabilities(self):

		self.numeral_matrix = create_probabilities(self.numerals)

		names = []

		for chord in self.chords:

			names.append(chord.name)

		self.chord_matrix = create_probabilities(names)




#Progression Class:

class Progression:
	def __init__ (self, key, style, notes, chords):
		self.key = key
		self.style = style
		self.notes = notes
		self.chords = chords #list
		self.modes = []
		self.triads = []
		self.names = []


	def add_chords_to_progression(self, chords):
		for number in chords:
			self.chords.append(number)


	def generate_modes(self):
		if self.style == "minor" or self.style == "Minor":
			temp = Minor(self.key, self.notes)
			for chords in self.chords:
				self.modes.append(temp[chords - 1])

		elif self.style == "mix" or self.style == "Mix":
			temp = Mixolydian(self.key, self.notes)
			for chords in self.chords:
				self.modes.append(temp[chords - 1])

		elif self.style == "phrygian" or self.style == "Phrygian":
			temp = Phyrgian(self.key, self.notes)
			for chords in self.chords:
				self.modes.append(temp[chords - 1])

		elif self.style == "Jazz Minor" or self.style == "jazz minor":
			temp = Jazz_Minor(self.key, self.notes)
			for chords in self.chords:
				self.modes.append(temp[chords - 1])

		else:
			temp = Major(self.key, self.notes)
			for chords in self.chords:
				self.modes.append(temp[chords - 1])


	def generate_triads(self, style):
		if style == "seventh":
			for mode in self.modes:
				self.triads.append(Jazz_Triad_7th(mode))
		else:
			for mode in self.modes:
				self.triads.append(Simple_Triad(mode))

	def give_names(self):
		for chord in self.triads:
			self.names.append(Chord_name(chord, self.notes))

	def play(self, tempo):
		play_progression(self.triads, self.notes, tempo)



# make the sequence of chords all start in the lower octave and then continue up to the higher octave
# voicings are more accurate 


'''Sound Stuff'''

from pydub import AudioSegment
from pydub.playback import play
import time

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size

    return trim_ms


def remove_leading_silence(sound):
	start_trim = detect_leading_silence(sound)
	duration = len(sound)
	trimmed_sound = sound[start_trim:duration]
	return trimmed_sound

'''Creates fixed length chord'''
def Create_playable_chord_generic(chord, tempo):
	# make adjustment here #
	sounds = []
	adjusted_chord = Keyboard_Chord(chord, Notes_Flats)
	for note in adjusted_chord:
		path = "/Users/mwparas/Documents/Python/Chord_Project/Pitches2/" + note + ".wav"
		sounds.append(AudioSegment.from_file(path))

	# sounds = [remove_leading_silence(sound) for sound in sounds]

	first = sounds.pop(0)

	while len(sounds) > 0:
		temp = sounds.pop(0)
		first = first.overlay(temp)

	whole_note = 4 / (tempo / 60)

	silence = AudioSegment.silent(duration=whole_note*1000)
	final = silence.overlay(first)

	return final 


def play_progression(progression, notes, tempo):
	chords = []
	for chord in progression:
		# print Chord_name(chord, Notes_Flats), chord
		print chord.list_of_notes, chord.name
		chords.append(Create_playable_chord_generic(chord.list_of_notes, tempo))

	first = chords.pop(0)

	while len(chords) > 0:
		temp = chords.pop(0)
		first = first.append(temp, crossfade=0)

	play(first)



import requests
from bs4 import BeautifulSoup



def scraper(website):

	page = requests.get(website)

	soup = BeautifulSoup(page.content, 'html.parser')

	junk = soup.find_all(class_="js-tab-content")

	spans = junk[0].find_all('span')

	Chords = []

	for span in spans:

		temp = str(span.get_text())
		Chords.append(temp)

	return Chords






def information_getter(list_of_chord_objects):

	list_of_chords = []

	list_of_roots = []

	for chord in list_of_chord_objects:

		list_of_chords.append(chord.list_of_notes)

		list_of_roots.append(chord.root)

	all_notes = sum(list_of_chords, [])

	list_of_notes = list(set(all_notes))

	tupl_counts = []

	counts = []

	for note in list_of_notes:

		temp = all_notes.count(note)

		tupl_counts.append((note, temp))

		counts.append(temp)

	#### new thing

	tupl_counts = sorted(tupl_counts, key=lambda x: x[1])

	tupl_counts.reverse()


	tupl_lengths = []

	lengths = []

	possible_keys = []

	for note in Notes_Flats:

		scale = Give_Mode(note, Notes_Flats, ionian)

		temp = set(scale).intersection(list_of_notes)

		lengths.append(len(temp))

		tupl_lengths.append((note, len(temp)))

	intersections = max(lengths)

	for pair in tupl_lengths:

		if pair[1] == intersections:

			possible_keys.append(pair[0])
	
	if len(possible_keys) == 1:
		
		major_key = possible_keys[0]

	else:

		narrowing = []

		for note in possible_keys:

			for pair in tupl_counts:

				if note == pair[0]:

					narrowing.append(pair)

		narrowing = sorted(narrowing, key=lambda x: x[1])

		narrowing.reverse()

		major_key = narrowing[0][0]

	major_scale = Give_Mode(major_key, Notes_Flats, ionian)

	minor_scale = Give_Mode(major_key, Notes_Flats, aeolian)

	major_numeral = []

	minor_numeral = []

	for note in list_of_roots:

		if note in major_scale and note in minor_scale:

			minor_numeral.append(minor_scale.index(note) + 1)

			major_numeral.append(major_scale.index(note) + 1)

	numerals = [1, 2, 3, 4, 5, 6, 7]

	minor_counts = []

	major_counts = []

	for numeral in numerals:

		count_minor = minor_numeral.count(numeral)

		count_major = major_numeral.count(numeral)

		minor_counts.append((numeral, count_minor))

		major_counts.append((numeral, count_major))

	# print minor_numeral

	if major_counts[0][1] > minor_counts[0][1]:

		final_key = major_key + ' ' + 'Major'

		return Ultimate_Guitar_Progression(list_of_chord_objects, final_key, major_numeral)

	else:

		final_key = minor_scale[0] + ' ' + 'Minor'

		return Ultimate_Guitar_Progression(list_of_chord_objects, final_key, minor_numeral)


	## determine if the key is major or minor 



def overall_product(url):

	temp = scraper(url)

	list_of_chord_objects = []

	for chord in temp:

		list_of_chord_objects.append(Special_Name(chord))

	progression_from_url = information_getter(list_of_chord_objects)

	progression_from_url.add_progression(url)

	progression_from_url.add_probabilities()

	return progression_from_url







def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result





'''
frank_zappa = pickle.load(open("frank_zappa", "rb"))
genesis = pickle.load(open("genesis", "rb"))
led_zeppelin = pickle.load(open("led_zeppelin", "rb"))
rush = pickle.load(open("rush", "rb"))
the_beatles = pickle.load(open("the_beatles", "rb"))
the_eagles = pickle.load(open("the_eagles", "rb"))



test_data = merge_dicts(frank_zappa, genesis, led_zeppelin, rush, the_beatles, the_eagles)


pickle.dump(test_data, open("test_data", "wb"))
'''
'''

test_data = pickle.load(open("test_data", "rb"))

temp = map_name_to_object(test_data)

pickle.dump(temp, open("name_map", "wb"))
'''


'''

random_everything = big_generate_progressions(first_order_probability_dictionary, second_order_probability_dictionary, count_probability_dictionary, name_map)

test_stuff = []

for chord in random_everything:

	test_stuff.append(Special_Name(chord))

product = information_getter(test_stuff)

product.play(300)

'''



def scraper_number2(url):

	page = requests.get(url)

	# print page.status_code

	soup = BeautifulSoup(page.content, 'html.parser')

	# temp = "https://tabs.ultimate-guitar.com/g/genesis/"

	# temp = "https://tabs.ultimate-guitar.com/m/misc_soundtrack/"

	# temp = "https://tabs.ultimate-guitar.com/f/frank_zappa/"

	# temp = "https://tabs.ultimate-guitar.com/t/the_beatles/"

	# temp = "https://tabs.ultimate-guitar.com/l/led_zeppelin/"

	temp = "https://tabs.ultimate-guitar.com/e/eagles/"

	links = []

	for a in soup.find_all('a', href=True):

   		# print "Found the URL:", a['href']

   		test = a['href']


   		if temp in test:

   			test = str(test)

   			links.append(test)


	return links



def scrape_and_save(url):

	links = scraper_number2(url)

	progression_dictionary = {}

	for link in links:

		try:
			
			test = link 

			# temp = test.replace("https://tabs.ultimate-guitar.com/g/genesis/", '')

			# temp = test.replace("https://tabs.ultimate-guitar.com/m/misc_soundtrack/", '')

			# temp = test.replace("https://tabs.ultimate-guitar.com/f/frank_zappa/", '')

			#temp = test.replace("https://tabs.ultimate-guitar.com/t/the_beatles/", '')

			# temp = test.replace("https://tabs.ultimate-guitar.com/l/led_zeppelin/", '')

			temp = test.replace("https://tabs.ultimate-guitar.com/e/eagles/", '')

			temp = temp.replace("_crd.htm", '') 

			name = temp

			print "trying " + name + "\n"

			progression_dictionary[name] = overall_product(link)

			print "Success! Sleeping..." + "\n"

			time.sleep(30)

		except:

			print "Failed on " + link + "\n"

			time.sleep(30)


	return progression_dictionary



def go_ahead_and_get_data(url, number_of_pages, name):

	test = scrape_and_save(url)

	for i in range(2, number_of_pages + 1):

		link = "https://www.ultimate-guitar.com/tabs/eagles_chords_tabs" + str(i) + ".htm"

		temp = scrape_and_save(link)

		test = merge_dicts(test, temp)

	
	pickle.dump(test, open(name, "wb"))


# go_ahead_and_get_data("https://www.ultimate-guitar.com/tabs/the_beatles_chords_tabs.htm", 13, "the_beatles")



# go_ahead_and_get_data("https://www.ultimate-guitar.com/tabs/genesis_chords_tabs.htm", 2, "genesis")


# print overall_product("https://tabs.ultimate-guitar.com/g/genesis/a_trick_of_the_tail_crd.htm")




# go_ahead_and_get_data("https://www.ultimate-guitar.com/tabs/eagles_chords_tabs.htm", 3, "the_eagles")



def transpose_and_store(progression):

	#test_data = {name -> progression}

	key = progression.key

	temp = key.partition(' ')

	key_note = temp[0]

	chord_list = []

	for chord in progression.chords:

		new_chord = chord

		new_chord.make_flats

		chord_list.append(new_chord)

	final = []

	i = Notes_Flats.index(key_note)

	for chord in chord_list:

		intervals = []

		for note in chord.list_of_notes:

			if note not in Notes_Flats:

				raise Exception('For some reason, this chord had notes that did not exist!')

			j = i

			temp_interval = 0

			while(Notes_Flats[j] != note):
			
				j = (j + 1) % 12

				temp_interval = temp_interval + 1

			intervals.append(temp_interval)

		intervals = tuple(intervals)

		set_of_final = (intervals)

		final.append(set_of_final)

	return final




def read_and_give_notes(transposition, key):

	transposed_chord_progression = []

	i = Notes_Flats.index(key)

	for chord_formula in transposition:

		final = [Notes_Flats[((i + interval) % 12)] for interval in chord_formula]

		transposed_chord_progression.append(final)

	return transposed_chord_progression






def overall_tranposer(data_set):

	new_dictionary = {}

	total_size = len(data_set)

	for key in data_set:

		try:

			print key, total_size

			current_progression = data_set[key]

			new_dictionary[key] = transpose_and_store(current_progression)

			total_size = total_size - 1

		except:

			print "failed on ", key

	return new_dictionary




# new thing to get markov'd -> make sequence for each chord consisting of (position, (intervals for chords))



def test_play_progression(progression, tempo):
	chords = []
	for chord in progression:
		# print Chord_name(chord, Notes_Flats), chord
		print chord
		chords.append(Create_playable_chord_generic(chord, tempo))

	first = chords.pop(0)

	while len(chords) > 0:
		temp = chords.pop(0)
		first = first.append(temp, crossfade=0)

	play(first)


#testing_things = read_and_give_notes(temp,'Gb')

#test_play_progression(testing_things, 250)


# test_data = pickle.load(open("test_data", "rb"))

# test = test_data['firth_of_fifth']

'''

chords = test.chords

empty = []

for chord in chords:

	empty.append(chord.list_of_notes)

print empty
'''

# print transpose_and_store(test)

def find_most_common_chords(chord_dictionary):

	count_dictionary = {}

	for key in chord_dictionary.keys():

		progression = chord_dictionary[key]

		for chord in progression:

			if chord not in count_dictionary.keys():

				count_dictionary[chord] = 1 / len(progression)

			else:
				
				count_dictionary[chord] = count_dictionary[chord] + (1 / len(progression))

	return count_dictionary


def probability_counts(chord_dictionary):

	count_dictionary = find_most_common_chords(chord_dictionary)

	total_count = 0

	for key in count_dictionary:

		temp = count_dictionary[key]

		total_count = temp + total_count

	for key in count_dictionary:

		count_dictionary[key] = count_dictionary[key] / total_count

	return count_dictionary


def first_order_markov_chain(data_set):

	count_dictionary = {}

	total_unique_stuff = []

	for key in data_set.keys():

		progression = data_set[key]

		for z in range(len(progression) - 2):

			key = (progression[z], progression[z+1])

			if count_dictionary.has_key(key):

				# print key

				count_dictionary[key] = count_dictionary[key] + 1

			else:

				count_dictionary[key] = 1

	iterating_list = count_dictionary.keys()

	for z in iterating_list:

		total_count = 0

		# print total_count

		for key in count_dictionary:

			if z[0] == key[0]:

				total_count = count_dictionary[key] + total_count

		for key in count_dictionary:

			if z[0] == key[0]:

				count_dictionary[key] = count_dictionary[key] / total_count


	return count_dictionary



def second_order_markov_chain(data_set):

	count_dictionary = {}

	total_unique_stuff = []

	for key in data_set.keys():

		progression = data_set[key]

		for z in range(len(progression) - 2):

			key = ((progression[z], progression[z+1]), progression[z+2])

			if count_dictionary.has_key(key):

				# print key

				count_dictionary[key] = count_dictionary[key] + 1

			else:

				count_dictionary[key] = 1


	iterating_list = count_dictionary.keys()

	for i in iterating_list:

		# print "iterating over ", i

		total_count = 0

		# print total_count

		for key in count_dictionary:

			if i[0] == key[0]:

				total_count = count_dictionary[key] + total_count

		for key in count_dictionary:

				if i[0] == key[0] and total_count != 0:

					count_dictionary[key] = count_dictionary[key] / total_count


	return count_dictionary



def big_generate_progressions(first_order_probability_dictionary, second_order_probability_dictionary, style):

	'''

	elements_1 = []

	weights_1 = []

	for key in count_probability_dictionary:

		elements_1.append(key)

		weights_1.append(count_probability_dictionary[key])

	first = choice(elements_1, p=weights_1)

	'''

	if style == "Minor" or style == "minor":

		first = (0, 3, 7)

	else:

		first = (0, 4, 7)

	final_progression = [first]

	current = first

	# build second value:

	elements = []

	weights = []

	for key in first_order_probability_dictionary:

		if key[0] == current:

			elements.append(key[1])

			weights.append(first_order_probability_dictionary[key])

	current = choice(elements, p=weights)


	index = 1

	final_progression.append(current)

	# build probability sets here:

	while(len(final_progression) < 10):

		elements2 = []

		weights2 = []

		for key in second_order_probability_dictionary:

			if key[0] == (final_progression[index - 1], final_progression[index]):

				elements2.append(key[1])

				weights2.append(second_order_probability_dictionary[key])


		current = choice(elements, p=weights)

		index = index + 1

		final_progression.append(current)

	final_progression.append(first)


	return final_progression


'''




test_data = pickle.load(open("transposed", "rb"))


first_order_probability_dictionary = first_order_markov_chain(test_data)

pickle.dump(first_order_probability_dictionary, open("new_first_order", "wb"))



second_order_probability_dictionary = second_order_markov_chain(test_data)

pickle.dump(second_order_probability_dictionary, open("new_second_order", "wb"))


count_probability_dictionary = probability_counts(test_data)

pickle.dump(count_probability_dictionary, open("new_probability_counts", "wb"))
'''




first_order_probability_dictionary = pickle.load(open("new_first_order", "rb"))

second_order_probability_dictionary = pickle.load(open("new_second_order", "rb"))



temp = big_generate_progressions(first_order_probability_dictionary, second_order_probability_dictionary, "Major")



new_temp = read_and_give_notes(temp, "Bb")

test_play_progression(new_temp, 250)






'''
test_data = pickle.load(open("genesis", "rb"))

test = test_data['afterglow']

temp = transpose_and_store(test)



# testing_things = read_and_give_notes(temp,'Bb')

test_play_progression(testing_things, 250)

'''

























