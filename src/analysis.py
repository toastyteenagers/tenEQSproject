import sys
import utils

if len(sys.argv) < 2:  # argv[0] is the script name
    print("Usage: python analysis.py [filename for csv]")
    sys.exit(1)

file_path = sys.argv[1]
print("Reading csv file at:", file_path)

df = utils.read_csv(file_path)


print(df.head())
print(df.describe())


sys.exit(0)
