from Network import Network

def read_data(file_full_path: str) -> tuple:
    input_list = []
    output = []
    with open(file_full_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line is not '\n':
                if line[0] != '1' and line[2] != '1' and line[4] != '1' and line[6] != '1':
                    line_numbers = line.split(" ")
                    input_inline = []
                    output_inline = []
                    for number in line_numbers[0:4]:
                        input_inline.append(float(number))
                    for number in line_numbers[4:]:
                        output_inline.append(float(number))

                    input_list.append(input_inline)
                    output.append(output_inline)

    return input_list, output

def get_train_weights():
    nn = Network([4, 5, 4])

    input_data, output_data = read_data('train_data1.txt')

    for step in range(0, len(input_data), 5):
        nn.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+100], output_data[step:step+100])

    nn.print_loss(input_data, output_data)

    input_data, output_data = read_data('train_data2.txt')

    for step in range(0, len(input_data), 5):
        nn.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+100], output_data[step:step+100])

    nn.print_loss(input_data, output_data)

    return



