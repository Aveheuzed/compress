#!/usr/bin/env python3

"""
RLE compression ;
number_of_caracters, caracter
escape caracter = 0,len(escape)
"""

import io

#both function are designed for bytes/bytesarray
def rle(text):
        ans = list()
        escape = False
        coeff = 1
        char = text[0]#becomes a list when escape=True
        for car in text[1:] :
                if not escape :
                        if car == char :
                                coeff += 1
                                if coeff == 256 :
                                        ans.append(coeff-1)
                                        ans.append(char)
                                        coeff = 1
                        elif coeff == 1 :
                                escape = True
                                coeff = 2
                                char = [char,car]
                        else :
                                ans.append(coeff)
                                ans.append(char)
                                coeff,char = 1,car
                else :
                        if car == char[-1] :
                                char = char[:-1]
                                coeff -= 1
                                ans.append(0)
                                ans.append(coeff)
                                ans.extend(char)

                                escape = False
                                char = car
                                coeff = 2
                        elif coeff == 256 :
                                ans.append(0)
                                ans.append(0)#0 = 256%256
                                ans.extend(char)
                                coeff,char = 1,[car,]
                        else :
                                coeff += 1
                                char.append(car)
        if escape :
                ans.append(0)
        ans.append(coeff)
        if isinstance(char,list):
                ans.extend(char)
        else :
                ans.append(char)

        return bytes(ans)



def expand(text):
        text = io.BytesIO(text)
        ans = bytes()
        while 1 :
                coeff = text.read(1)
                if not len(coeff) :
                        break
                else :
                        coeff = ord(coeff)

                if not coeff :#escape = True ; zero added
                        coeff = ord(text.read(1))
                        if not coeff :
                                coeff = 256
                        ans += text.read(coeff)
                else :
                        ans += text.read(1)*coeff
        return ans
