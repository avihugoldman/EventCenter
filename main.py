from event_master import EventMaster
# from test import Test
# import argparse
# parser = argparse.ArgumentParser(prog="Detector App", description="Starting Captain's Eye Detector Main Algorithm App! ")
# parser.add_argument('-t', '--type', required=True, default="config.json", help='config file')
# check if can commit
if __name__ == '__main__':

    #args = parser.parse_args()

    em = EventMaster()

    camList = em.load_configuration("config.txt", "data_config.json")

    #camList = em.load_configuration_from_json("data_config.json")

    for camera in camList:
        camera.convert_event_int_to_str()

    em.run_as_server(camList)

    # if args.type == "Q":
    #     exit(0)
    #
    # elif args.type == "T":
    #     test = Test("T")
    #     test.start_test("SMOKE")
    #
    # elif args.type == "A":
    #     em.run_as_server(camList)
    #
    # elif args.type == "P":
    #     sock = em.open_socket()
    #     em.run_as_client(camList, sock, "p")
    #
    # elif args.type == "S":
    #     sock = em.open_socket()
    #     em.run_as_client(camList, sock, "s")

