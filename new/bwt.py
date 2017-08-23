#!/usr/bin/env python3

"""Burrows-Wheeler transformation (BWT)
do and undo are the brute algorithm, as described on wikipedia
while doo and undoo are optimized, in terms of memory and CPU"""

def do(string):
        #this function compresses
        string_ = string
        work = list()
        for i in range(len(string)):
                work.append(string)
                string = string[-1:]+string[:-1]
        work.sort()
        return int.to_bytes(work.index(string_),4,"big") + bytes([x[-1] for x in work])


def undo(string):
        #this function expands
        index, string = int.from_bytes(string[:4],"big"), string[4:]

        work = [list() for i in string]

        while len(work[0]) < len(string):
                [row.insert(0,x) for row,x in zip(work,string)]
                work.sort()
        return bytes(work[index])


#those functions are to be optimized for being used with huge amounts of data

# def doo(string):
#         #this function compresses
#         string2 = string+string
#         i = 1
#         #here comes a complicated line that says :
#         #while the i first caracters of ANY slice of string
#         #are not enough to determine where it has been picked in the string,
#         #then i +=1
#         #the goal is to work on only the beginning of the string,
#         #but still to ensure a correct sorting
#         while len(set(string2[index:index+i] for index in range(len(string)))) < len(string):
#                 i += 1
#         del string2
#
#         string_ = string[:i]+string[-1:]#the original string shortened
#         work = list()
#         for _ in range(len(string)):
#                 work.append(string[:i]+string[-1:])
#                 string = string[-1:]+string[:-1]
#         work.sort()
#         return int.to_bytes(work.index(string_),4,"big") + bytes([x[-1] for x in work])

def _max_id_letters(string):
        """This function returns the max number of consecutive letters in string
        ex : b'world' => 1
        b'hello world' => 2 bc. 'll'"""
        i = 0
        last = -1
        j = 0
        for x in string :
                if x == last :
                        j += 1
                else :
                        j = 1
                        last = x

                if j > i :
                        i = j
        return i

def doo(string):
        string2 = string+string
        if string[0] == string[-1]:
                i = _max_id_letters(string2)
        else :
                i = _max_id_letters(string)

        string = list(string)
        original = string.pop()
        string.append(256)#256 = 255 (max value of 1 byte) +1
        f = lambda x:original if x == 256 else x

        string = list(sorted(enumerate(string),key=lambda x:f(string2[x[0]+1:x[0]+i+1])))
        string = list(x for i,x in string)
        return int.to_bytes(string.index(256),4,"big") + bytes(f(x) for x in string)

def _find_nth(string,letter,n):
        """This function finds the nth (n>1) letter in string and returns its index.
        It uses *.index, and thus has the same output"""
        assert n >= 1
        start = -1
        while n >= 1 :
                start = string.index(letter,start+1)
                n -= 1
        return start

def undoo(string):
        index, string = int.from_bytes(string[:4],"big"), list(string[4:])
        sorted_string = list(sorted(string))
        out = list()
        while len(out) < len(string):
                letter = sorted_string[index]
                out.append(letter)

                index = _find_nth(string, letter, \
                sorted_string[:index+1].count(letter))
        return bytes(out)
