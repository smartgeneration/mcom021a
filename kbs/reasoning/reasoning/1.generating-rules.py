import pandas as pd
import utilities.network as nw

infile = 'original-rules.csv'
outfile = 'rules.csv'

print("Processing the input file...")
fp = open(infile, 'r')
lst = []
for line in fp:
    # remove comment lines
    if line[0] != '#':
        original_rule = line.rstrip('\n')
        lst.append(f"#{original_rule}")
        lst.extend(nw.split_rule(original_rule))
# storing data
print("Storing data to the output file...")
with open(outfile, 'w') as fp:
    for item in lst:
        # write each item on a new line
        fp.write(f"{item}\n")
    print('Done')