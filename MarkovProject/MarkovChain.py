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

            key = (progression[z], progression[z + 1])

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

            key = ((progression[z], progression[z + 1]), progression[z + 2])

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
