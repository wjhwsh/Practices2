def getHex(dec):
    print "Hexadecimal:%x" % int(dec)
def getDec(hex):
    print "Decimal: ",
    print int(str(hex), 16)

if __name__ == '__main__':
    mode = raw_input("Which mode?\n0. Hex -> Dec\n1. Dec -> Hex")
    number = raw_input("Enter the number: ")
    if mode == '0':
        getDec(number)
    else:
        getHex(number)

