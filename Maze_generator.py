import copy, random

arr_gen = lambda x, y: [[0 for _ in range(x)] for _ in range(y)]
arr_print = lambda matrix: [print(row) for row in matrix]

def maze_gen(x_line, y_line):
    matrix = arr_gen(x_line, y_line)
    right_border = copy.deepcopy(matrix)
    under_border = copy.deepcopy(matrix)
    under_chek = 0
    array_chek = 0
    array_interrupt = False

    for num_l, line in enumerate(matrix):

        for num_i, itm in enumerate(line):
            if random.randint(1,3) == 1:
                right_border[num_l][num_i] = 1
                array_interrupt = True
            else: array_chek += 1

            if random.randint(1, 3) == 1:
                under_border[num_l][num_i] = 1
                if array_interrupt is True and array_chek == under_chek:
                    under_border[num_l][num_i] = 0
                under_chek += 1

            if array_interrupt is True:
                under_chek = 0
                array_chek = 0
                array_interrupt = False

            if num_i == len(line) - 1:
                right_border[num_l][num_i] = 1

        if num_l == len(matrix) - 1:
            under_border[num_l] = [1] * x_line

    return right_border, under_border


right_border, under_border = maze_gen(10, 15)

print('\nright_border\n')
arr_print(right_border)
print('\nunder_border\n')
arr_print(under_border)
