"""Implement quick sort in Python.
Input a list.
Output a sorted list."""
def quicksort(array):
    quickSortHelper(array,0,len(array)-1)
    print array
    
def quickSortHelper(array,f,l):
    if f<l:
        splitpt=partition(array,f,l)  #return rmk, a new sorted position (don't move)
        quickSortHelper(array,f,splitpt-1)
        quickSortHelper(array,splitpt+1,l)

def partition(array,f,l): #first,last
    pivot=array[f]
    lmk=f+1  #leftmark
    rmk=l    #rightmark
    OKOK=False
    while not OKOK:  #unsorted partition
        while lmk<=rmk and array[lmk]<=pivot:
            lmk=lmk+1
        while array[rmk]>=pivot and rmk>=lmk:
            rmk=rmk-1
        if rmk<lmk:
            OKOK=True
        else: #swap(array[rmk], array[lmk])
            tmp=array[rmk]
            array[rmk]=array[lmk]
            array[lmk]=tmp
    #swap(array[f], array[rmk])    
    tmp=array[f]
    array[f]=array[rmk]
    array[rmk]=tmp
    return rmk    


test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
#test=[3,44,38,5,47,15,36,26,27,2,46,4,19,50,48]
print quicksort(test)
