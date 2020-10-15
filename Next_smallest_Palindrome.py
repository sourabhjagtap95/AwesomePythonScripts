import sys
def Next_smallest_Palindrome(num):
    numstr = str(num)
    for i in range(num+1,sys.maxsize):
        if str(i) == str(i)[::-1]:
            return i

print(Next_smallest_Palindrome(99));
print(Next_smallest_Palindrome(1221));
