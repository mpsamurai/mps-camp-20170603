# # リストの中から求めたい(num)を見つける

class BisectionMethod():

    def __init__(self):
        self.low = 0
        self.mid = 0

    def bisection_method_list(self, num, list):
        get_list = list
        # low = 0
        # mid = 0
        result = num
        high = get_list[-1]

        while True:
            self.mid = (high - self.low) / 2 + self.low
            print("mid", self.mid)
            if self.mid == result:
                print("みつかったよ", self.mid, result)
                break
            else:
                if self.mid < result:
                    self.low = self.mid
                else:
                    high = self.mid

if __name__ == '__main__':

    bisection = BisectionMethod()
    bisection.bisection_method_list(6, range(1,11))

