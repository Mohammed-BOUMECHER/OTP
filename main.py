import os
import argparse
import sys



def generate (parent_dir):

    '''

    :param: parent_dir :

    '''

    # Parent Directory path 


    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    i = 0
    f = os.path.join(parent_dir, '0000')

    while os.path.exists(f):
        i += 1
        f = os.path.join(parent_dir, str(i).rjust(4, '0'))    

    os.makedirs(f) # create 0000 files

    for index in range(0, 100):
        name = os.path.join(f, str(index).rjust(2, '0'))
        f1, f2, f3 = name+'p.txt', name+'c.txt', name+'s.txt'

        File1 = open(f1, "a")
        File2 = open(f2, "a")
        File3 = open(f3, "a")

        with open("/dev/urandom", 'rb') as s:
            for x in s.read(48):     
                File1.write(bin(x)[2:].rjust(8, '0'))

            for x in s.read(2000):
                File2.write(bin(x)[2:].rjust(8, '0')) 

            for x in s.read(48):
                File3.write(bin(x)[2:].rjust(8, '0'))

        File1.close()
        File2.close()
        File3.close()



def get(path):
    '''
    
    '''
    folder = path + '/' + os.listdir(path)[0] + '/'
    print('--',folder)

    for x in range(100):
        fileP = folder + '{0:02}'.format(x) + 'p.txt'
        fileC = folder + '{0:02}'.format(x) + 'c.txt'
        fileS = folder + '{0:02}'.format(x) + 's.txt'
        if os.path.isfile(fileC):
            break

    return fileP,fileC,fileS


def convert_text_to_Bin(text):
    '''
    convert text to binary
    :param text:str
    :return byte_list: list
    '''
    strBin = ""
    a_byte_array = bytearray(text, "utf8")
    byte_list = []
    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(binary_representation.replace("b", "").rjust(8,'0'))
    for i in byte_list:
        strBin = strBin + i
    return strBin



def send (data, c, p, s):
    '''

    '''
    # read pad prefix and suffix
    f_pad = open(c, "r")
    pad = f_pad.read()

    f_pref = open(p, "r")
    prefix = f_pref.read()
    
    f_suff = open(s, "r")
    suffix = f_suff.read()

    f_pad.close()
    f_pref.close()
    f_suff.close()

    Bdata = ""
    Bdata = convert_text_to_Bin(data)
    #print('---  >>',Bdata)
    y = int(Bdata,2) ^ int(pad,2)
    y = bin(y)[2:].zfill(len(pad))
    print('***',y)


################## Main Function ##################
if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", '--generate', action='store_true')
    parser.add_argument("-s", '--send', action='store_true')
    parser.add_argument("-t", '--text')
    parser.add_argument('dir')
    parser.add_argument("-f", '--file')
    args = parser.parse_args()

    if (args.generate):
        generate(args.dir)

    elif (args.send):
        print('mode s')
        # send mode
        if args.file:
            data = args.file
            with open(args.file, 'r') as file:
                data = file.read().replace('\n', '')
        elif args.text:
            data = args.text
        else:
            data = input("Text: ")

        if(len(data) > 2000):
            print("Can't encode text, because pad too short")

        # Get the first pad available path    
        prefix, c_available, suffix = get(args.dir)
        print('-->',prefix)

        # funcition encode (data, pad) (bin then xor)
        send(data, c_available, prefix, suffix)

