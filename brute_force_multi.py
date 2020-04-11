import os
import sys
import time

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

def divide_list(wordlist, num_to_split):
	if num_to_split > mp.cpu_count():
		print("Changing to {} as a default".format(mp.cpu_count()))
		num_to_split = mp.cpu_count()
	splitted_wordlists = list()
	n_wordlist = list()
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			for n_line, line in enumerate(wd):
				n_wordlist.append(line)
				if n_line % num_to_split == 0:
					splitted_wordlists.append([splitted_wordlists])
					n_wordlist = list()

	except OverflowError as error:
		print("OverFlow: ", error)
	except Exception as exception:
		print("Exception in divided: ", exception)
	return splitted_wordlists

def brute_force_simple(wordlist):
	target = '' # edit to your GPG file
	gpg = gnupg.GPG()
	time_count = time.time()
	for pwd in wordlist:
		try:
			decrypted_file = gpg.decrypt_file(target, passphrase=pwd)
			if decrypted_file.ok:
				print('status: ', decrypted_file.status)
				print('stderr: ', decrypted_file.stderr)
				return pwd
		except Exception as e:
			print("Exception: ", e)
	return "not yet {}".format(time.time() - time_count)

if __name__ == "__main__":
	# Setting up numbers of cores to use
	print("There're {} cores available on machine".format(mp.cpu_count()))
	cpu_cores = int(input("How many cores do you want to use?\n"))
	if cpu_cores > mp.cpu_count() and cpu_cores <= 0:
		print("setting up to maximum")
		cpu_cores = mp.cpu_count()
	NUM_PROCESSES = cpu_cores * 2
	#TODO: argparse for any wordlist and gpg file
	# Not a good way if you don't want to freeze your computer
	# wordlists = [wd for wd in os.listdir('.') if os.path.isfile(wd) if wd.endswith("_*.txt")]
	wordlists = divide_list('rockyou.txt', NUM_PROCESSES) # edit to your wordlist
	gpg_file = open(target, 'rb')
	start = time.time()

	# Starting workers
	print("Starting workers", time.time() - start)
	TASKS = [(brute_force_simple, w) for wd in wordlists]

	# Setting queues
	q = mp.Queue()
	done = mp.Queue()

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
