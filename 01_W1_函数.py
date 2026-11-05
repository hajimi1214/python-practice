# -*- coding: utf-8 -*-
"""
================================================================
  01_W1_函数.py        W1（10/29 - 11/04）收尾六题
================================================================

怎么用：

  1. 每道题下面都有一个 def，里面只有一行 raise NotImplementedError
  2. 把那行删掉，写你自己的代码
  3. 保存
  4. 回到文件夹，双击运行 `跑一下.py`（或者命令行 python 跑一下.py）
  5. 它会告诉你哪题过了、哪题错在哪

  raise NotImplementedError 的意思是「这题还没写」。
  跑一下.py 看到它会显示「未做」，那不是报错，是提醒。


规则（就两条）：

  · 不要复制粘贴，一个字母一个字母敲。中文引号 '' 「」 用在代码里会
    直接 SyntaxError，手敲一次你就永远记住了。
  · 卡超过 30 分钟就先跳过下一题。绕过也是一种经历。

写完这 6 题 = W1 毕业。
================================================================
"""


# ============================================================

def average(nums):
    total = 0
    for num in nums:
        total += num
    if len(nums) == 0:
        return 0
    else:
        return total / len(nums)


res = average([80, 90, 100])
print(res)


# ============================================================

n=100
def is_even(n):
    num = n % 2
    if num == 0:
        return True
    else:
        return False

print(is_even(n))


# ============================================================

c = 100
def c_to_f(c):
    m = c * 9 / 5 + 32
    return m
print(c_to_f(c))


# ============================================================
names = (['张三','李四','王五'])

def print_names(names):
    for i in names:
        print(i)


# ============================================================
score = 90
def grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'E'
print(grade(score))


# ============================================================
def sum_1_to_100():
    num = 0
    for i in range(1,101):
        num += i
    return num
print(sum_1_to_100())


