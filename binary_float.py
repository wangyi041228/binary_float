from timeit import timeit


def b0(n):
    s = bin(int(n * 2 ** 16))
    s = s[2:]
    while len(s) < 16:
        s = '0' + s
    return s[:len(s) - 16] + '.' + s[-16:]


def b1(num):
    s = bin(int(num * 2 ** 16))[2:]
    if len(s) < 16:
        return '.' + '0' * (16 - len(s)) + s
    else:
        return s[:len(s) - 16] + '.' + s[-16:]


def b2(num):
    s = bin(int(num * 2 ** 16))[2:]
    if len(s) < 16:
        return ''.join(('.', '0' * (16 - len(s)), s))
    elif len(s) == 16:
        return '.' + s
    else:
        return s[:len(s) - 16] + '.' + s[-16:]


def b3a(num):
    s = bin(int(num * 2 ** 16))[2:]
    if len(s) < 16:
        return f'.{"0" * (16 - len(s))}{s}'
    elif len(s) == 16:
        return '.' + s
    else:
        return f'{s[:len(s) - 16]}.{s[-16:]}'


def b3(num, bits=16):
    s = bin(int(num * 2 ** bits))[2:]
    if len(s) <= bits:
        s1 = f'.{"0" * (bits - len(s))}{s}'
    else:
        s1 = f'{s[:len(s) - bits]}.{s[-bits:]}'
    return s1


def b4(num, bits=16):
    s = bin(int(num * 2 ** bits))[2:]
    if len(s) <= bits:
        return f'.{"0" * (bits - len(s))}{s}'
    else:
        return f'{s[:len(s) - bits]}.{s[-bits:]}'


def b5(num, bits=16):
    s = bin(int(num * 2 ** bits))[2:]
    if len(s) < bits:
        return ''.join(('.', '0' * (bits - len(s)), s))
    elif len(s) == bits:
        return '.' + s
    else:
        return s[:len(s) - bits] + '.' + s[-bits:]


def c0(num):
    t0 = float.hex(num - int(num) + 1)  # 小数部分+1 得16进制文本
    t1 = t0[4:-3]  # 去头去尾
    t2 = bin(int(t1, base=16))  # 二进制整数
    t3 = t2[2:]  # 去头
    t4 = '0' * (((len(t3) - 1) // 4 + 1) * 4 - len(t3)) + t3.rstrip('0')  # 补头0  去尾0
    return t4


def main():
    tests = [0.1, 0.125, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.1]
    print(f'|n|b0|b1|b2|b3|b4|b5|c0|')
    print(f'|----|----|----|----|----|----|----|----|')
    for n in tests:
        # print(b0(n))
        r0 = timeit('b0(n)', setup=f'from __main__ import b0; n = {n}')
        # print(b1(n))
        r1 = timeit('b1(n)', setup=f'from __main__ import b1; n = {n}')
        # print(b2(n))
        r2 = timeit('b2(n)', setup=f'from __main__ import b2; n = {n}')
        # print(b3(n))
        r3 = timeit('b3(n)', setup=f'from __main__ import b3; n = {n}')
        # print(b4(n))
        r4 = timeit('b4(n)', setup=f'from __main__ import b4; n = {n}')
        # print(b4(n))
        r5 = timeit('b5(n)', setup=f'from __main__ import b5; n = {n}')
        # print(c0(n))
        r6 = timeit('c0(n)', setup=f'from __main__ import c0; n = {n}')
        print(f'|{n}|{r0:.4f}|{r1:.4f}|{r2:.4f}|{r3:.4f}|{r4:.4f}|{r5:.4f}|{r6:.4f}|')


if __name__ == '__main__':
    main()
