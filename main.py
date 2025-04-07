import multiprocessing
from multiprocessing import Pool
from passlib.hash import md5_crypt
import time
import math

salt = "9mjD5ht1" # given salt
expected = "ro2ITHJjiBpTyfjYRYn2R" # expected hash

def check(results):
    for result in results:
        if result != None:
            print("Found password: ", result)
            exit(0)

    return None

def combos(list1, list2):
    result = []
    for i in list1:
        for j in list2:
            result.append(i + j)
    return result

def partition(combos, threads):
    factor = math.ceil(len(combos) / threads)
    lower = 0
    upper = factor
    partitions = []

    for i in range(threads):
        partitions.append(combos[int(lower):int(upper)])
        lower = upper
        upper += factor

    return partitions

def hash_check(combos, partition):
    for firstHalf in combos:
        for secondHalf in partition:
            combo = firstHalf + secondHalf
            result = md5_crypt.hash(combo, salt=salt)
            result_hash = result.split("$")[3]

            is_correct_password = result_hash == expected
            if is_correct_password:
                return combo
            
    return None

def parallelize(combos, partitions, processes):
    args = [(partition, combos) for partition in partitions]
    with Pool(processes) as pool:
        results = pool.starmap(hash_check, args)
    return results

if __name__ == "__main__":
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    processes = multiprocessing.cpu_count()
    start = time.time()

    emptyCombo = ['']
    oneCombos = alphabet.copy()
    twoCombos = combos(oneCombos, alphabet)
    threeCombos = combos(twoCombos, alphabet)

    onePartitions = partition(oneCombos, processes)
    twoPartitions = partition(twoCombos, processes)
    threePartitions = partition(threeCombos, processes)

    print("Testing 1 character passwords")
    oneResults = parallelize(emptyCombo, onePartitions, processes)
    check(oneResults)

    print("Testing 2 character passwords")
    twoResults = parallelize(emptyCombo, twoPartitions, processes)
    check(twoResults)

    print("Testing 3 character passwords")
    threeResults = parallelize(emptyCombo, threePartitions, processes)
    check(threeResults)

    print("Testing 4 character passwords")
    fourResults = parallelize(oneCombos, threePartitions, processes)
    check(fourResults)

    print(time.time() - start)
    exit(0)

    print("Testing 5 character passwords")
    fiveResults = parallelize(twoCombos, threePartitions, processes)
    check(fiveResults)

    print("Testing 6 character passwords")
    sixResults = parallelize(threeCombos, threePartitions, processes)
    check(sixResults)

    print("Password not found")
    exit(1)