a,b,c = map(int,input().split())
if a == 0:
    if b==0:
        if c==0:
            print("any")
        else:
            print("no way")
    else:
        print(-c/b)
else:
    d = b**2 - 4*a*c
    if d < 0:
        print("no way")
    elif d==0:
        print(-b/(2*a))
    else:
        x1 = (-b + d**0.5)/(2*a)
        x2 = (-b - d**0.5)/(2*a)
        print(min(x1,x2),max(x1,x2))