#!/usr/bin/python

import sqlite3, os
import argparse, sys

# Read user input
def process_arguments(args):
    parser = argparse.ArgumentParser(description="Tool to parse and extract .db3 quarantined files by AntiVirus(OPSWAT)")
    parser.add_argument('-f',
                        '--file',
                        required=True,
                        help="DB3 file to read"
                        )
    options = parser.parse_args(args)
    return vars(options)

if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])
if userOptions["file"] != None:
    db_file = userOptions["file"]

# Prepare where to save the files
print "(+) Reading %s" %db_file
cwd = os.getcwd()
cwd_extract = cwd+'/extracted/'
if os.path.exists(cwd_extract):
    print "(+) Directory 'extracted' already exists"
else:
    try:
        os.makedirs(cwd_extract)
        print "(+) Directory created %s" %cwd_extract
    except Exception as err:
        print "Error: %s" %err

# Open a connection with the database
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Get all the quarantine ID's from the tabel
d1 = c.execute("SELECT `_rowid_`,* FROM `QUARANTINE_INFO`  ORDER BY `_rowid_` ASC LIMIT 0, 50000")

# Go over all the quarantine ID's and extract the data for them
for d1_each in d1:
    try:
        qid = str(d1_each[2])
        fn1 = str(d1_each[-1]).replace(':', '').replace('\\', 'xxxxx').replace('.', 'yyyyy')+'xxxxx'+str(d1_each[-2])+'xxxxx'+str(d1_each[3])
        f3 = ''.join(e for e in fn1 if e.isalnum())
        filename = f3.replace('xxxxx', '_').replace('yyyyy', '.')
        file_path = cwd_extract+filename
        c1 = 'sqlite3 '+db_file+ ' "SELECT quote(blob_data) FROM QUARANTINE_BLOB WHERE quarantine_id = '+qid+'"'
        c2 = " | cut -d\\' -f2 | xxd -r -p > "+file_path
        # Name the file [original filename + timestamp + threat name]
        extract_com = c1+c2
        print "(+) Extracting %s" %file_path
        os.system(extract_com)
    except Exception as err:
        print "Error: %s" %err
