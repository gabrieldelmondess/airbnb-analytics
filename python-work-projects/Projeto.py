#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[14]:


movimentacao = pd.read_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\Movimentação Pix.xlsx')
base = pd.read_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\CADASTRO.xlsx')
dados = pd.read_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\dadosV.xlsx')

print('Colunas Movimentação Pix', movimentacao.columns)
print('Colunas na Base de Dados', base.columns)
print('Colunas dados', dados.columns)
                     


# In[20]:


base['CHAVE'] = base['CHAVE'].astype(str)
movimentacao['CHAVE'] = movimentacao['CHAVE'].astype(str)

dados = pd.merge(base, movimentacao, on='CHAVE', how = 'inner')

baseV = ['ID_PESSOA', 'CPF', 'NOME']
movimentacaoV = ['Tarifa em R$', 'Valores em R$', 'DT_DEPOSITO']

dadosV = dados [baseV + movimentacaoV]

dadosV = dadosV.assign(MES_COMP=dadosV['DT_DEPOSITO'].dt.month, ANO_COMP=dadosV['DT_DEPOSITO'].dt.year, MES_REF=dadosV['DT_DEPOSITO'].dt.month, ANO_REF=dadosV['DT_DEPOSITO'].dt.year)


dadosV.to_excel(r'C:\Users\gabriel.lima\Documents\Projetos Python\PROJETO.xlsx')


# In[ ]:




