
if __name__ == '__main__':
    threshold = 5
    lst = [3, 8, 2, 10, 7, 4]
    sorted_indexes = [i for i, x in sorted(enumerate(lst), key=lambda x: x[1]) if x >= threshold]
    k =0