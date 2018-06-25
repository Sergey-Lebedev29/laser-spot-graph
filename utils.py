

def get_map(image):
    image_ = image.convert(mode='L')
    matrix = []
    for i in range(image_.height):
        row = []
        for j in range(image_.width):
            row.append(image_.getpixel((j, i)) / 64)
        matrix.append(row)
    return matrix


def get_segment(value, delta, map_length):
    right_value = value + delta
    left_value = value - delta

    if right_value > map_length and left_value < 0:
        left_value = 0
        right_value = map_length
    elif right_value > map_length:
        dd = right_value - map_length
        right_value = map_length
        left_value = left_value - dd if dd < left_value else 0
    elif left_value < 0:
        dd = - left_value
        left_value = 0
        right_value = right_value + dd if right_value + dd < map_length else map_length

    return left_value, right_value


def get_avg_by_y(y, delta, _map):
    left_value, right_value = get_segment(y, delta, len(_map))
    rows = list()
    count = right_value - left_value
    for i in range(left_value, right_value):
        rows.append(_map[i])
    result = [sum(x) / float(count) for x in zip(*rows)]
    return result


def get_avg_by_x(x, delta, _map):
    left_value, right_value = get_segment(x, delta, len(_map))
    rows = list()
    count = right_value - left_value
    for i in range(left_value, right_value):
        rows.append([row[i] for row in _map])
    result = [sum(n) / float(count) for n in zip(*rows)]
    return result
