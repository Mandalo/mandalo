'''
@A -> shoulb be a numeric array
@start -> lower bound of the array
@end -> higher bound of array
'''
def max_subarray(A, start, end):
    if start < 0 or end > len(A):
        raise IndexError("Out of bounds")
    temp_max = 0
    total_max = A[start]
    left = 0
    right = 0
    temp_left = 0
    for x in range(start, end):
        temp_max = max(0, temp_max + A[x])
        if temp_max > total_max:
            total_max = temp_max
            right = x
            left = temp_left
        if temp_max == A[x]:
            temp_left = x
    return total_max

def get_results(A, start, end):
    result = max_subarray(A, start, end)
    print ('Sum: {}'.format(result))


def main():
    array = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    get_results(array, 0, len(array))

if __name__ == '__main__':
    main()
