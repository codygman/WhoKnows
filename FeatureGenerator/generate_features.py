"""
generate_features.py
Ambidextrous

Input: JSON blobs for 2 people
    - person to person_code mapper
    - person to word, word to person - both types of matrices
    - V dimensional vectors, the features would just be words (lowercased and stemmed)

To be run once; does not need to be run live

"""

import sys
import json
from nltk_get_tokens import generate
from collections import defaultdict

def complain_and_die():
    print 'Usage: please supply the name of the raw JSON blobs file'
    sys.exit()

def parse_json(input_file):
    people = defaultdict(dict)
    with open(input_file, 'r') as fh:
        for line in fh:
            person_data = line.strip()[0]
            ID = person_data['ID']
            # Use the following data for other features
            people[ID]['name'] = person_data['name']
            people[ID]['dept'] = person_data['dept']
            people[ID]['data'] = person_data['profile_full_text']
            people[ID]['pic'] = person_data['profile_picture_src']
    return people

def generate_token_vectors(people):
    vectors = {}
    for ID in people:
        vector = generate(people[ID][data])
        vectors[ID]['name'] = people[ID]['name']
        vectors[ID]['tokens'] = vector
    return vectors

def main():
    if len(sys.argv) != 2:
        complain_and_die()
    people = parse_json(sys.argv[1])
    matrix = generate_token_vectors(people)

if __name__ == '__main__':
    main()

