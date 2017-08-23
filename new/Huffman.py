#!/usr/bin/env python3

"""
Format of a huffmanized string :
***header***
(a) length of a data block (bits) (on 8 bits)
(b) lenght of the smallest code -1 (bits) (on 8 bits)
(c) difference of length between the longest code and the shortest (bits) (on 8 bits)
(d) length of the dictionnary (keys) (on 8 bits)
***dictionnary***
key : a data block
value : length of the code that represents this data block - (b)
The dictionnary shows the keys in the order in witch they appear in the data
It is written as follows :
key1 value1 key2 value2
without any separator
The values are written on the smallest amount of bits necessary to write the longest code's length
(get it with (b) and (c))
***data***
an array of bits : codes reprensenting data blocks as given in the dictionnary
There is no separator ; zeros may be append to fill the last byte ;
their removing isn't currently implemented.
"""

import boolstring
import io

to_bytes = lambda string : boolstring.to_bytes([int(x) for x in string])
to_bool = lambda x,l : bin(x)[2:].zfill(l)
rbin = lambda x : int(x,base=2)
# def parse_dict(dictionnary,prefix=""):
#         #WARNING : this function isn't well build ; it is bugged
#         #this function is used to turn the Huffman tree (unknown deepness)
#         #into a flat (deepness=1) dictionnary as letter:code
#         #because of the unknown deepness, we use recursivity
#         receive = dict()
#         if len(dictionnary) == 2 :
#                 receive.update(parse_dict(dictionnary[0],prefix+"0"))
#                 receive.update(parse_dict(dictionnary[1],prefix+"1"))
#         else :
#                 receive[dictionnary[0][0]] = prefix
#         return receive


def parse_dict(d,prefix=""):
	receive = dict()
	if not isinstance(d[0],tuple):
		receive[d[0]] = prefix
	else :
		d = [x for x in d if not isinstance(x,int)]
		if len(d) == 2 :
			for i,x in enumerate(d):
				receive.update(parse_dict(x,prefix=prefix+str(i)))
		else :#we're sure that len(d) == 1 or 2 ; now, 2 is excluded
			receive.update(parse_dict(d[0],prefix=prefix))
	return receive

#this one is a bit slower
# def parse_dict(d,prefix=""):
# 	receive = dict()
# 	for i,x in enumerate(d):
# 		if isinstance(x,tuple):
# 			receive.update(parse_dict(x,prefix=prefix+str(i)))
# 		elif not i :
# 			receive[x] = prefix
# 	return receive



#Both functions are designed to be used with bytes / bytesarray
def huffmanize(string):
        charset = set(string)
        dictionnary = [(char,string.count(char)) for char in charset]
        while len(dictionnary) > 1 :
                dictionnary.sort(key=lambda x:x[1])
                i0,i1 = dictionnary.pop(0),dictionnary.pop(0)
                count = i0[1]+i1[1]
                dictionnary.append(((i0,i1),count))
                #there we have our Huffman tree,
                #now we d'like the code associated with each char
        dictionnary = parse_dict(dictionnary)
        charset = list(charset)
        charset.sort(key=lambda x:string.index(x))

        #now we just have to build the output.
        output = str()
        _ = dictionnary.values()
        m,M = len(min(_,key=len)), len(max(_,key=len))
        m_,M_ = m-1, M-m
        L = len(bin(M_))-2#this -2 represents the '0b' at the beginning of bin(...)
        output += to_bool(m_,8)
        output += to_bool(M_,8)
        output += to_bool(len(_),8)
        for char in charset :
                output += to_bool(char,8)
                l = len(dictionnary[char])
                l -= m
                output += to_bool(l,L)

        #now come the data itself.
        for char in string :
                output += dictionnary[char]

        #now, converting to bytes :
        i = 0
        while len(output)%8 != 5 :#5 = 8-3, because we will add 3 bits just after
                output += "0"
                i += 1
        output = to_bool(i,3)+output

        return to_bytes(output)

def dehuffmanize(string):
        string = "".join(str(int(x)) for x in boolstring.to_bool(string))
        added = rbin(string[:3])
        string = string[3:-added]


        string = io.StringIO(string)
        m,M = rbin(string.read(8)), rbin(string.read(8))
        L = len(bin(M))-2
        m += 1
        M += m
        len_dict = rbin(string.read(8))
        dictionnary = dict()
        order = list()
        for i in range(len_dict):
                _ = rbin(string.read(8))
                dictionnary[_] = rbin(string.read(L))+m
                order.append(_)

        #headers done, now come the data
        order = iter(order)
        met = dict()
        output = list()

        code = ""
        while 1 :
                new = string.read(1)
                if not len(new):
                        break
                code += new

                if code in met.keys():
                        output.append(met[code])
                        code = ""
                elif any(x.startswith(code) for x in met.keys()) :
                        continue
                else :#we got a new letter
                        char = next(order)
                        len_code = dictionnary[char]
                        code += string.read(len_code-len(code))
                        met[code] = char
                        code = ""
                        output.append(char)
        return bytes(output)
