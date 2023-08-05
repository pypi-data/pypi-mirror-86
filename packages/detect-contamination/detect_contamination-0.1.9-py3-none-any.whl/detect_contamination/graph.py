from matplotlib import pyplot as plt 
import numpy as np 
  
def draw(result, output):
    name=[]
    data=[]
    other=1
    for taxo in result:
        name.append(taxo)
        data.append(result[taxo])
        other -= result[taxo]
    if other != 0:
        name.append("others")
        data.append(other)
  
    fig1, ax1 = plt.subplots()
    ax1.pie(data , labels=name, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  

    plt.savefig(output)
    plt.show()
