`异形工厂游戏交流群(1163635014)`的群友`真·鸽子(1171049718)`问`梦想天生(Left_E)(445495653)`道：
```
小数点后的十进制转二进制有什么好方法？
```
`梦想天生`很快给出了足够好的解：
```
def b0(n):
    s = bin(int(n * 2**16))
    s = s[2:]
    while len(s) < 16:
        s = '0' + s
    return s[:len(s)-16] + '.' + s[-16:]
```
stackoverflow 有几个相关问题：  
https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex  
https://stackoverflow.com/questions/59226493/converting-float-numbers-to-binary  
https://stackoverflow.com/questions/8751653/how-to-convert-a-binary-string-into-a-float-value  
https://stackoverflow.com/questions/53538504/float-to-binary-and-binary-to-float-in-python  
https://stackoverflow.com/questions/4838994/float-to-binary  

下面几种简单改进
```
def b1(num):
    s = bin(int(num * 2**16))[2:]
    if len(s) < 16:
        return '.' + '0' * (16 - len(s)) + s
    else:
        return s[:len(s) - 16] + '.' + s[-16:]


def b2(num):
    s = bin(int(num * 2**16))[2:]
    if len(s) < 16:
        return ''.join(('.', ['0'] * (16 - len(s)), s))
    elif len(s) == 16:
        return '.' + s
    else:
        return s[:len(s) - 16] + '.' + s[-16:]


def b3(num, bits=16):
    s = bin(int(num * 2**bits))[2:]
    if len(s) <= bits:
        s1 = f'.{"0" * (bits - len(s))}{s}'
    else:
        s1 = f'{s[:len(s) - bits]}.{s[-bits:]}'
    return s1


def b4(num, bits=16):
    s = bin(int(num * 2**bits))[2:]
    if len(s) <= bits:
        return f'.{"0" * (bits - len(s))}{s}'
    else:
        return f'{s[:len(s) - bits]}.{s[-bits:]}'


def b5(num, bits=16):
    s = bin(int(num * 2**bits))[2:]
    if len(s) < bits:
        return ''.join(('.', ['0'] * (bits - len(s)), s))
    elif len(s) == bits:
        return '.' + s
    else:
        return s[:len(s) - bits] + '.' + s[-bits:]

```

先用不靠谱的timeit测一下，b2基本最优，引入位数变量用时增加一倍。

|n|b0|b1|b2|b3|b4|b5|c0|
|----|----|----|----|----|----|----|----|
|0.1|0.4392|0.2878|0.2944|0.4613|0.4630|0.4892|1.0095|
|0.125|0.3824|0.2963|0.2988|0.4688|0.4585|0.4978|1.1945|
|0.2|0.3833|0.2958|0.2972|0.4671|0.4642|0.5008|0.9837|
|0.3|0.3285|0.2882|0.2886|0.4585|0.4751|0.4740|0.9778|
|0.4|0.3298|0.2834|0.2889|0.4541|0.4511|0.4769|0.9969|
|0.5|0.2775|0.2741|0.2243|0.4504|0.4491|0.4203|1.1900|
|0.6|0.2802|0.2783|0.2273|0.4555|0.4580|0.4166|0.9683|
|0.7|0.2829|0.2712|0.2263|0.4541|0.4516|0.4224|0.9461|
|0.8|0.2841|0.2732|0.2255|0.4646|0.4532|0.4194|0.9553|
|0.9|0.2835|0.2770|0.2286|0.4542|0.4535|0.4197|0.9678|
|0.99|0.2869|0.2809|0.2270|0.4557|0.4444|0.4193|0.9468|
|1.1|0.3235|0.3167|0.3426|0.5193|0.5092|0.5554|1.0125|

在命令行在py3.8.10用pyperf测一下n=0.1s时的b0、b1、b2和b3a。
* 对于小于1的数，while循环表现不好；
* 对于大于1的数，单列相等比较有点浪费。
* b3a综合表现好，但f字符串在timeit中表现不好。
```
py -3.8 -m pyperf timeit -s "def f(n):" -s "  s = bin(int(n * 2**16))" -s "  s = s[2:]" -s "  while len(s) < 16:" -s "    s = '0' + s" -s "  return s[:len(s) - 16] + '.' + s[-16:]" "f(0.1)" --rigorous
py -3.8 -m pyperf timeit -s "def f(n):" -s "  s = bin(int(n * 2**16))[2:]" -s "  if len(s) < 16:" -s "    return '.' + '0' * (16 - len(s)) + s" -s "  else:" -s "    return s[:len(s) - 16] + '.' + s[-16:]" "f(0.1)" --rigorous
py -3.8 -m pyperf timeit -s "def f(n):" -s "  s = bin(int(n * 2**16))[2:]" -s "  if len(s) < 16:" -s "    return ''.join(('.', '0' * (16 - len(s)), s))" -s "  elif len(s) == 16:" -s "    return '.' + s" -s "  else:" -s "    return s[:len(s) - 16] + '.' + s[-16:]" "f(0.1)" --rigorous
py -3.8 -m pyperf timeit -s "def f(n):" -s "  s = bin(int(n * 2**16))[2:]" -s "  if len(s) < 16:" -s "    return f'.{"0" * (16 - len(s))}{s}'" -s "  elif len(s) == 16:" -s "    return '.' + s" -s "  else:" -s "    return f'{s[:len(s) - 16]}.{s[-16:]}'" "f(0.1)" --rigorous

n=0.1
485 +- 15 ns
325 +- 5 ns
327 +- 5 ns
321 +- 6 ns

n=0.5
317 6
310 6
262 5
264 7

n=1.1
353 8
351 6
371 5
352 6
```
引入有默认值的位数变量，在timeit中大幅减慢速度，在pyperf中也是。
```
py -3.8 -m pyperf timeit -s "def f(n, bits=16):" -s "  s = bin(int(n * 2**bits))[2:]" -s "  if len(s) < bits:" -s "    return f'.{"0" * (bits - len(s))}{s}'" -s "  elif len(s) == bits:" -s "    return '.' + s" -s "  else:" -s "    return f'{s[:len(s) - bits]}.{s[-bits:]}'" "f(0.1)" --rigorous

n=0.1
471 6 (+46.73%)

n=0.5
404 7 (+53.03%)

n=1.1
520 8 (+47.73%)
```