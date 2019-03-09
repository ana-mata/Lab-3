#   Author: Ana Luisa Mata Sanchez
#   Course: CS2302
#   Assignment: Lab #3
#   Instructor: Olac Fuentes
#   Description: Binary search tree operations
#   T.A.: Anindita Nath
#   Last modified: 03/08/2019
#   Purpose: Display a BST as a figure, search a BST, extract a sorted list into a BST,
#   extract a BST into a sorted list and print all elements by depth.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import math 

# Code to implement a binary search tree 
# Programmed by Olac Fuentes
# Last modified February 27, 2019

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')

################################# START OF NEW CODE #################################
        
#Creates the circle
def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

#Draws the circle
def draw_circle(ax,center,radius):
    x,y = circle(center,radius)
    #Add zorder to make sure that the circle is drawn after the tree
    ax.plot(x,y, linewidth=2,color='k', zorder=1)
    #Fill in the circle with white
    ax.fill(x, y, color='w')

#Draws binary trees
def draw_bintrees(ax,p,deltay,T,circlesize):
    if T!=None:
        #Adds the text for the current item, it places it centered on the center of the arch 
        plt.text(p[1][0],p[1][1], str(T.item), horizontalalignment='center', verticalalignment='center',fontsize=25)
        
        #If there is both a right and left child, draw a full arch
        if T.right != None and T.left != None:
            plt.plot(p[:,0],p[:,1],linewidth=1,color='k', zorder=0)
        #if there is only a right child, draw a right line    
        elif T.left == None and T.right!= None:
            b = np.array([[p[2][0],p[2][1]],[p[1][0],p[1][1]],[p[2][0],p[2][1]]])
            plt.plot(b[:,0],b[:,1],linewidth=1,color='k', zorder=0)
        #if there is only a left child, draw a left line  
        elif T.right == None and T.left!= None:
            a = np.array([[p[0][0],p[0][1]],[p[1][0],p[1][1]],[p[0][0],p[0][1]]])
            plt.plot(a[:,0],a[:,1],linewidth=1,color='k', zorder=0)            
        
        #use distance to make the next arches
        distance = math.hypot((p[0][0] - p[2][0]),(p[0][1] - p[2][1]))//4
        
        #new arches
        r = np.array([[p[0][0]-distance,p[0][1]-(deltay)],[p[0][0],p[0][1]],[p[0][0]+distance,p[0][1]-(deltay)]])
        q = np.array([[p[2][0]-distance,p[2][1]-(deltay)],[p[2][0],p[2][1]],[p[2][0]+distance,p[2][1]-(deltay)]])
        
        #if there is a left child, draw the circle for that left child and call the method again
        if T.left != None:
            draw_circle(ax, r[1], circlesize)    
            draw_bintrees(ax,r,deltay,T.left,circlesize)
        
        #if there is a right child, draw the circle for that right child and call the method again
        if T.right != None:
            draw_circle(ax, q[1], circlesize)
            draw_bintrees(ax,q,deltay,T.right,circlesize)               
        
#Iterative search
def iterSearch(L,key):
    #boolean to keep track if we found the item
    isFound = False
    
    #iterate through the tree until you reach the end
    while L!=None and L.item!=None:
        #if you find the item stop and mark it as found
        if L.item == key:
            isFound = True
            #return the item that you found
            return L
            break
        #if you have not found it and it is larger than the one you are on, go left
        elif key<L.item:
            L = L.left
        #if you have not found it and it is smaller than the one you are on, go right            
        elif key>L.item:
            L = L.right
    
    #if you reached the end and did not find the item, return None
    if isFound == False:
        return None

#Building a balanced binary search tree given a sorted list as input. 
def BuildAVL(L):
    if len(L) == 0:
        return
    
    #the root will always be the middle element
    T = BST(L[len(L)//2])

    #split the list in two
    leftlist = L[:len(L)//2]
    rightlist = L[len(L)//2+1:]
    
    #Call the method again while maintining the link to the root
    T.right = BuildAVL(rightlist)
    T.left = BuildAVL(leftlist)
    
    #return the finished tree
    return T      

def TreeToList(T,L):
    if T != None:
        
        #add the left
        if T.left != None:
            TreeToList(T.left,L)
        #then add the root, that is larger than the left but smaller than the right
        L.append(T.item)
        #add the right
        if T.right != None:
            TreeToList(T.right,L)
        
        #return finished list
        return L
    else:
        #if the tree is null return an empty list
        return []

#Calculates the depth of the tree
def Depth(T):
    #a tree that is none has depth 0
    if T==None:
        return 0
    
    #keeps going either left or right and returns the largest path
    if T.left != None:
        return 1 + Depth(T.left)
    elif T.right != None:
        return 1 + Depth(T.right)
    else:
        return 0

#prints elements by depth    
def PrintByDepth(T,d):
    if T != None:
        #when it has traveled all the way until the desired depth, print
        if d == 0:
            print(T.item, " ", end="")
        
        #keep iterating thorugh depths
        PrintByDepth(T.left,d-1)
        PrintByDepth(T.right,d-1)   
            
# Code to test the functions above
T = None
A = [70, 50, 90, 130, 150, 40, 10, 30, 100, 180, 45, 60, 140, 42]
for a in A:
    T = Insert(T,a)
    
InOrder(T)
print()
InOrderD(T,'')
print()

print(SmallestL(T).item)
print(Smallest(T).item)

FindAndPrint(T,40)
FindAndPrint(T,110)

n=60
print('Delete',n,'Case 1, deleted node is a leaf')
T = Delete(T,n) #Case 1, deleted node is a leaf
InOrderD(T,'')
print('####################################')

n=90      
print('Delete',n,'Case 2, deleted node has one child')      
T = Delete(T,n) #Case 2, deleted node has one child
InOrderD(T,'')
print('####################################')

n=70      
print('Delete',n,'Case 3, deleted node has two children') 
T = Delete(T,n) #Case 3, deleted node has two children
InOrderD(T,'')

n=40      
print('Delete',n,'Case 3, deleted node has two children') 
T = Delete(T,n) #Case 3, deleted node has two children
InOrderD(T,'')

################################# START OF NEW METHOD CALLS #################################
print('############### Tree Figure ###############')
plt.close("all") 
orig_size = 1000
p = np.array([[-orig_size,-orig_size],[0,0],[orig_size,-orig_size]])
fig, ax = plt.subplots()
fig.set_size_inches(18, 18.6)
#draws the tree
draw_bintrees(ax,p,orig_size,T,orig_size//6)
#draws the circle for the root
draw_circle(ax, [0,0], orig_size//6)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('BinTree.png')
print()

print('############### Search for an item ###############')
searchee = iterSearch(T,10)
if searchee != None:
    print(searchee.item, "was found!")
else:
    print("Item not found")

print()
print('###############Build Balance Tree###############')
L = [1,2,3,4,5,6,7]
AVLTree = BuildAVL(L)
InOrderD(AVLTree," ")

print()
print('###############Tree to List###############')
L = []      
TreeInList = []      
TreeInList = TreeToList(T,L)
print(TreeInList)

print()
print('###############Depth of Tree###############')
#get the depth of the tree
d = Depth(T)
#print elements by depth using a loop
for i in range(d+1):
    print("Keys at depth ", i ,": ", sep = '', end="")
    PrintByDepth(T,i)
    print()
