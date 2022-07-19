import simpy
from Entities import ServiceType, Service


def get_inputs():
    service_orders = [
        ServiceType.restaurant_management,
        ServiceType.customer_management,
        ServiceType.orders_management,
        ServiceType.delivery_communication,
        ServiceType.payment,
        ServiceType.api_gate,
        ServiceType.web_gate,
    ]

    mean_service_times = [8, 5, 6, 9, 12, 2, 3]

    services = {}

    service_numbers = [int(i) for i in input().split()]

    requests_rate = int(input())
    time = int(input())
    max_times = [int(i) for i in input().split()]

    for i, (service_type, service_num) in zip(service_orders, service_numbers):
        services[service_type.value] = Service(service_type, service_num, mean_service_times[i], max_times[i])


def simulation():
    get_inputs()
    env = simpy.Environment()

    env.run(until=10)


if __name__ == "__main__":
    simulation()
