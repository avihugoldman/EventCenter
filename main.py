from event_master import EventMaster
from runType import runType
from test import Test

if __name__ == '__main__':
    em = EventMaster()

    camList = em.load_configuration("config.txt", "data_config.json")

    for camera in camList:
        camera.convertEventIntToSTR()

    rt = runType()

    if rt == -1:
        exit(0)

    elif rt == 10:
        test = Test("PERSONS")
        test.start_test()

    elif rt == 11 or rt == 12:
        test = Test("SMOKE")
        test.start_test()

    else:
        sock = em.open_socket()
        em.run(camList, sock)

