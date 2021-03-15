

class runType:

    def __init__(self):
        self.eventType = self.read_from_user()

    def read_from_user(self):
        while True:
            ccc = input("Please choose event type: (p: PERSONS s: SMOKE AND LEAKAGE t:test training q: quit) ? ")
            if (ccc == 'p'):
                self.eventType = 1
                break
            if (ccc == 's'):
                self.eventType = 2
                break
            if (ccc == "t"):
                c = input("What do you want to test: (p: PERSONS s: SMOKE l: LEAKAGE : ")
                if c == 'p':
                    self.eventType = 10
                    break
                elif c == 's':
                    self.eventType = 11
                    break
                elif c == 'l':
                    self.eventType = 12
                    break
                else:
                    self.eventType = 10
                    break
            if (ccc == 'q'):
                print("closing program")
                self.eventType = -1
                break
