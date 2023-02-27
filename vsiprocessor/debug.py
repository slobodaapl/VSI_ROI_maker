
class Test:

    def __init__(self, num):
        self.num = num

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.num == 0:
            raise StopIteration
        self.num -= 1
        return self.num


blah = Blah(5)
for i in blah:
    print(i)

with Blah(5) as blah:
    for i in blah:
        print(i)