#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
from datetime import datetime
acompanhamento = pd.read_excel(r'W:\DISEG\GEARC\_RESTRITO\RELATÓRIO GERENCIAL\Acompanhamento - FICHAS.xlsx')
data_atual = datetime.now().date()
acompanhamento ['Data de finalização'] = pd.to_datetime(acompanhamento['Data de finalização'])

hoje = pd.to_datetime(data_atual)

fichas = acompanhamento[acompanhamento['Data de finalização'].dt.date == hoje.date()]

contagem = fichas['Tipo'].value_counts()
total = contagem.sum()
print(contagem)
print('-------------------------------------------------------' )
print('TOTAL: ', total)



# In[7]:


print(data_atual)


# In[ ]:




