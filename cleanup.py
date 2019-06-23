''' Cleans up the workspace by removing all output files '''
from glob import glob
from os import remove

cnt = 0

for file in glob("out*.txt"):
  remove(file)
  cnt += 1
  
print("Removed %d file(s)." % cnt)