import random
import numpy as np


def get_random_number(likelihoods):
    rand_num = random.random()

    s = 0
    for i in range(len(likelihoods)):
        s += likelihoods[i]
        if rand_num <= s:
            return i

    return 0


def get_request(request_type, all_requests):
    for r in all_requests:
        if all_requests[r].type == request_type:
            return all_requests[r]


def get_service(service_type, all_services):
    for s in all_services:
        if all_services[s].type == service_type:
            return all_services[s]


def get_exp_sample(mean, samples_num=1):
    return np.random.exponential(mean, samples_num)


def convert_to_minute(seconds):
    # return int(seconds / 60)
    return seconds / 60
