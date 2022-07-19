import simpy
import random
from entities import *
from utils import *

all_requests = []
all_services = []

request_orders = [
    RequestType.mobile_order,
    RequestType.web_order,
    RequestType.message_delivery,
    RequestType.view_info_mobile,
    RequestType.view_info_web,
    RequestType.delivery_request,
    RequestType.followup_order
]

service_orders = [
    ServiceType.restaurant_management,
    ServiceType.customer_management,
    ServiceType.orders_management,
    ServiceType.delivery_communication,
    ServiceType.payment,
    ServiceType.api_gate,
    ServiceType.web_gate,
]


def init_requests():
    requests = {}

    services = {
        RequestType.mobile_order: [ServiceType.api_gate, ServiceType.orders_management, ServiceType.payment],
        RequestType.web_order: [ServiceType.web_gate, ServiceType.orders_management, ServiceType.payment],
        RequestType.message_delivery: [ServiceType.api_gate, ServiceType.customer_management,
                                       ServiceType.delivery_communication],
        RequestType.view_info_mobile: [ServiceType.api_gate, ServiceType.restaurant_management],
        RequestType.view_info_web: [ServiceType.web_gate, ServiceType.restaurant_management],
        RequestType.delivery_request: [ServiceType.web_gate, ServiceType.restaurant_management,
                                       ServiceType.delivery_communication],
        RequestType.followup_order: [ServiceType.api_gate, ServiceType.orders_management]
    }

    priorities = {
        RequestType.mobile_order: 1,
        RequestType.web_order: 1,
        RequestType.message_delivery: 2,
        RequestType.view_info_mobile: 2,
        RequestType.view_info_web: 2,
        RequestType.delivery_request: 1,
        RequestType.followup_order: 2
    }

    for request_type, l in zip(request_orders, request_likelihoods):
        requests[request_type] = Request(request_type, l, services[request_type], priorities[request_type])

    return requests


def init_services(service_numbers):
    services = {}

    mean_service_times = [8, 5, 6, 9, 12, 2, 3]
    error_rates = [0.02, 0.02, 0.03, 0, 1, 0, 2, 0.01, 0.01]

    max_times = [int(i) for i in input().split()]

    for i, (service_type, service_num) in enumerate(zip(service_orders, service_numbers)):
        services[service_type.value] = Service(service_type, service_num, mean_service_times[i], max_times[i],
                                               error_rates[i])

    return services


def set_env(env):
    pass


def handle_customer(env, customer_num, system):
    request_type = request_orders[get_random_number(request_likelihoods)]
    request = get_request(request_type, all_requests)
    service_chain = request.services

    arrival_time = env.now

    for service in service_chain:
        with system.__getattribute__(service.value).request() as request:
            yield request
            # here we should run a function with env for timeout for a specific time
            yield env.process(theater.purchase_ticket(moviegoer))


def run_simulation(env, request_rate, system):
    customers = 0

    while True:
        customers += 1
        # handle_customer(env, customers)
        env.process(handle_customer(env, customers, system))

        yield env.timeout(request_rate)


def start_simulation():
    service_numbers = [int(i) for i in input().split()]

    request_rate = int(input())
    total_time = int(input())

    all_services = init_services(service_numbers)
    all_requests = init_requests()

    env = simpy.Environment()
    system = System(env, all_services)

    env.process(run_simulation(env, request_rate, system))
    env.run(until=total_time)


if __name__ == "__main__":
    start_simulation()