a=[[" "," "," "],[" "," "," "],[" "," "," "]]
def output():
    for i in range(0,20):
        print()
    print(" "+a[0][0]+" | "+a[0][1]+" | "+a[0][2])
    print("-----------")
    print(" "+a[1][0]+" | "+a[1][1]+" | "+a[1][2])
    print("-----------")
    print(" "+a[2][0]+" | "+a[2][1]+" | "+a[2][2])
def check():
    if(a[0][1]==a[0][0] and a[0][0]==a[0][2] and a[0][0]!=" "):
        return True
    elif(a[1][1]==a[1][0] and a[1][0]==a[1][2] and a[1][0]!=" "):
        return True
    elif(a[2][1]==a[2][0] and a[2][0]==a[2][2] and a[2][0]!=" "):
        return True
    elif(a[1][0]==a[0][0] and a[0][0]==a[2][0] and a[0][0]!=" "):
        return True
    elif(a[1][1]==a[0][1] and a[0][1]==a[2][1] and a[0][1]!=" "):
        return True
    elif(a[1][2]==a[0][2] and a[0][2]==a[2][2] and a[0][2]!=" "):
        return True
    elif(a[1][1]==a[0][0] and a[0][0]==a[2][2] and a[0][0]!=" "):
        return True
    elif(a[1][1]==a[0][2] and a[0][2]==a[2][0] and a[0][2]!=" "):
        return True
    else:
        return False
def empty():
    for e in a:
        for i in e:
            if(i==" "):
                return True
    print("It is a draw")
    return False
x=True
while(empty()):
    output()
    n=int(input("Player "+str(int((not x))+1)+"'s turn: "))-1
    if(n<0 or n>8):
        print("Game ended due to invalid move")
        break
    if(x):
        a[n//3][n%3]="X"
    else:
        a[n//3][n%3]="0"
    if(check()):
        output()
        print("Player "+str(int((not x))+1)+" wins.")
        break
    x=not x