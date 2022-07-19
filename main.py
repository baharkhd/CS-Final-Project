import simpy
from Entities import ServiceType, Service, RequestType, Request


def init_requests():
    requests = {}
    likelihoods = [0.2, 0.1, 0.05, 0.25, 0.15, 0.2, 0.05]

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

    request_orders = [
        RequestType.mobile_order,
        RequestType.web_order,
        RequestType.message_delivery,
        RequestType.view_info_mobile,
        RequestType.view_info_web,
        RequestType.delivery_request,
        RequestType.followup_order
    ]

    for request_type, l in zip(request_orders, likelihoods):
        requests[request_type] = Request(request_type, l, services[request_type])

    return requests


def init_services(service_numbers):
    services = {}

    mean_service_times = [8, 5, 6, 9, 12, 2, 3]
    error_rates = [0.02, 0.02, 0.03, 0, 1, 0, 2, 0.01, 0.01]

    service_orders = [
        ServiceType.restaurant_management,
        ServiceType.customer_management,
        ServiceType.orders_management,
        ServiceType.delivery_communication,
        ServiceType.payment,
        ServiceType.api_gate,
        ServiceType.web_gate,
    ]

    max_times = [int(i) for i in input().split()]

    for i, (service_type, service_num) in zip(service_orders, service_numbers):
        services[service_type.value] = Service(service_type, service_num, mean_service_times[i], max_times[i],
                                               error_rates[i])

    return services


def get_inputs():
    service_numbers = [int(i) for i in input().split()]

    request_rate = int(input())
    time = int(input())

    services = init_services(service_numbers)
    requests = init_requests()


def simulation():
    get_inputs()
    env = simpy.Environment()

    env.run(until=10)


if __name__ == "__main__":
    simulation()
