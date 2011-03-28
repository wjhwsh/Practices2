def sort(number):
    realsort(number, 0, len(number) - 1)

def realsort(number, left, right):
    if left < right:
        s = number[left]
        i = left
        j = right + 1
        while True:
            while i + 1 < len(number):
                i += 1
                if number[i] >= s:
                    break
            while j - 1 > -1:
                j -= 1
                if number[j] <= s:
                    break
            if i >= j:
                break
            number[i], number[j] = number[j], number[i]
        number[left], number[j] = number[j], number[left]
        realsort(number, left, j - 1)
        realsort(number, j + 1, right)
list = [2,1,4,5,3]
sort(list)
print list
