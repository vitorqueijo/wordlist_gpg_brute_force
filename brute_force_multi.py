import os
import sys
import time

from multiprocessing import Semaphore
import psutil
import multiprocessing as mp

import gnupg


#def worker(input, output):
#	for func, args in iter(input.get, 'STOP'):
#		result = calculate(func, args)
#		print(result)
#	sema.release()
#
#def calculate(func, args):
#    result = func(*args)
#    return '%s says that %s%s = %s' % \
#       (mp.current_process().name, func.__name__, args, result)

def limit_cpu_usage():
	pid = psutil.Process(os.getpid())
	pid.nice(19)

def chunkfy_list(wordlist):
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			size_wd = len(wd)
			chunks = [wd[line:line+10000] for line in range(0, size_wd, 10000)]

	except OverflowError as error:
		print("OverFlow: ", error)
	except Exception as exception:
		print("Exception in divided: ", exception)
	return chunks

def brute_force_simple(name, wordlist, sema):
	time.sleep(0.01)
	sema.acquire()
	print("Process {} running".format(name))

	gpg = gnupg.GPG()
	target = gpg.decrypt_file('lab1.gpg', passphrase=pwd)
	time_count = time.time()
	for pwd in wordlist:
		try:
			if decrypted_file.ok:
				print('status: ', decrypted_file.status)
				print('stderr: ', decrypted_file.stderr)
				print("PASSWORD: ", pwd)
				target.close()
				sema.release()
		except Exception as e:
			print("Exception: ", e)
	print("not yet {}".format(time.time() - time_count))
	target.close()
	sema.release()

if __name__ == "__main__":
	print("Attack Initiated!")	
	start = time.time()
	resourses = chunkfy_list('rockyou.txt') # edit to your wordlist
	print("wordlist chunkfied, elapsed time: ", time.time() - start)
	print("Setting up concurrency at 1% of all tasks")
	print("Setting up tasks")
	concurrency = int(len(resourses) * 0.01)
	num_tasks = len(resourses)
	sema = Semaphore(concurrency)

	# Start
	processes = list()
	for i, r in enumerate(resourses):
		process = mp.Process(target=brute_force_simple, args=(i, r, sema))
		processes.append(process)
		process.start()

	# Finish
	for p in processes:
		p.join()

	print("Elapsed time: ", time.time() - start)
	end = time.time() - start
	print("End of process, time elapsed: {}".format(end))
