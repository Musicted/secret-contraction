from bisect import bisect_left
import sys

def prepare_lists(path):
  with open(path) as f:
    l = sorted([word.strip().lower() for word in f.readlines()])
    l_reverse = sorted(["".join(reversed(word)) for word in l])
  return (l, l_reverse)
    
def search(word, list, list_reverse, min_len, max_len):
  result = []
  for i in range(min_len, max_len + 1):
    result += search_with_prefix_len(i, word, list, list_reverse)
    
  return result

def search_with_prefix_len(prefix_len, word, list, list_reverse):
  prefix = word[:prefix_len]
  index = bisect_left(list, prefix)
  prefix_words = []
  
  while index < len(list) and list[index][:prefix_len] == prefix:
    prefix_words.append(list[index])
    index += 1
  
  if prefix_words == []:
    return []
  
  suffix_words = find_suffix_words("".join(reversed(word[prefix_len:])), list_reverse)
  
  return [(pre, suf) for pre in prefix_words for suf in suffix_words]
  
def find_suffix_words(suffix_reverse, list_reverse):
  index = bisect_left(list_reverse, suffix_reverse)
  suffix_words = []
  
  while index < len(list_reverse) and list_reverse[index][:len(suffix_reverse)] == suffix_reverse:
    suffix_words.append("".join(reversed(list_reverse[index])))
    index += 1
    
  return suffix_words
  
if __name__ == '__main__':
  print(len(sys.argv))
  if len(sys.argv) != 3 and len(sys.argv) != 5:
    print("Usage:\tpython contraction.py word wordlist [min] [max]")
    print("\tmin and max specify minimum and maximum prefix length, respectively")
    exit(0)
  
  word = sys.argv[1]
  path = sys.argv[2]
  
  min_prefix_len = 3
  max_prefix_len = 6
  
  if len(sys.argv) == 5:
    min_prefix_len = int(sys.argv[3])
    max_prefix_len = int(sys.argv[4])
  
  l, l_reverse = prepare_lists(path)
  
  result = search(word, l, l_reverse, min_prefix_len, max_prefix_len)
  
  with open("out_" + word + ".txt", "w") as f:
    for pair in result:
      f.write(pair[0] + " " + pair[1] + "\n")