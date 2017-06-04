search = 3;
li = [1,2,3,4,5,6,7,8,9]

#単純検索
for l in li:
    if l == search:
        print(l);
        break;


#2分法
def check_num_in_list(li, num):
    low = 0
    high = len(li) - 1
    while len(li):
        mid = int(len(li) / 2)
        print("mid:",mid)
        return
        if li[mid] < num:
            low = mid
        elif li[mid] > num:
            high = mid
        else:
            return True;
        li = li[low:high]
        print("low:",low)
        print("high:", high)
    return False

search = 10;
li = [1,2,3,4,5,6,7,8,9]
print(check_num_in_list(li, search))
