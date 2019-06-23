from bisect import bisect_left
import argparse, random

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
    if list[index][:len(word)] != word:
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
  parser = argparse.ArgumentParser(description = 'For a given string and word list, finds pairs of words from the list that the given string could be a contraction of.')
  parser.add_argument('string')
  parser.add_argument('-l', '--list', default='sowpods.txt', help='Word list')
  parser.add_argument('-b', '--bounds', nargs=2, default=[1, 32], type=int, help='Minimum and maximum prefix length', metavar=('MIN','MAX'))
  parser.add_argument('-w', '--write', action='store_true', help='Write all solutions to an output file')
  parser.add_argument('-n', '--num', type=int, default=1, help='Number of solutions to be printed to the console; invalidated by -w')
  args = parser.parse_args()
  
  l, l_reverse = prepare_lists(args.list)
  
  result = search(args.string, l, l_reverse, args.bounds[0], args.bounds[1])
  
  if args.write:
    with open("out_%s.txt" % args.string, "w") as f:
      for pair in result:
        f.write(pair[0] + " " + pair[1] + "\n")
    print("Wrote %d pairs to out_%s.txt" % (len(result), args.string) )
  else:
    for _ in range(args.num):
      i = random.randrange(len(result))
      pair = result[i]
      print(pair[0], pair[1])
      del(result[i])