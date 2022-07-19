from enum import Enum


class ServiceType(Enum):
    restaurant_management = "RESTAURANT_MANAGEMENT"
    customer_management = "CUSTOMER_MANAGEMENT"
    orders_management = "ORDERS_MANAGEMENT"
    delivery_communication = "DELIVERY_COMMUNICATION"
    payment = "PAYMENT"
    api_gate = "API_GATE"
    web_gate = "WEB_GATE"


class Service:
    def __init__(self, service_type: ServiceType, number, mean_service_time, max_time):
        self.service_type = service_type
        self.number = number
        self.mean_time = mean_service_time
        self.max_time = max_time
