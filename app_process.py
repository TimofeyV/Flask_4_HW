from random import randint, seed
import multiprocessing
import time

seed(0)
my_list = [randint(1, 100) for i in range(1000000)]
summ_list = 0
start_time = time.time()

counter = multiprocessing.Value('i', 0)


def increment(current_list, cnt):
    for i in range(len(current_list)):
        with cnt.get_lock():
            cnt.value += current_list[i]
    print(f"Значение счетчика: {cnt.value:_}")


if __name__ == '__main__':
    processes = []
    parts = 5
    for i in range(parts):
        p = multiprocessing.Process(target=increment, args=(my_list[(len(my_list) // parts) * i:len(my_list) // parts * (i + 1)], counter,))
        processes.append(p)
        p.start()
    p = multiprocessing.Process(target=increment, args=(my_list[(len(my_list) // parts) * parts:], counter,))
    processes.append(p)
    p.start()

    for p in processes:
        p.join()

    print(f"Значение счетчика в финале: {counter.value:_}")
    print(f"Result in {time.time() - start_time:.2f} seconds")