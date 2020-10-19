def cal(name1,name2):
    combStr = name1 + "loves" + name2
    strCount = ""
    for c1 in combStr:
        if combStr.count(c1) != 0:
            strCount+=str(combStr.count(c1))
            combStr = combStr.replace(c1,"")

    n= list(map(int,strCount))
    
    while len(n)>2:
        n = shortn(n)
    per = int(''.join(map(str,n)))
    return per




def shortn(n):
    i=0
    i=0
    j=len(n)-1
    n1=[]
    while i<=j :
        per = n[i]+n[j]
        if i==j:
            per = n[i]
        n1.append(per)
        i+=1
        j-=1
    return n1


if __name__ == "__main__":
    
    n1=input("Enter your name: ").lower()
    n2=input("Enter your Partner/Crush name: ").lower()
    
    print(f" \n{n1.upper()} and {n2.upper()}")
    
    
    print(f""" 
             love meter:
                _____     ______
               (     \   /      )
                \     \ /      /
                 \            / 
                  \  {cal(n1,n2)}%    /
                   \        /
                    \      /
                     \    /
                      \  /
                       \/                  """ )
