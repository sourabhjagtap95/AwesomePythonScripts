def check_repeat(row):
    if len(row) != len(set(row)):
        return False
    return True


def check_elements(row, ref):
    for item in row:
        if item not in ref:
            return False
    return True


def row_wise(arr, ref):
    for row in arr:
        if check_elements(row, ref) == False or check_repeat(row) == False:
            return False
    return True


def col_wise(arr, ref):
    num = len(arr[0])
    for pos in range(num):
        temp_list = []
        for iter_col in range(num):
            temp_list.append(arr[iter_col][pos])
        if check_elements(temp_list, ref) == False or check_repeat(temp_list) == False:
            return False
    return True


def check_sudoku(arr):
    # check flags
    flags = [False, False]
    # collect elements
    ref = [x for x in range(1, len(arr[0]) + 1)]
    # checking row wise
    flags[0] = row_wise(arr, ref)
    # check column wise
    flags[1] = col_wise(arr, ref)
    # return answer
    if False in flags:
        return False
    return True


correct = [[1,2,3],
           [2,3,1],
           [3,1,2]]

print(len(correct[0]))
print(check_sudoku(correct))
