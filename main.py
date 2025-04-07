from multiprocessing import Pool

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
threads = len(alphabet)
salt = "9mjD5ht1" # given salt
expected = "ro2ITHJjiBpTyfjYRYn2R" # expected hash

def init(data):
    global shared_data
    shared_data = data

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

def partition(combos):
    if(len(combos) % threads != 0):
        exit("Error: Number of combinations is not divisible by number of threads.")

    factor = len(combos) / threads
    lower = 0
    upper = factor
    partitions = []

    for i in range(threads):
        partitions.append(combos[int(lower):int(upper)])
        lower = upper
        upper += factor

    return partitions

def hash_check(partition):
    from passlib.hash import md5_crypt
    global shared_data
    count = 0
    for firstHalf in shared_data:
        for secondHalf in partition:
            combo = firstHalf + secondHalf
            count += 1

            result = md5_crypt.hash(combo, salt=salt)
            result_hash = result.split("$")[3]

            is_correct_password = result_hash == expected
            if is_correct_password:
                return combo
    print(count) 
    return None

def parallelize(combos, partitions):
    results = []
    with Pool(threads, initializer=init, initargs=(combos,)) as pool:
        results = pool.map(hash_check, partitions)
    return results

emptyCombo = ['']
oneCombos = alphabet.copy()
twoCombos = combos(oneCombos, alphabet)
threeCombos = combos(twoCombos, alphabet)

onePartitions = partition(oneCombos)
twoPartitions = partition(twoCombos)
threePartitions = partition(threeCombos)

if __name__ == "__main__":
    print("Testing 1 character passwords")
    oneResults = parallelize(emptyCombo, onePartitions)
    check(oneResults)

    print("Testing 2 character passwords")
    twoResults = parallelize(emptyCombo, twoPartitions)
    check(twoResults)

    print("Testing 3 character passwords")
    threeResults = parallelize(emptyCombo, threePartitions)
    check(threeResults)

    print("Testing 4 character passwords")
    fourResults = parallelize(oneCombos, threePartitions)
    check(fourResults)
    
    print("Testing 5 character passwords")
    fiveResults = parallelize(twoCombos, threePartitions)
    check(fiveResults)

    print("Testing 6 character passwords")
    sixResults = parallelize(threeCombos, threePartitions)
    check(sixResults)

    print("Password not found")
    exit(1)