import time
from multiprocessing import Process, Queue, current_process
from queue import Empty  # exception to break from loop when the get(block=False) called on empty queue

numbers = [15492781, 15492787, 15492803,
           15492811, 15492810, 15492833,
           15492859, 15502547, 15520301, 15527509]


def is_prime(number):
    """returns True if number
    is prime, False otherwise"""
    # your code here
    if number > 1:
        for i in range(2, int(number / 2) + 1):
            if (number % i) == 0:
                return False
            else:
                return True

    else:
        return True


def check_prime_worker(job_queue,N):
    """worker function passed as target to Process"""
    while True:
        try:
            num = job_queue.get(block=False)
            print(num,' is prime? ',is_prime(num),N, 'current process:', current_process())
        except Empty:
            break


# your code here
# 1. get next available number from queue
# 2. print the number and whether it
#    is prime or not, use is_prime()
# 3. use try/except to catch Empty exception
#    and quit the loop if no number remains in queue


# calculate if the numbers are prime or not
# measure the performance of parallel processing
if __name__ == "__main__":
    job_queue = Queue()
    t_par = []  # to measure the time
    # number of processes
    for N in range(1, len(numbers) + 1):
        # preparing the jobs to be done by workers
        for n in numbers:
            job_queue.put(n)

        # your code here

        # 1. create list of processes of N process.
        processes = []
        for i in range(1, N):
            p = Process(target=check_prime_worker, args=(job_queue,N))
            processes.append(p)
        # 2. record the start time
        start = time.time()

        # 3. start each of the processes
        [p.start() for p in processes]
        # 4. call join on each of the processes
        [p.join() for p in processes]
        # 5. measure the performance and append to the list of records
        t_par.append(time.time() - start)

        # 6. close the processes
        [p.close() for p in processes]

    print(t_par)




