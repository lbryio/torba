import statistics
import timeit
from unittest import TestCase


def confidence(times, z_factor, plus_err=True):
    mean = statistics.mean(times)
    standard_dev = statistics.stdev(times)
    err = (z_factor * standard_dev) / (len(times) ** 0.5)
    return (mean + err) if plus_err else (mean - err)


def kolakoski():
    def get_sequence(size):
        current_values = [1, 2, 2]
        for i in range(3, size - 2):
            if i % 2 == 1:
                current_values.extend([1] * current_values[i - 1])
            else:
                current_values.extend([2] * current_values[i - 1])
            if len(current_values) >= size:
                break
        return current_values[:size]
    sequence = get_sequence(10000)
    assert sequence.count(1), sequence.count(2) == (502, 498)


class BenchmarkTestCaseMixin(TestCase):
    __kolakoski_ratio = None
    __kolakoski_base = 0.0014849151484668255

    def do_bench(self, what, base_ratio_case=False):
        timer = timeit.Timer(what)
        data = []
        repetitions = 200 if base_ratio_case else None
        data.extend(
            timer.repeat(
                repetitions or timer.autorange(lambda _, time_taken: data.append(time_taken))[0],
                number=1)
        )

        final = min(data)
        if base_ratio_case:
            self.__kolakoski_ratio = self.__kolakoski_base/final
        else:
            return final * self.__kolakoski_ratio

    def assertPerformance(self, what, expected_time: float, error_rate=0.1):  # pylint: disable=C0103
        if self.__kolakoski_ratio is None:
            self.do_bench(kolakoski, base_ratio_case=True)
        delta = error_rate*expected_time
        time_taken = None
        for _ in range(2):
            time_taken = self.do_bench(what)
            if (expected_time - delta) <= time_taken <= (expected_time + delta):
                return
        self.fail(f"Test took {time_taken} instead of {expected_time} with an error rate of {error_rate}")
