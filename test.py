from entities import RequestType

if __name__ == "__main__":
    # # Setup and start the simulation
    # print('Event Latency')
    # env = simpy.Environment()
    #
    # cable = Cable(env, 10)
    # env.process(sender(env, cable))
    # env.process(receiver(env, cable))
    #
    # env.run(until=SIM_DURATION)

    request_orders = [
        RequestType.mobile_order,
        RequestType.web_order,
        RequestType.message_delivery,
        RequestType.view_info_mobile,
        RequestType.view_info_web,
        RequestType.delivery_request,
        RequestType.followup_order
    ]


