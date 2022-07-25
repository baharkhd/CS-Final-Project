from statistics import mean

from entities import *
from utils import *

all_requests = []
all_services = []
timeouts = []

queues = {}
server_usage = {}
wait_times = {}

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

    max_times = [int(i) for i in input().split()]
    max_times_dict = {}

    for i in range(len(max_times)):
        req = request_orders[i]
        max_times_dict[req] = convert_to_minute(max_times[i])

    for request_type, l in zip(request_orders, request_likelihoods):
        requests[request_type] = Request(request_type, l, services[request_type], max_times_dict[request_type],
                                         priorities[request_type])

    return requests


def init_services(service_numbers):
    services = {}

    mean_service_times = [8, 5, 6, 9, 12, 2, 3]
    error_rates = [0.02, 0.02, 0.03, 0, 1, 0, 2, 0.01, 0.01]

    for i, (service_type, service_num) in enumerate(zip(service_orders, service_numbers)):
        services[service_type.value] = Service(service_type, service_num, mean_service_times[i], error_rates[i])

    return services


def do_service(env, service_time):
    # service_time = get_exp_sample(all_services[service_type.value].mean_time)[0]
    # print(service_time, convert_to_minute(service_time))
    yield env.timeout(service_time)


def handle_customer(env, customer_num, system):
    request_type = request_orders[get_random_number(request_likelihoods)]
    request = get_request(request_type, all_requests)
    service_chain = request.services

    arrival_time = env.now

    service_time_total = 0
    for service_type in service_chain:
        with system.__getattribute__(service_type.value).request(priority=request.priority) as req:
            # print('---', service_type.value, '---')
            # for q in system.__getattribute__(service_type.value).queue:
            #     print('+++')
            #     print(q.priority)
            #     print('+++')
            # print('********')
            # print(system.__getattribute__(service_type.value))
            # print(len(system.__getattribute__(service_type.value).queue), ':', service_type.value)

            # print(service_type.value, system.__getattribute__(service_type.value).capacity)

            service_time = convert_to_minute(get_exp_sample(all_services[service_type.value].mean_time)[0])

            yield req

            if service_time_total + arrival_time > request.max_time:
                request.timeout = True
                # print('man hanooz zendam koskesh')
                break

            service_time_total += service_time
            yield env.process(do_service(env, service_time))

            if service_type.value in server_usage.keys():
                server_usage[service_type.value].append(service_time)
            else:
                server_usage[service_type.value] = [service_time]

    finish_time = env.now

    # print(request.type)
    # print(arrival_time)
    # print(service_time_total)
    # print(finish_time)

    if request.type in wait_times.keys():
        wait_times[request.type].append(max(finish_time - arrival_time - service_time_total, 0))
    else:
        wait_times[request_type] = [max(finish_time - arrival_time - service_time_total, 0)]

    timeouts.append(request.timeout)


def run_simulation(env, system):
    customers = 0

    while True:
        customers += request_rate
        for i in range(request_rate):
            env.process(handle_customer(env, customers, system))

        for service in service_orders:
            if service.value in queues.keys():
                queues[service.value].append(len(system.__getattribute__(service.value).queue))
            else:
                queues[service.value] = [len(system.__getattribute__(service.value).queue)]

        yield env.timeout(1 / 60)


def start_simulation():
    env = simpy.Environment()
    system = System(env, all_services)

    env.process(run_simulation(env, system))
    env.run(until=total_time)


if __name__ == "__main__":
    service_numbers = [int(i) for i in input().split()]

    request_rate = int(input())
    total_time = convert_to_minute(int(input()))

    all_services = init_services(service_numbers)
    all_requests = init_requests()

    start_simulation()

    print("**** wait times in queues ****")
    total_waiting = 0
    for wt in wait_times.keys():
        total_waiting += mean(wait_times[wt])
        print(f'{wt}: {mean(wait_times[wt])}')

    print("**** wait times total avg ****")
    print(total_waiting / len(wait_times), 'min')

    print('**** avg queue lengths ****')
    for queue in queues.keys():
        print(f'{queue}: {mean(queues[queue])}')

    print('**** server time usage ****')
    for server in server_usage.keys():
        service = get_service(server, all_services)
        print(f'{server}: {sum(server_usage[server]) / total_time}')

    print("**** timeout avg ****")
    print(mean(timeouts))
