#!/usr/bin/env python27
import fractions
import re
import sys


def printFrobeniusNumber(strDenotation):
    """Outputs the Frobenius number (if any) of a Numerical Subgroup."""

    # Make sure we can parse the string into an array of integers
    try:
        numbers = map(int, strDenotation.split(','))
    except ValueError as e:
        print "Invalid format of Subset denotation. Please try again."
        return


    # Perform some initial checks to see if it is possible for the list
    # to have a Frobenius number.
    setNum = set(numbers)
    if len(numbers) != len(set(numbers)):
        print "<A> cannot contain duplicate numbers. Please try again."

    elif len(setNum.intersection([0])) > 0:
        print "The denotation cannot contain the number 0. Please try again."

    elif len(setNum.intersection([1])) > 0:
        print ("For a nummerical subgroup that includes 1, there will be no " +
            "gaps and hence no Frobenius number.")

    elif len(numbers) < 2:
        print "<A> has to consist of a minimum of two numbers. Please try again."

    elif reduce(fractions.gcd, numbers) > 1:
        print ("The greatest common divisor of <A> cannot be greater than 1. " +
            "Please try again.")

    else:

        # Now we have established that the numbers are a valid denotation for
        # a nummerical Subset and can start doing the actual calulations.

        if len(numbers) == 2:
            # When the dimension of the numbers, is two, then we can use the
            # proven formula for determining the Frobenius number:
            # <A> = <a,b> = S  =>  (a-1)(b-1)-1 = F(S)
            print "The Frobenius number is %s" % (
                    (numbers[0]-1) * (numbers[1]-1) - 1
                )

        else:
            # Otherwise we have to perform som additional checks. But we can
            # safely assume that it will not be greater than the Frobenius
            # number of the Subset that is made up of the two smallest integers
            # in the list. So that is our benchmark.
            numbers.sort()
            max_frob = (numbers[0]-1) * (numbers[1]-1) - 1
            i = max_frob
            while i > 0:
                sys.stdout.write("\rTesting %i                " % i)
                sys.stdout.flush()
                if tryGapNumber(numbers, i):
                    print "\rThe Frobenius number is %s" % i
                    return
                i -= 1


def tryGapNumber(numbers, num):

    # We build a list to keep track of the multipliers that we are going to
    # try with the supplied list of numbers.
    multipliers = [0] * len(numbers)

    # Initiate a loop that will try all possible combinations in the format of:
    #
    # x1*a1 + x2*a2 + ... + xn*an = combo
    #
    # where all the x are the multipliers and all the a are the numbers list.
    #
    while True:
        combo = sum(map(multiplyT, zip(numbers, multipliers)))

        if combo == num:
            # if the combo is equal to the potential gap number, then we
            # know that it is actually not valid, so we return False
            return False

        elif combo < num:
            # If the combo is less than the potential Frobenius number, then
            # we increase the last multiplier by 1.
            multipliers[-1] += 1

        else: # combo > num
            # If the result is greater than the potential Frobenius number, then
            # we reset the last non-zero multiplier, to 0, and increase the
            # previous multiplier by 1.
            i = len(numbers) - 1
            while i >= 1:
                if multipliers[i] != 0:
                    multipliers[i] = 0
                    multipliers[i-1] += 1
                    i = -1 # break out of loop
                else:
                    i -= 1

            if i == 0:
                # if i equals 0, that means the loop expired instead of being
                # broken out of. And that in turn means we could not find any
                # combination that matched the target number, hence the number
                # is a gap number and can be a Frobenius number.
                return True

def multiplyT(t):
    return t[0] * t[1]


print """
================================================================
= Frobenius number calculater
================================================================
= Auth: Daniel Viklund
= Date: 2017-05-07
= Desc: Given a Numerical Subset, this program will determine
=       the Frobenius number for that subset.
=
================================================================

"""

# REGEX pattern to parse the string input
denotation_pattern = re.compile('^<([0-9,\s]+)>$')

while True:
    num_subset = raw_input("\nEnter the denotation (<A>) for the Numerical " +
        "Subset, i.e. <2,3>. (leave blank to quit): ")

    if num_subset == "":
        sys.exit()

    else:
        res = denotation_pattern.search(num_subset)
        if res:
            printFrobeniusNumber(res.group(1))

        else:
            print "Invalid format of Subset denotation. Please try again."
