from event_master import EventMaster
from test import Test
import argparse
#parser = argparse.ArgumentParser(prog="Detector App", description="Starting Captain's Eye Detector Main Algorithm App! ")
#parser.add_argument('-t', '--type', required=True, default="config.json", help='config file')
# check if can commit


class Args:
    def __init__(self, type):
        self.type = type

if __name__ == '__main__':

    #args = parser.parse_args()

    args = Args(input("press 'p' for person, 's' for smoke, 'a' for anomaly, 't' for test or 'q' to exit"))
    em = EventMaster()

    camList = em.load_configuration("config.txt", "data_config.json")

    #camList = em.load_configuration_from_json("data_config.json")

    for camera in camList:
        camera.convert_event_int_to_str()

    if args.type == "q":
        exit(0)

    elif args.type == "t":
        test = Test("T")
        test.start_test("SMOKE")

    elif args.type == "a":
        em.run_as_server(camList)

    elif args.type == "p":
        sock = em.open_socket()
        em.run_as_client(camList, sock, "p")

    elif args.type == "s":
        sock = em.open_socket()
        em.run_as_client(camList, sock, "s")

