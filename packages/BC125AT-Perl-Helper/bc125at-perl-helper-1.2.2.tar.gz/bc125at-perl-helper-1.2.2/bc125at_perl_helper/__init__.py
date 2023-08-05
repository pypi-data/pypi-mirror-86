#!/usr/bin/python3

# Imports
import sys
import io
import json
import re
import csv
import subprocess
import string
import random

# Constants
NAME = "BC125AT-Perl Helper"
CMD = "bc125at-perl-helper"
VERSION = "1.2.2"
AUTHOR = "Max Loiacono"

OPERATION_TO_CSV = 0
OPERATION_TO_TXT = 1


def main():
	# Basics
	print(NAME + "\nVersion " + VERSION + " by " + AUTHOR + "\n")

	# CliArgs handler
	if len(sys.argv) < 2:
		showHelp()
	elif sys.argv[1] == "c" and len(sys.argv) == 4:
		convert(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "r" and len(sys.argv) == 3:
		scannerRead(sys.argv[2])
	elif sys.argv[1] == "w" and len(sys.argv) == 3:
		scannerWrite(sys.argv[2])
	elif sys.argv[1] == "clean" and len(sys.argv) == 3:
		cleanCSV(sys.argv[2])
	else:
		showHelp()

	exit(0)


def showHelp():
	print("Usage:\n\t" + CMD + " <command> <1?> <2?>\n")
	print("Please specify a command:")
	print("\tr <out file>\t\tRead channels from the scanner and output a CSV file.")
	print("\tw <CSV file>\t\tWrite a CSV file directly to the scanner.")
	print("\tc <in file> <out file>\tConvert a bc125at-perl file to CSV or vice-versa.")
	print("\tclean <CSV file>\tReset any channels without a frequency set.")
	exit(1)


def writeOut(outFileName, outData):
	try:
		outFile = open(outFileName, "w")
		outFile.write(outData)
		outFile.close()
		print("Success! Wrote file to: " + outFileName)
	except:
		print("ERROR: Could not write file: " + outFileName)
		exit(1)


def bc125at2JSON(inData):
	# Convert text to JSON
	inData = re.sub("(\s(?=[a-z_]* => '))|(\s(?==> '))", "\"", inData)
	inData = inData.replace("=> '", ": '")
	inData = inData.replace("'", "\"")
	inData = inData.replace("\"pri\": \"0\",", "\"pri\": \"0\"")
	inData = inData.replace("\"pri\": \"1\",", "\"pri\": \"1\"")
	inData = re.sub("},\s*]", "}]", inData)

	try:
		inData = json.loads(inData)
		return inData
	except:
		print("ERROR: Could not parse file. Did you modify it?")
		exit(1)


def list2bc125at(inData):
	# Setup output file
	outData = "[\n"

	# Generate output data
	ind = 1
	for c in inData:
		outData += "{\n"
		outData += "cmd => 'CIN',\n"
		outData += "index => '" + str(ind) + "',\n"
		if len(c[0]) > 16:
			print("ERROR: \"" + c[0] + "\" is longer than 16 characters!")
			exit(1)
		outData += "name => '" + c[0] + "',\n"
		outData += "frq => '" + c[1] + "',\n"
		if c[2] not in ["FM", "NFM", "AM", "AUTO"]:
			print("ERROR: Unknown modulation: \"" + c[2] + "\"")
			exit(1)
		outData += "mod => '" + c[2] + "',\n"
		outData += "ctcss_dcs => '" + c[3] + "',\n"
		if int(c[4]) < 0:
			print("ERROR: Delay must be >=0!")
			exit(1)
		outData += "dly => '" + c[4] + "',\n"
		if c[5] != "0" and c[5] != "1":
			print("ERROR: Lockout must be either 0 or 1!")
			exit(1)
		outData += "lout => '" + c[5] + "',\n"
		if c[6] != "0" and c[6] != "1":
			print("ERROR: Priority must be either 0 or 1!")
			exit(1)
		outData += "pri => '" + c[6] + "',\n"
		outData += "},\n"

		ind += 1
	outData += "]\n"

	return outData


def json2csv(inJSON):
	outData = "Name,Frequency,Modulation,CTCSS Tone,Delay,Locked Out,Priority\n"

	try:
		for c in inJSON:
			outData += "\"" + c["name"] + "\"" + "," + "\"" + c["frq"] + "\"" + "," + "\"" + c["mod"] + "\"" + "," + "\"" + c["ctcss_dcs"] + "\"" + "," + "\"" + c["dly"] + "\"" + "," + "\"" + c["lout"] + "\"" + "," + "\"" + c["pri"] + "\"" + "\n"
	except:
		print("ERROR: Could not convert file. Did you modify it?")
		exit(1)

	return outData


def list2csv(inList):
	return json2csv(bc125at2JSON(list2bc125at(inList)))


def csv2list(inData):
	# Convert CSV to TXT
	inData = inData.replace("Name,Frequency,Modulation,CTCSS Tone,Delay,Locked Out,Priority\n", "")
	# Read CSV
	inData = csv.reader(io.StringIO(inData))
	inData = list(inData)

	if len(inData) != 500:
		print("ERROR: Total channels does not equal 500! (" + str(len(inData)) + ")")
		exit(1)
	
	return inData


def readFile(inFileName):
	# Test input files
	inFile = None
	try:
		inFile = open(inFileName)
		inFile.read(4)
		inFile.seek(0)
	except:
		print("ERROR: Could not read file: " + inFileName)
		exit(1)

	inData = inFile.read()
	inFile.close()

	return inData


def convert(inFileName, outFileName):
	# Test input files
	operation = None
	if inFileName.lower().endswith('.csv'):
		operation = OPERATION_TO_TXT
	else:
		operation = OPERATION_TO_CSV

	# Begin conversion
	print("Converting " + inFileName + " to " + ("CSV" if operation == OPERATION_TO_CSV else "Text"))

	inData = readFile(inFileName)
	outData = None

	if operation == OPERATION_TO_CSV:
		inData = bc125at2JSON(inData)
		
		# Write CSV
		outData = json2csv(inData)
	else:
		inData = csv2list(inData)

		outData = list2bc125at(inData)
		
	writeOut(outFileName, outData)


def randString(length):
	return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))


def scannerRead(outFile):
	print("Reading from scanner...")

	f = randString(36)
	subprocess.call(["sudo", "bc125at-perl", "driver"])
	subprocess.call(["sudo", "bc125at-perl", "channel", "read", "--file=/tmp/" + f + ".txt"])
	convert("/tmp/" + f + ".txt", outFile)


def scannerWrite(inFile):
	print("Writing to scanner...")

	if not inFile.lower().endswith(".csv"):
		print("ERROR: File must end with .csv")
		exit(1)

	f = randString(36)
	convert(inFile, "/tmp/" + f + ".txt")
	subprocess.call(["sudo", "bc125at-perl", "driver"])
	subprocess.call(["sudo", "bc125at-perl", "channel", "write", "--file=/tmp/" + f + ".txt"])


def cleanCSV(inFile):
	print("Cleaning " + inFile)
	if not inFile.lower().endswith(".csv"):
		print("ERROR: File must end with .csv")
		exit(1)

	fc = readFile(inFile)
	fc = csv2list(fc)

	for i in range(0, len(fc)):
		if fc[i][1] in ["0.000", "0"]:
			fc[i] = ["", "0.000", "AUTO", "0", "2", "1", "0"]

	fc = list2csv(fc)
	writeOut(inFile, fc)


main()
