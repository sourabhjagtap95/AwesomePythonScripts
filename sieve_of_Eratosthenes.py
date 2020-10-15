def sieve_of_Eratosthenes(num):
    limitn = num+1
    not_prime_num = set()
    prime_nums = []

    for i in range(2, limitn):
        if i in not_prime_num:
            continue

        for f in range(i*2, limitn, i):
            not_prime_num.add(f)

        prime_nums.append(i)

    return prime_nums

print(sieve_of_Eratosthenes(100));
