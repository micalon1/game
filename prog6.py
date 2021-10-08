def find_highest_in_file(file_name):
    f = open(file_name, "r")
    high = -10000000000000000000000000000
    for i in f:
        try:
            n = int(i)
            if n > high:
                high = n
        except:
            return False
    return high
    f.close()

def find_matches(input_file, output_file, s, v):
    first_file = open(input_file, "r")
    sec_file = open(output_file, "w")
    count = 0
    for line in first_file:
        if v == True and s in line:
            sec_file.write(line)
            count += 1
        if v == False and s not in line:
            sec_file.write(line)
            count += 1
    return count
    first_file.close()
    sec_file.close()

def draw_entity(entity, lists):
    try:
        if entity.top_left_x >= 0 and entity.top_left_y >= 0 and entity.top_left_x + (entity.width - 1) <= len(lists[0]) and entity.top_left_y + (entity.height - 1) <= len(lists[0]):
            for row in range(entity.top_left_y, entity.top_left_y + entity.height):
                for index in range(entity.top_left_x, entity.top_left_x + entity.width):
                    lists[row][index] = entity.icon
            return True
    except:
        return False
    e.close()