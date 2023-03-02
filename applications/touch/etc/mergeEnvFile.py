"""
Merge the example environment file in to the production one if it exists, otherwise make a copy of the example file
"""

import os

def containsEnvVar(vals, var):
	for i, pair in enumerate(vals):
		if type(pair) is list:
			if var == pair[0]:
				return True
	return False

def main():
	vals = []
	example_vals = []
	exists = True

	if os.path.exists("../.env"):
		print("Existing .env file found, merge in the example file but keep values from the existing .env file")
		with open("../.env", 'r') as prod:
			for line in prod.readlines():
				if line.strip() != "":
					name, val = line.split("=", 1)
					vals.append([name.strip(), val.strip()])
				else:
					vals.append(line)
	else:
		print("Creating .env file with example values")
		exists = False

	with open(".env-example", 'r') as example:
		# put in example values
		for line in example.readlines():
			if line.strip() != "":
				name, val = line.split("=")
				name = name.strip()
				if not containsEnvVar(vals, name.strip()):
					if exists:
						print("Existing .env does not have val '{}'. Adding it in".format(name))
					if len(example_vals) == 0:
						example_vals.append("\n")
					example_vals.append(line)
			elif not exists:
				example_vals.append(line)

	# for line in example_vals:
	# 	print(repr(line))

	# write out final file
	with open("../.env", 'w') as out:
		for pair in vals:
			if not type(pair) is list:
				out.write(pair)
			else:
				out.write("{}={}\n".format(pair[0], pair[1]))
		for line in example_vals:
			out.write(line)

		print("Wrote out .env at repo root")



if __name__ == '__main__':
	# set dir to location of script
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	main()