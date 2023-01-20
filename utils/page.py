def create_page(num, limit, data):
    start = (num - 1) * limit
    end = num * limit
    len_s = len(data)
    if len_s < end:
        end = len_s
    arr_list = []
    count = 0
    print(start,end)
    for node in data:
        if count < start - 1:
            count += 1
        elif start - 1 <= count <= end - 1:
            count += 1
            arr_list.append(node)
        else:
            break
    return arr_list
