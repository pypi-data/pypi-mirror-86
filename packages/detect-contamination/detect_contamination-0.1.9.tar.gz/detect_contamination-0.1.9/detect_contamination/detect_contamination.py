import os
import sys
import argparse
import subprocess
import tempfile
from detect_contamination.fragmentation import fragmentation

def detect_contamination(args: argparse.Namespace):

    path_command = subprocess.run('which centrifuge', check=True, shell=True, capture_output=True)
    centrifuge_path = path_command.stdout.decode("utf-8").partition('\n')[0]

    reads, num_fragments, sequence_length, primary_file = fragmentation(args.contaminated, args.fragment_length, args.overlap_length, args.index, centrifuge_path)

    to_write = tempfile.NamedTemporaryFile(
                    suffix=".fa", 
                    mode="r", 
                    delete=False,
                )

    summary = tempfile.NamedTemporaryFile(
                    suffix=".fa", 
                    mode="r", 
                    delete=False,
                )

    exit_now = False

    centrifuge_command = centrifuge_path + " -p " + str(args.threads) + "  -f -x " + args.index + " " + primary_file + " -k 1 " + " --report-file " + summary.name + " >> " + to_write.name
    new_command = subprocess.run(centrifuge_command, shell=True, capture_output=True)
    if (new_command.returncode != 0):
        exit_now = True
        print(new_command.stderr)

    if (exit_now):
        print("fail")
        os.remove(to_write.name)
        os.remove(summary.name)
        return None


    results = {}
    
    with open(to_write.name, 'r') as f:
        f.readline()
        for line in f:
            fields = line.split()
            if (fields[0] == "readID"):
                continue
                
            if fields[2] in results.keys():
                results[fields[2]] += int(fields[5])
            else:
                results[fields[2]] = int(fields[5])   

    for item in results:
        results[item] = results[item]/sequence_length

    key_to_remove = ""

    for key in results.keys():
        if (results[key] == 0):
            key_to_remove = key
            results.pop(key_to_remove)
            break

    os.remove(primary_file)
    
    return results


