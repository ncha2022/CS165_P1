
from passlib.hash import md5_crypt
from multiprocessing import Pool

first_letters = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
letters = [
    '', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]


correct = "ro2ITHJjiBpTyfjYRYn2R"
salt = "9mjD5ht1"
results = 0
found_bool = 0
found_passwd = ""

def genHash(password):
    result = md5_crypt.hash(password, salt=salt)
    return result.split("$")[3] == correct

# for first in first_letters:
#     for second in first_letters:
#         for third in first_letters:
#             for fourth in first_letters:
#                 for fifth in first_letters:
#                     combos = []
#                     for sixth in first_letters:
#                        combos.append(first + second + third + fourth + fifth + sixth)
#                     with Pool(26) as p:     
#                         results = p.map(genHash,combos)
#                     print(results)
output = False   
if __name__ == "__main__":         
    for first in first_letters:
            combos = []
            for second in first_letters:
                combos.append(first + second)
            with Pool(26) as p:     
                results = p.map(genHash,combos)
            output = output + True in results
                
print(output)        
# passwd = first
# result = md5_crypt.hash(passwd, salt=salt)
# found_bool = found_bool + (result.split("$")[3] == correct)



# xxxxxa
# xxxxxb
# xxxxxc
# ...
# xxxxxz

# xxxxa
# xxxxb
# ...
# xxxxz
