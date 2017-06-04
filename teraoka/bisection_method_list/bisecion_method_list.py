x = [1,2,3,4,5,6,7,8,9,10]
y = 9
print(y)
low = 0
high = len(x) -1
print(high)
print(x[high])
z = round((x[low] + x[high]) / 2) # 中央値
print(z)
while low<=high:
    if y == x[z]:
        print("z", x[z])
        print("見つかった！")
        break
    elif y > x[z]:
        print("x[z]", x[z])
        low = y
    elif y < x[z]:
        high = y
        z = round((x[low] + x[high]) / 2)
    else:
        print("ありませんでした")































































