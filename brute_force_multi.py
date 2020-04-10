import multiprocessing as mp
import gnupg


def divide_list(wordlist, num_to_split):
	if num_to_split > 4:
		print("Changing to 4 as a default")
	num_to_split = 4
	splitted_wordlist = None
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			for n_line, line in enumerate(wd):
				if n_line % num_to_split == 0:
					if splitted_wordlist:
						splitted_wordlist.close()
					n_splitted = "rockyou_{}.txt".format(n_line+num_to_split)
					splitted_wordlist = open(n_splitted, "w")
				splitted_wordlist.write(str(line))
			if splitted_wordlist:
				splitted_wordlist.close()
	except OverflowError as error:
		print(error)
	except Exception as exception:
		print(exception)

def decrypt_gpg(gpg_file):
	gpg = gnupg.GPG()
	with open(gpg_file, 'rb') as f:
		decrypted_file = gpg.decrypt_file(f, passphrase=password_attempt)
	if decrypted_file.ok:
		print('status: ', decrypted_file.status)
		print('stderr: ', decrypted_file.stderr)

