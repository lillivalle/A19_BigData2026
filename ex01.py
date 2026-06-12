#pip install pandas
#pip install numpy

import pandas as pd 
import numpy as np

try:
    print('Obtendo dados...')
    endereco_dados = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    #utf-8,iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(endereco_dados, sep =';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    #delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic','roubo_veiculo',]]

    # Totalizando oa roubos pelos municípios

    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)[['roubo_veiculo']].sum()

    #ordenando o dataframe
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)

    # print(df_roubo_veiculo.head(10))
    print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro ao obter dados {e}')


# obtendo Medidas
try:
    print('Calculando as medidas...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)

    print('\nMedida de Tendência Central')
    print(30*' - ')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia: {distancia} %')


except Exception as e:
    print(f'Erro ao calcular {e}')


#Obtendo medidas descritivas
    
try:
    print('Processando os quartis')

    q1 = np.quantile(array_roubo_veiculo, .25)
# não vai calcular o q2 porque mediana e q2 é a mesma coisa
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nQuartis')
    print(30*'=')
    print(f'Q1: {mediana_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Q3: {q3}')

# Municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

# Municípios com mais roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q3]

    print('\nMunicípios com menos casos de roubo')
    print(30*'=')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com mais casos de roubo')
    print(30*'=')
    #print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo')) #grande na parte de cima
    print(df_roubo_veiculo_maiores)

    # Dados escrepantes -> Outliers (se diferenciam dos demais)

except Exception as e:
    print(f'Obtendo a distribuição {e}')


#Medidas de Dispersão
try:
    # Amplitude total -> iqr (é o q3 - q1) 
    # amplitude = max - min
    # Resultado: mais próximo do mínimo, baixa dispersão.
    # Se for 0, quer dizer que todos os dados são iguais (o maior valor é igual ao menor valor).
    # Se mais próximo do maior valor, alta dispersão.
    # Mais próximo do zero > a homogeneidade
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo
    print('\nMedidas de Dispersão')
    print(30*'=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão: {e}')


# Calculando Outliers
try:
    # iqr (Intervalo Interquartil) - Amplitude dos 50% dados mais centrais.
    # iqr = q3 - q1 
    # Ele ignora os valores extremos. Max e Min estão fora do Interquartil (IQR)
    # Não sofre interferência dos valores extremos (outliers)
    # Quanto mais próximo do q1 (ou zero), mais homogêneos são os dados
    # Quanto mais próximo de q3, menos homogêneos são os dados
    iqr = q3 - q1

    # Limite inferior
    # É uma medida que vai identificar como outliers, os valores abaixo dele 
    limite_inferior = q1 - (1.5 * iqr)

    #Limite superior
    # É uma medida que vai identificar como outliers, os valores acima dele 
    limite_superior = q3 + (1.5 * iqr)
except Exception as e:
    print(f'Erro ao calcular Outliers: {e}')

