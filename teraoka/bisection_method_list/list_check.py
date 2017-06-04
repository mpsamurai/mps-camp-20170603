x = [1,2,3,4,5]
y = 3
for key in x:
    if key == y:
        print("OK")

































#
# low = 0
# high = len(x)
# # t は中央番目の数
# t = (low + high) / 2
#
# # 探索の下限のlowが上限のhighになるまで探索
# # lowがhighに達すると数は見つからなかったということ
# while (low<=high):
#     if (i==x[t]):
#         break
#     elif (i > x[t]):
#         low = t + 1
#     elif (i < x[t]):
#         high = t - 1
#     t = (low + high) / 2
#
# if (i==x[t]):
#     print str(t + 1) + "番目にあります"
# else:
#     print "ありません"
#
#
#
#
#
#
# x = 27
# epsilon = 0.01
# num_guesses = 0
# low = min(-1.0, x)
# high = max(1.0, x)
# ans = (high + low) / 2.0
#
# pwr = 3
#
# while abs(ans**pwr - x) >= epsilon:
#     print('low =', low, 'high =', high, 'ans =', ans)
#     num_guesses += 1
#     if ans**pwr < x:
#         low = ans
#     else:
#         high = ans
#     ans = (high + low) / 2.0
#
# print('num_guesses =', num_guesses)
# print(ans, 'is close to square root of', x)