from Network import Network

def read_data(file_full_path: str) -> tuple:
    input_list = []
    output_direction = []
    output_velocity = []
    with open(file_full_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line is not '\n':
                if line[0] != '1' and line[2] != '1' and line[4] != '1' and line[6] != '1':
                    line_numbers = line.split(" ")
                    input_inline = []
                    output_inline_1 = []
                    output_inline_2 = []
                    for number in line_numbers[0:4]:
                        input_inline.append(float(number))
                    for number in line_numbers[4:6]:
                            output_inline_1.append(float(number))

                    for number in line_numbers[6:]:
                        output_inline_2.append(float(number))

                    input_list.append(input_inline)
                    output_direction.append(output_inline_1)
                    output_velocity.append(output_inline_2)

    return input_list, output_direction, output_velocity

def get_train_weights(batch_size: int ):
    nn_direction = Network([4, 6, 2])
    nn_velocity = Network([4, 6, 2])

    input_data, output_data_direction, output_data_velocity = read_data('train_data1.txt')

    print("DIRECTION:")
    for step in range(0, len(input_data), batch_size):
        nn_direction.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+batch_size], output_data_direction[step:step+batch_size])

    print("VELOCITY:")
    for step in range(0, len(input_data), batch_size):
        nn_velocity.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+batch_size], output_data_velocity[step:step+batch_size])


    input_data, output_data_direction, output_data_velocity = read_data('train_data2.txt')

    print("DIRECTION:")
    for step in range(0, len(input_data), batch_size):
        nn_direction.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+batch_size], output_data_direction[step:step+batch_size])

    print("VELOCITY:")
    for step in range(0, len(input_data), batch_size):
        nn_velocity.session_train(0.2, 0.0000001, [0.8, 0.8], input_data[step:step+batch_size], output_data_velocity[step:step+batch_size])

    return nn_direction, nn_velocity
