from enum import Enum
import simpy

request_likelihoods = [0.2, 0.1, 0.05, 0.25, 0.15, 0.2, 0.05]


class ServiceType(Enum):
    restaurant_management = "RESTAURANT_MANAGEMENT"
    customer_management = "CUSTOMER_MANAGEMENT"
    orders_management = "ORDERS_MANAGEMENT"
    delivery_communication = "DELIVERY_COMMUNICATION"
    payment = "PAYMENT"
    api_gate = "API_GATE"
    web_gate = "WEB_GATE"


class RequestType(Enum):
    mobile_order = "MOBILE_ORDER"
    web_order = "WEB_ORDER"
    message_delivery = "MESSAGE_DELIVERY"
    view_info_mobile = "VIEW_INFO_MOBILE"
    view_info_web = "VIEW_INFO_WEB"
    delivery_request = "DELIVERY_REQUEST"
    followup_order = "FOLLOWUP_ORDER"


class Service:
    def __init__(self, service_type: ServiceType, number, mean_service_time, max_time, error_rate):
        self.type = service_type
        self.number = number
        self.mean_time = mean_service_time
        self.max_time = max_time
        self.error_rate = error_rate


class Request:
    def __init__(self, request_type, occurrence_likelihood, services, priority):
        self.type = request_type
        self.occurrence_likelihood = occurrence_likelihood
        self.services = services
        self.priority = priority


# how to get attribute of system
# system.__getattribute__(ServiceType.restaurant_management.value)

class System:
    def __init__(self, env, services):
        self.env = env
        for s in services:
            setattr(self, services[s].type.value, simpy.Resource(env, services[s].number))
