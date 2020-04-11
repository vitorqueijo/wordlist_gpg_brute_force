import os
import sys
import time

from multiprocessing import Semaphore
import multiprocessing as mp
import gnupg


def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (mp.current_process().name, func.__name__, args, result)

def chunkfy_list(wordlist):
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			size_wd = len(wd)
			chunks = [wd[x:x+10000] for line in range(0, size_wd, 10000)]

	except OverflowError as error:
		print("OverFlow: ", error)
	except Exception as exception:
		print("Exception in divided: ", exception)
	return chunks

def brute_force_simple(wordlist):
	target = 'lab1.gpg' # edit to your GPG file
	gpg = gnupg.GPG()
	time_count = time.time()
	for pwd in wordlist:
		try:
			decrypted_file = gpg.decrypt_file(target, passphrase=pwd)
			if decrypted_file.ok:
				print('status: ', decrypted_file.status)
				print('stderr: ', decrypted_file.stderr)
				sema.release()
				print("PASSWORD: ", pwd)
		except Exception as e:
			print("Exception: ", e)
	sema.release()
	print("not yet {}".format(time.time() - time_count))

if __name__ == "__main__":
	# Setting up numbers of cores to use
	#print("There're {} cores available on machine".format(mp.cpu_count()))
	#cpu_cores = int(input("How many cores do you want to use?\n"))
	#if cpu_cores > mp.cpu_count() and cpu_cores <= 0:
	#	print("setting up to maximum")
	#	cpu_cores = mp.cpu_count()
	NUM_PROCESSES = cpu_cores * 2
	#TODO: argparse for any wordlist and gpg file
	# Not a good way if you don't want to freeze your computer
	# wordlists = [wd for wd in os.listdir('.') if os.path.isfile(wd) if wd.endswith("_*.txt")]
	start = time.time()
	wordlists = chunkfy_list('rockyou.txt') # edit to your wordlist
	print("wordlist chunkfied, elapsed time: ", time.time() - start)
	print("Setting up concurrency at 1% of all tasks")
	concurrency = len(TASKS) * 0.01
	num_tasks = len(TASKS)
	sema = Semaphore(concurrency)

	# Starting workers
	print("Setting up tasks, elapsed time: ", time.time() - start)
	TASKS = [(brute_force_simple, wd) for wd in wordlists]

	# Submitting
	for task in TASKS:
		q.put(task)

	# Start
	for process in range(NUM_PROCESSES):
		mp.Process(target=worker, args=(q, done)).start()
	# Results
	print('Results: \n')
	for i in range(len(TASKS)):
	        print('\n', done.get())
	# Then, stop done
	for i in range(NUM_PROCESSES):
        	q.put('STOP')

	print("Elapsed time: ", time.time() - start)
	end = time.time() - start
	print("End of process, time elapsed: {}".format(end))
