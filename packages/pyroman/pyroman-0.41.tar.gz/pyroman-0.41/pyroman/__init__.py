roman = {
    0: '',
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII',
    8: 'VIII',
    9: 'IX',
    10: 'X',
    20: 'XX',
    30: 'XXX',
    40: 'XL',
    50: 'L',
    60: 'LX',
    70: 'LXX',
    80: 'LXX',
    90: 'XC',
    100: 'C',
    200: 'CC',
    300: 'CCC',
    400: 'CD',
    500: 'D',
    600: 'DC',
    700: 'DCC',
    800: 'DCCC',
    900: 'CM',
    1000: 'M',
    2000: 'MM',
    3000: 'MMM',
    4000: 'MV',
    5000: 'V̅',
    6000: 'V̅M',
    7000: 'V̅MM',
    8000: 'V̅MMM',
    9000: 'MX̅',
    10000: 'X̅',
    20000: 'X̅X̅',
    30000: 'X̅X̅X̅',
    40000: 'X̅L̅',
    50000: 'L̅',
    60000: 'L̅X̅',
    70000: 'L̅X̅X̅',
    80000: 'L̅X̅X̅X̅',
    90000: 'X̅C̅',
    100000: 'C̅',
    200000: 'C̅C̅',
    300000: 'C̅C̅C̅',
    400000: 'C̅D̅',
    500000: 'D̅',
    600000: 'D̅C̅',
    700000: 'D̅C̅C̅',
    800000: 'D̅C̅C̅C̅',
    900000: 'C̅M̅',
    1000000: 'M̅'
}
validLetters = 'IVXLCDMV̅X̅L̅C̅D̅M̅'


def _getInt(val):
    for key, value in roman.items():
        if val == value:
            return key
    return None


def intToRoman(num):
    if type(num) == str:
        try:
            num = int(num)
        except:
            raise ValueError('Enter valid number.')
    if type(num) == float:
        raise ValueError("Invalid Number.")
    if type(num) == int:
        if num > 1999999:
            raise ValueError('Too big number.')
        num = str(num)
    num = [int(i) for i in num]
    num.reverse()
    num = [num[i] * (10**i) for i in range(len(num))]
    num.reverse()
    ret = ''
    for i in num:
        ret += roman[i]
    return ret


def romanToInt(rom):
    if type(rom) != str:
        raise TypeError('String not passed.')
    rom = rom.upper()
    for i in rom:
        if i not in validLetters:
            raise ValueError('Not a valid Roman Number.')
    num = ''
    #print(rom, end=': ')
    while True:
        if len(rom) == 0:
            break
        elif len(rom) == 1:
            num = str(int(_getInt(rom) / (10**len(num)))) + num
            rom = ''
        else:
            for i in range(1, 6):
                #print('loop:', i)
                #print('rom:', rom)
                #print('num:', num)
                if len(rom) < i:
                    num = str(int(
                        _getInt(rom[-1 * (i - 1):]) / (10**len(num)))) + num
                    rom = rom[:-1 * (i - 1)]
                    break
                temp = _getInt(rom[-1 * i:])
                if temp == None and _getInt(rom[-1 * (i - 1):]) != None:
                    num = str(int(
                        _getInt(rom[-1 * (i - 1):]) / (10**len(num)))) + num
                    rom = rom[:-1 * (i - 1)]
                    #print('Break in main area')
                    break
                else:
                    pass

    return int(num)


if __name__ == '__main__':
    print(intToRoman('99878'))
    #print(_getInt('III'))
    #for i in range(1, 100000):
    #    print(romanToInt(intToRoman(i)))
    print(romanToInt('X̅C̅MX̅DCCCLXXVIII'))