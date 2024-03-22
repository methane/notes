import os, time, sys

f = open("foo.txt", "w")

class C:
    def __init__(self):
        self.f = f
        #os.register_at_fork(after_in_child=self.atfork)
        sys.addaudithook(self.audit)

    def atfork(self):
        print("atfork")

    def audit(self, event, args):
        print(event)

c=C()
del c, f, C
