
morse_code = ("-.-.--",".--.-.",".-...","-.--.","-.--.-",   #1
"T",".-.-.","-...-","-----",".----",                        #2
"..---","...--","....-",".....","-....",                    #3
"--...","---..","----.",".-","-...",                        #4
"-.-.","-..",".","..-.","--.",                              #5
"....","..",".---","-.-",".-..",                            #6
"--","-.","---",".--.","--.-",                              #7
".-.","...","-","..-","...-",                               #8
".--","-..-","-.--","--..","---...",                        #9
".-..-.",".----.","--..--","E",                             #10
"-..-.","..--..","\\")                                      #11

alphabet_code = ("!","@","&","(",")",                       #1
"-","+","=","0","1"                                         #2
"2","3","4","5","6",                                        #3
"7","8","9","A","B",                                        #4
"C","D","E","F","G",                                        #5
"H","I","J","K","L",                                        #6
"M","N","O","P","Q",                                        #7
"R","S","T","U","V",                                        #8
"W","X","Y","Z",":",                                        #9
"\"","\'",".",",",".",                                      #10
"/","?"," ") 

def encrypt(message):
    message=message.upper()
    encrypt_message = ''
    for i in message:
        try:
            index_morse = alphabet_code.index(i)
            encrypt_message = encrypt_message + morse_code[index_morse] + " "
        except:
            print("Invalid characters in input!!")
            return False

    return encrypt_message


def decrypt(message):
    message = message.split()
    decrypt_message = ''
    for i in message:
        try:
            index_alphabet = morse_code.index(i)
            decrypt_message = decrypt_message + alphabet_code[index_alphabet] + " "
        except:
            print("Invalid characters in input!!")
            return False

    return decrypt_message