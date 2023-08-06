def CheckIsPrime(x):
    is_prime = True
    for i in range(2, x):
        if x%i == 0:
            # print(x,'不是質數')
            is_prime = False
            break
    return is_prime