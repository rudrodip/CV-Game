filename = './game/calib.txt'

def read():
    text = check()
    if text:
        data = text.split(' ')
        calib = [
            [int(data[0]), int(data[1])],
            [int(data[2]), int(data[3])],
            bool(int(data[4]))
        ]
        return calib
    return None

def check():
    with open(filename, 'r') as f:
            text = f.read()
            if len(text) > 1:
                if int(text[-1]):
                    return text
    return None

def write(data):
    with open('./game/calib.txt', 'w') as f:
        f.write(f'{data[0][0]} {data[0][1]} {data[1][0]} {data[1][1]} {int(data[2])}')

    print('calibration file written successfully')