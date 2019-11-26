primes = [2]
for x in range(2, 50):
    if x % 2: # passes all odd numbers 
        for p in primes:
            if x % p == 0: # if a number in primes array divides into x perfectly then it is not a prime number 
                break # exits the loop and skips the else 
        else:
            primes.append(x)
# print("The prime numbers from 2 to 50 are: ")
# print(primes)