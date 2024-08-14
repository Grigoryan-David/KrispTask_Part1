import io
import os
import re

import requests

GOOGLE_NEWS_URL = "https://news.google.com/news/rss"
byte_stream = io.BytesIO()


############
#
# Cheap Crowdfunding Problem
#
# There is a crowdfunding project that you want to support. This project
# gives the same reward to every supporter, with one peculiar condition:
# the amount you pledge must not be equal to any earlier pledge amount.
#
# You would like to get the reward, while spending the least amount > 0.
#
# You are given a list of amounts pledged so far in an array of integers.
# You know that there is less than 100,000 of pledges and the maximum
# amount pledged is less than $1,000,000.
#
# Implement a function find_min_pledge(pledge_list) that will return
# the amount you should pledge.
#
############


def find_min_pledge(pledge_list: list) -> int:
    pledge_set = set(pledge_list)
    new_pledge = 1
    while new_pledge in pledge_set and new_pledge < 10:
        new_pledge += 1
    if new_pledge == 10:
        return 0
    return new_pledge


assert find_min_pledge([1, 3, 6, 4, 1, 2]) == 5
assert find_min_pledge([1, 2, 3]) == 4
assert find_min_pledge([-1, -3]) == 1
assert find_min_pledge([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 0


############
#
# Extract Titles from RSS feed
#
# Implement get_headlines() function. It should take a url of an RSS feed
# and return a list of strings representing article titles.
#
############


def get_headlines(rss_url: str) -> list:
    response_text = requests.get(rss_url).text
    pattern = re.compile(r'<item><title>\s*(.*?)\s*</title>')
    response = re.findall(pattern, response_text)
    return response


print(get_headlines(GOOGLE_NEWS_URL))


###########

# Streaming Payments Processor
#
# The function `process_payments()` is processing a large, but finite
# amount of payments in a streaming fashion.
#
# It relies on two library functions to do its job. The first function
# `stream_payments_to_storage(storage)` reads the payments from a payment
# processor and writes them to storage by calling `storage.write(buffer)`
# on it's `storage` argument. The `storage` argument is supplied by
# calling `get_payments_storage()` function. The API is defined below.
#
# TODO: Modify `process_payments()` to print a checksum of bytes written
# by `stream_payments_to_storage()`. The existing functionality
# should be preserved.
#
# The checksum is implemented as a simple arithmetic sum of bytes.
#
# For example, if bytes([1, 2, 3]) were written, you should print 6.
#
#
# NOTE: you need to take into account the following restrictions:
# - You are allowed only one call each to `get_payments_storage()` and
# to `stream_payments_to_storage()`
# - You can not read from the storage.
# - You can not use disk as temporary storage.
# - Your system has limited memory that can not hold all payments.

###########


class CheckSum(io.BufferedWriter):
    def __init__(self, raw):
        super().__init__(raw)
        self.checksum = 0

    def write(self, binary_text):
        self.checksum += sum(binary_text)
        return super().write(binary_text)


def get_payments_storage() -> CheckSum:
    return CheckSum(open(os.devnull, 'wb'))


def stream_payments_to_storage(storage: CheckSum):
    for i in range(10):
        storage.write(bytes([1, 2, 3, 4, 5]))


def process_payments():
    storage = get_payments_storage()
    stream_payments_to_storage(storage)
    print(storage.checksum)


process_payments()


############
# Streaming Payments Processor, two vendors edition.
#
# We decided to improve the payment processor from the previous
# exercise and hired two vendors. One was to implement `stream_payments()`
# function, and another `store_payments()` function.
#
# The function `process_payments_2()` is processing a large, but finite
# amount of payments in a streaming fashion.
#
# Unfortunately the vendors did not coordinate their efforts, and delivered
# their functions with incompatible APIs.
#
# TODO: Your task is to analyse the APIs of `stream_payments()` and
# `store_payments()` and to write glue code in `process_payments_2()`
# that allows us to store the payments using these vendor functions.
#
# NOTE: you need to take into account the following restrictions:
# - You are allowed only one call each to `stream_payments()` and
# to `store_payments()`
# - You can not read from the storage.
# - You can not use disk as temporary storage.
# - Your system has limited memory that can not hold all payments.
#
###########


def stream_payments(callback_fn: callable):
    for i in range(10):
        callback_fn(i)


def store_payments(amount_iterator: list):
    for i in amount_iterator:
        print(i)


def callback_fn(amount):
    byte_stream.write(amount.to_bytes(4, 'big'))


def payment_byte_to_int(byte_stream: io.BytesIO) -> list:
    amounts = []
    while True:
        amount = byte_stream.read(4)
        if not amount:
            break
        amounts.append(int.from_bytes(amount, 'big'))
    return amounts


def process_payments_2():
    stream_payments(callback_fn)
    byte_stream.seek(0)
    store_payments(payment_byte_to_int(byte_stream))


process_payments_2()


############
#
# Code Review
#
# Please do a code review for the following snippet.
# Add your review suggestions inline as python comments
#
############


def get_value(data, key, default, lookup=None, mapper=None):
    return_value = data[key]  # better to use get method to handle missing key, return_value = data.get(key, default)
    if return_value is None or return_value == "":  # with get method this is not needed
        return_value = default
    if lookup:
        return_value = lookup[return_value]  # better to use the get method to handle missing key
    if mapper:
        return_value = mapper(return_value)
    return return_value


def ftp_file_prefix(namespace):
    return ".".join(namespace.split(".")[:-1]) + '.ftp'  # better to handle cases if the namespace is empty


def string_to_bool(string):
    if string.lower() == 'true':  # It is better to convert the input string to lowercase once and use it for comparison
        return True
    if string.lower() == 'false':
        return False
    raise ValueError(f'String {string} is neither true nor false')


def config_from_dict(dict):
    # the variable name dict shadows the built-in dict type, it is better to rename it
    namespace = dict['Namespace']

    # it is better to handle missing key error
    return (dict['Airflow DAG'],
            # it is not readable to write this way could have been declared before return
            {"earliest_available_delta_days": 0,
             "lif_encoding": 'json',
             # if the get_value always gets the same dict no need to pass each time,
             # can be declared as a constant and then be used in a function
             "earliest_available_time":
                 get_value(dict, 'Available Start Time', '07:00'),
             "latest_available_time":
                 get_value(dict, 'Available End Time', '08:00'),
             "require_schema_match":
                 get_value(dict, 'Requires Schema Match', 'True',
                           mapper=string_to_bool),
             "schedule_interval":
                 get_value(dict, 'Schedule', '1 7 * * * '),
             "delta_days":
                 get_value(dict, 'Delta Days', 'DAY_BEFORE',
                           lookup=DeltaDays),  # Consider defining DeltaDays
             "ftp_file_wildcard":
                 get_value(dict, 'File Naming Pattern', None),
             "ftp_file_prefix":
                 get_value(dict, 'FTP File Prefix', ftp_file_prefix(namespace)),
             "namespace": namespace
             }
            )
