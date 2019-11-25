primes = [2]
for x in range(2, 50):
    if x % 2:
        for p in primes:
            if x % p == 0:
                break # exits the loop and skips the else 
        else:
            primes.append(x)
print("The prime numbers from 2 to 50 are: ")
print(primes)