import logging
import os
import random
import string
""" Collection of generators to be used in templating for test data

Plans: extend these by allowing generators that take generators for input
Example: generators that case-swap
"""

INT32_MAX_VALUE = 2147483647  # Max of 32 bit unsigned int

logger = logging.getLogger('resttest3.generators')

# Character sets to use in text generation, python string plus extras
CHARACTER_SETS = {
    'ascii_letters': string.ascii_letters,
    'ascii_lowercase': string.ascii_lowercase,
    'ascii_uppercase': string.ascii_uppercase,
    'digits': string.digits,
    'hexdigits': string.hexdigits,
    'hex_lower': string.digits + 'abcdef',
    'hex_upper': string.digits + 'ABCDEF',
    'letters': string.ascii_letters,
    'lowercase': string.ascii_lowercase,
    'octdigits': string.octdigits,
    'punctuation': string.punctuation,
    'printable': string.printable,
    'uppercase': string.ascii_uppercase,
    'whitespace': string.whitespace,
    'url.slug': string.ascii_lowercase + string.digits + '-',
    'url.safe': string.ascii_letters + string.digits + '-~_.',
    'alphanumeric': string.ascii_letters + string.digits,
    'alphanumeric_lower': string.ascii_lowercase + string.digits,
    'alphanumeric_upper': string.ascii_uppercase + string.digits
}


def factory_generate_ids(starting_id=1, increment=1):
    """ Return function generator for ids starting at starting_id
        Note: needs to be called with () to make generator """

    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment

    return generate_started_ids


def generator_basic_ids():
    """ Return ids generator starting at 1 """
    return factory_generate_ids(1)()


def generator_random_int32():
    """ Random integer generator for up to 32-bit signed ints """
    system_random = random.SystemRandom()
    while True:
        yield system_random.randint(0, INT32_MAX_VALUE)


def factory_generate_text(legal_characters=string.ascii_letters, min_length=8, max_length=8):
    """ Returns a generator function for text with given legal_characters string and length
        Default is ascii letters, length 8

        For hex digits, combine with string.hexstring, etc
        """
    system_random = random.SystemRandom()  # To Cryptographically secure random

    def generate_text():
        local_min_len = min_length
        local_max_len = max_length
        while True:
            length = system_random.randint(local_min_len, local_max_len)
            array = [system_random.choice(legal_characters) for _ in range(0, length)]
            yield ''.join(array)

    return generate_text


def factory_fixed_sequence(values):
    """ Return a generator that runs through a list of values in order, looping after end """

    def seq_generator():
        my_list = list(values)
        i = 0
        while True:
            yield my_list[i]
            i += 1
            if i == len(my_list):
                i = 0

    return seq_generator


def parse_fixed_sequence(config):
    """ Parse fixed sequence string """
    vals = config['values']
    if not vals:
        raise ValueError('Values for fixed sequence must exist')
    if not isinstance(vals, list):
        raise ValueError('Values must be a list of entries')
    return factory_fixed_sequence(vals)()


def factory_choice_generator(values):
    """ Return a generator that picks values from a list randomly """
    system_random = random.SystemRandom()  # To Cryptographically secure random

    def choice_generator():
        my_list = list(values)
        while True:
            yield system_random.choice(my_list)

    return choice_generator


def parse_choice_generator(config):
    """ Parse choice generator """
    vals = config['values']
    if not vals or (not isinstance(vals, list)):
        raise ValueError('Values must be a list of entries')
    return factory_choice_generator(vals)()


def factory_env_variable(env_variable):
    """ Return a generator function that reads from an environment variable """

    def return_variable():
        variable_name = env_variable
        while True:
            yield os.environ.get(variable_name)

    return return_variable


def factory_env_string(env_string):
    """ Return a generator function that uses OS expand path to expand environment variables in string """

    def return_variable():
        while True:
            yield os.path.expandvars(env_string)

    return return_variable


""" Implements the parsing logic for YAML, and acts as single point for reading configuration """


def parse_random_text_generator(configuration):
    """ Parses configuration options for a random text generator """
    character_set = configuration.get('character_set')

    if character_set:
        character_set = character_set.lower()
        if character_set not in CHARACTER_SETS:
            raise ValueError(
                "Illegal character set name, is not defined: {0}".format(character_set))
        characters = CHARACTER_SETS[character_set]
    else:  # Custom characters listing, not a character set
        characters = configuration.get('characters')

    min_length = int(configuration.get('min_length', 8))
    max_length = int(configuration.get('max_length', 8))
    if not characters:
        return factory_generate_text(min_length=min_length, max_length=max_length)()
    characters = str(characters)

    if configuration.get('length'):
        length = int(configuration.get('length'))
        min_length = length
        max_length = length

    return factory_generate_text(
        legal_characters=characters, min_length=min_length, max_length=max_length)()


# List of valid generator types
GENERATOR_TYPES = {'env_variable',
                   'env_string',
                   'number_sequence',
                   'random_int',
                   'random_text',
                   'fixed_sequence'
                   }

GENERATOR_PARSING = {'fixed_sequence': parse_fixed_sequence}


def register_generator(typename: str, parse_function):
    """ Register a new generator for use in testing
        typename is the new generator type name (must not already exist)
        parse_function will parse a configuration object (dict)
    """
    if not isinstance(typename, str):
        raise TypeError(
            'Generator type name {0} is invalid, must be a string'.format(typename))
    if typename in GENERATOR_TYPES:
        raise ValueError(
            'Generator type named {0} already exists'.format(typename))
    GENERATOR_TYPES.add(typename)
    GENERATOR_PARSING[typename] = parse_function


# Try registering a new generator
register_generator('choice', parse_choice_generator)


def parse_generator(configuration):
    """ Parses a configuration built from yaml and returns a generator
        Configuration should be a map
    """
    from resttest3.utils import Parser
    configuration = Parser.lowercase_keys(Parser.flatten_dictionaries(configuration))
    gen_type = str(configuration.get(u'type')).lower()

    if gen_type not in GENERATOR_TYPES:
        raise ValueError(
            'Generator type given {0} is not valid '.format(gen_type))

    # Do the easy parsing, delegate more complex logic to parsing functions
    if gen_type == 'env_variable':
        return factory_env_variable(configuration['variable_name'])()
    elif gen_type == 'env_string':
        return factory_env_string(configuration['string'])()
    elif gen_type == 'number_sequence':
        start = int(configuration.get('start', 1))
        increment = int(configuration.get('increment', 1))
        return factory_generate_ids(start, increment)()
    elif gen_type == 'random_int':
        return generator_random_int32()
    elif gen_type == 'random_text':
        return parse_random_text_generator(configuration)
    elif gen_type in GENERATOR_TYPES:
        return GENERATOR_PARSING[gen_type](configuration)

    raise Exception("Unknown generator type: {0}".format('gen_type'))
