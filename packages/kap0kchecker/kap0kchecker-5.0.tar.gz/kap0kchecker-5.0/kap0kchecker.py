import sys
def checkflag():
    cipher = [0x6b,0x41,0x50,0x10,0x4b,0x5b,0x6c,
        0x11,0x46,0x13,0x7f,0x11,0x53,0x7f,
        0x53,0x48,0x10,0x52,0x17,0x7f,0x69,
        0x7f,0x55,0x53,0x13,0x7f,0x70,0x59,
        0x17,0x48,0x10,0x4e,0x5d]
    
    print("please input your flag:")
    if sys.version > '3':
        flag = input()
    else:
        flag = raw_input()
    if(len(flag) != 33 ):
        print("Wrong flag")
        return 0
    else:
        for i in range(33):
            if(ord(flag[i])^0x20 != cipher[i]):
                print("Wrong flag")
                return 0
        print("You win,the flag is " + flag)
        return 1



            