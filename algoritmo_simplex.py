arquivo =  open("funcao.txt", "r")

linhas = arquivo.readlines()  

if linhas[0].strip().lower().startswith("max"):
    of = True
else:
    of = False

linhas[0] = linhas[0].strip()[7:].strip()
coef = ""
num=0
funcao1 = []

for i, elemento in enumerate(linhas[0]): 
    if elemento == 'x':
        if coef == '' or coef == '+':
            coef = '1'
        elif coef == '-':
            coef = '-1'
        
        funcao1.append(int(coef))
        coef = ""

    if (elemento.isdigit() and (i+1 < len(linhas[0]) and linhas[0][i+1] == 'x')) or elemento in ['+', '-']: 
        coef += elemento 
    
        
if coef != '':
    funcao1.append(int(coef))

print(funcao1)

arquivo.close()