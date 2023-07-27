#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd


# In[22]:


base = pd.read_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\VERIFICACOES SEM EMAIS - SEM DATA\base 25-07-2023.xlsx')
sdata = pd.read_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\VERIFICACOES SEM EMAIS - SEM DATA\PARTICIPANTES SEM DATA DE NASCIMENTO (2).xlsx')


# In[30]:


base.loc[:, 'CPF'] = base['CPF'].astype(str)
base.loc[:, 'CPF'] = base['CPF'].str.strip()
sdata.loc[:, 'CPF'] = sdata['CPF'].astype(str)
sdata.loc[:, 'CPF'] = sdata['CPF'].str.strip()

base = base.drop_duplicates(subset='CPF')
base.loc[:, 'CPF'] = base['CPF'].str.zfill(11)
sdata['CPF'] = sdata['CPF'].str.zfill(11)

verific_sdata = pd.merge(sdata, base, on='CPF', how='inner')

verific_base_data = verific_sdata[['CPF', 'NOME', 'SG_EMPRESA', 'DT_NASCIMENTO', 'NM_EMAIL']]

verific_base_data.to_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\VERIFICACOES SEM EMAIS - SEM DATA\PARTICIPANTES SEM DATA DE NASCIMENTO - Verific.xlsx')


# In[ ]:





# In[ ]:




