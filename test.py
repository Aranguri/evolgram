def main():
    x, y, z = (1, 4, 9)
    #l = {'x': x, 'y': y, 'z':z}
    exec('z = x + y', {}, l)
    print(l)
    #exec('print(x, y)')
    #print (b)

main()
