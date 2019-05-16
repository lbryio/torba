import statistics
import timeit
from unittest import TestCase


def confidence(times, z, plus_err=True):
    mean = statistics.mean(times)
    standard_dev = statistics.stdev(times)
    err = (z * standard_dev) / (len(times) ** 0.5)
    return (mean + err) if plus_err else (mean - err)


def kolakoski():
    def get_sequence(r):
        a = [1, 2, 2]
        for i in range(3, r - 2):
            if i % 2 == 1:
                a.extend([1] * a[i - 1])
            else:
                a.extend([2] * a[i - 1])
            if len(a) >= r:
                break
        return a[:r]
    sequence = get_sequence(10000)
    assert sequence.count(1), sequence.count(2) == (502, 498)


class BenchmarkTestCaseMixin(TestCase):
    __kolakoski_ratio = None
    __kolakoski_base = 0.0015350378746379041

    def do_bench(self, what, base_ratio_case=False):
        timer = timeit.Timer(what)
        data = timer.repeat(200 if base_ratio_case else timer.autorange()[0], number=1)

        final = confidence(data, 3.291)
        if base_ratio_case:
            self.__kolakoski_ratio = self.__kolakoski_base/final
        else:
            return final * self.__kolakoski_ratio

    def assertPerformance(self, what, expected_time: float, error_rate=0.1):
        if self.__kolakoski_ratio is None:
            self.do_bench(kolakoski, base_ratio_case=True)
        return self.assertAlmostEqual(self.do_bench(what), expected_time, delta=error_rate*expected_time)
