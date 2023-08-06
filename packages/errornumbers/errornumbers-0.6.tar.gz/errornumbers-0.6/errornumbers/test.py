from errornumbers import ErrorNumber
import math

def from_non_reproducible(lort):
    '''
    THIS USES THE n(n-1) one
    '''
    #compute an average
    average = sum(lort)/len(lort)
    sum_of_of_quad_diffs = sum([(x-average)**2 for x in lort])
    fout = math.sqrt((1/(len(lort)*(len(lort) - 1)))* sum_of_of_quad_diffs)
    return ErrorNumber(average, fout * 3)


print(from_non_reproducible([2.953, 2.955, 2.960, 2.955, 2.954]))
