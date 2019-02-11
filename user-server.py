import math
import primes
import random
import sys
import numpy as np

def invmod(a, p, maxiter=1000000):
    """The multiplicitive inverse of a in the integers modulo p:
         a * b == 1 mod p
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d


class PrivateKey(object):

    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invmod(self.l, n)

    def __repr__(self):
        return '<PrivateKey: %s %s>' % (self.l, self.m)

class PublicKey(object):

    @classmethod
    def from_n(cls, n):
        return cls(n)

    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1

    def __repr__(self):
        return '<PublicKey: %s>' % self.n

def generate_keypair(bits):
    p = primes.generate_prime(bits / 2)
    q = primes.generate_prime(bits / 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

def generate_random_integer():
    r = random.randint(1, sys.maxsize)
    return r
def generate_random_R():
    r = random.randint(1, 10)
    return r

def decrypt(priv, pub, cipher):
        x = pow(cipher, priv.l, pub.n_sq) - 1
        plain = ((x // pub.n) * priv.m) % pub.n
        return plain

def generate_random_user():
    time_slots=random.randint(2,5)
    users=random.randint(2,5)
    user_list=[]
    for i in range(users):
        user_avaliability=[]
        for j in range(time_slots):
            user_avaliability.append(random.randint(0,1))
        user_list.append(user_avaliability)
    return user_list

def test_user(user_list):
    list=[1]*len(user_list[0])
    count=0
    for i in range(len(user_list)):
        for j in range(len(user_list[0])):
            list[j]*=user_list[i][j]
    for i in range(len(list)):
        if list[i]==1:
            print("The "+str(i+1)+"th slot should be available for all users")
        else:
            count+=1
    if count==len(list):
            print("There shouldnt be a time slot that is available for all users")
    return list






def encrypt(pub, plain):
    while True:
        r = primes.generate_prime((round(math.log(pub.n, 2))))
        if r > 0 and r < pub.n:
            break
    x = pow(r, pub.n, pub.n_sq)
    cipher = (pow(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    return cipher

class Server:
    def __init__(self, key_length):
        keypair =generate_keypair(key_length)
        self.privkey, self.pubkey = keypair
    def multiplication_encrypted_vectors(self,list):
        encryped_schedule=[]

        i=0
        size=len(list[0])
        while i<size:
            user_encrypted_schedule = 1
            for encypted_user in list:
                user_encrypted_schedule*=encypted_user[i]
            user_encrypted_schedule=pow(user_encrypted_schedule,generate_random_R()) % self.pubkey.n_sq
            encryped_schedule.append(user_encrypted_schedule)
            i=i+1
        return encryped_schedule


class User:
    def __init__(self,b_list):
        self.id=id
        self.b_list=b_list
        self.time_slots=len(b_list[0])


    def encrypt_vector(self,pub, b_):
        return [encrypt(pub, i) for i in b_]

    def generate_bvector(self):
        list=[]
        for j in range(len(self.b_list)):
            b_ = [0 for i in range(self.time_slots)]
            for i in range(self.time_slots):
                if self.b_list[j][i] == 1:
                    b_[i] = 0
                else:
                    b_[i] = generate_random_integer()
                i = i + 1
            list.append(b_)
        return list

    def decrypt_vector(self,x,priv,pub):
        return np.array([decrypt(priv,pub, i) for i in x])




server=Server(24) #24 bits keypairs
users=generate_random_user()
user=User(users)
print(users)
print(test_user(users))


encrypted_list=[]
print("step 1. Generating b vector for each user")
list=user.generate_bvector()
print(list)
new_list=[]

for waiting_list in list:
    print("user encrypted b vector")

    encrypted_vector = user.encrypt_vector(server.pubkey, waiting_list)
    print(encrypted_vector)

    encrypted_list.append(encrypted_vector)

new_list=server.multiplication_encrypted_vectors(encrypted_list)
print("step 2. server do multiplication and exponention for each time slot")
print(new_list)

final=[]
final=user.decrypt_vector(new_list,server.privkey,server.pubkey)
print("step 3. each user decrypted E schedule")
print(final)
size=len(final)
count=0
for i in range(0,size):
    if final[i]==0:
        print("The "+str(i+1)+"th slot is available for all users")
    else:
        count+=1
if count==size:
        print("There's no such time slot that all users are available")


