with open('words.txt', 'r') as f:
    lines = f.readlines()
    f.close()
    
with open('words1.txt', 'w') as f:
    for i in lines:
        if len(i) >= 7:
            f.write(i)
    f.close()