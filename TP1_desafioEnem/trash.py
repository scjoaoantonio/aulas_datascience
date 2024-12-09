# IMPORTAÇÕES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CARREGAR E INSPECIONAR O CONJUNTO DE DADOS
# Carregar os dados
data = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';')

# Inspecionar as primeiras linhas do dataframe
print(data.head())

# Inspecionar as colunas do dataframe
print(data.columns)

# IDENTIFICAR COLUNAS RELEVANTES E TRATAMENTO DE VALORES AUSENTES E INCONSISTENTES
# Colunas relevantes
relevant_columns = [
    'TP_SEXO', 'SG_UF_PROVA', 'TP_ESCOLA', 
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'
]

# Selecionar apenas as colunas relevantes
data = data[relevant_columns]

# Verificar valores ausentes
print(data.isnull().sum())

# TRATAMENTO DE VALORES AUSENTES
# Remover linhas com valores ausentes
data = data.dropna()

# Verificar novamente valores ausentes
print(data.isnull().sum())

# CRIAR NOVAS COLUNAS CATEGÓRICAS PARA AGRUPAR OS DADOS
# Dicionário de regiões
regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# Função para mapear estados para regiões
def get_regiao(estado):
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return 'Desconhecida'

# Aplicar a função para criar a coluna 'Regiao'
data['Regiao'] = data['SG_UF_PROVA'].apply(get_regiao)

# Verificar os dados
print(data.head())

# AGRUPAR POR GÊNERO E TIPO DE ESCOLA
# Mapear códigos para descrições de tipos de escola
tipo_escola = {
    1: '1',
    2: '2',
    3: '3'
}

# Aplicar o mapeamento
data['Tipo_Escola'] = data['TP_ESCOLA'].map(tipo_escola)

# Verificar os dados
print(data.head())

# CALCULAR A MÉDIA DAS NOTAS
# Calcular a média das notas
data['Media_Notas'] = data[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)

# Verificar os dados
print(data.head())

# MEDIDAS DE TENDÊNCIA CENTRAL E DISPERSÃO
# Selecionar colunas de notas
notas_columns = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']

# Calcular medidas de tendência central e dispersão
descriptive_stats = data[notas_columns].describe().T
descriptive_stats['median'] = data[notas_columns].median()
descriptive_stats['std'] = data[notas_columns].std()
descriptive_stats['q1'] = data[notas_columns].quantile(0.25)
descriptive_stats['q3'] = data[notas_columns].quantile(0.75)

# Exibir estatísticas descritivas
print(descriptive_stats)

# ANÁLISE POR GÊNERO
# Inicializar um dicionário para armazenar as estatísticas descritivas
gender_stats = {}

# Calcular as estatísticas para cada gênero
for gender, group in data.groupby('TP_SEXO'):
    stats = group[notas_columns].describe().T
    stats['median'] = group[notas_columns].median()
    stats['std'] = group[notas_columns].std()
    stats['q1'] = group[notas_columns].quantile(0.25)
    stats['q3'] = group[notas_columns].quantile(0.75)
    gender_stats[gender] = stats

# Exibir estatísticas descritivas por gênero
for gender, stats in gender_stats.items():
    print(f'Estatísticas para o gênero {gender}:')
    print(stats)
    print('\n')


# ANÁLISE POR REGIÃO
# Inicializar um dicionário para armazenar as estatísticas descritivas
region_stats = {}

# Calcular as estatísticas para cada região
for region, group in data.groupby('Regiao'):
    stats = group[notas_columns].describe().T
    stats['median'] = group[notas_columns].median()
    stats['std'] = group[notas_columns].std()
    stats['q1'] = group[notas_columns].quantile(0.25)
    stats['q3'] = group[notas_columns].quantile(0.75)
    region_stats[region] = stats

# Exibir estatísticas descritivas por região
for region, stats in region_stats.items():
    print(f'Estatísticas para a região {region}:')
    print(stats)
    print('\n')

# ANÁLISE POR TIPO DE ESCOLA
# Inicializar um dicionário para armazenar as estatísticas descritivas
school_type_stats = {}

# Calcular as estatísticas para cada tipo de escola
for school_type, group in data.groupby('Tipo_Escola'):
    stats = group[notas_columns].describe().T
    stats['median'] = group[notas_columns].median()
    stats['std'] = group[notas_columns].std()
    stats['q1'] = group[notas_columns].quantile(0.25)
    stats['q3'] = group[notas_columns].quantile(0.75)
    school_type_stats[school_type] = stats

# Exibir estatísticas descritivas por tipo de escola
for school_type, stats in school_type_stats.items():
    print(f'Estatísticas para o tipo de escola {school_type}:')
    print(stats)
    print('\n')

# GRÁFICO DE DISTRIBUIÇÃO DAS NOTAS POR REGIÃO
# Definir o estilo do seaborn
sns.set(style="whitegrid")

# Dicionário de mapeamento para os nomes das notas
notas_renomeadas = {
    'NU_NOTA_CN': 'Ciências da Natureza',
    'NU_NOTA_CH': 'Ciências Humanas',
    'NU_NOTA_LC': 'Linguagens',
    'NU_NOTA_MT': 'Matemática',
    'NU_NOTA_REDACAO': 'Redação'
}

# Gráficos de distribuição das notas por região
for nota, nome_amigavel in notas_renomeadas.items():
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Regiao', y=nota, data=data)
    plt.title(f'Distribuição das notas de {nome_amigavel} por região')
    plt.xlabel('Região')
    plt.ylabel('Nota')
    plt.show()

# GRÁFICO DE DISTRIBUIÇÃO DAS NOTAS POR GÊNERO
# Gráficos de distribuição das notas por gênero
for nota, nome_amigavel in notas_renomeadas.items():
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='TP_SEXO', y=nota, data=data)
    plt.title(f'Distribuição das notas de {nome_amigavel} por gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Nota')
    plt.show()

# GRÁFICO DE DISTRIBUIÇÃO DAS NOTAS POR TIPO DE ESCOLA
# Gráficos de distribuição das notas por tipo de escola
for nota, nome_amigavel in notas_renomeadas.items():
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Tipo_Escola', y=nota, data=data)
    plt.title(f'Distribuição das notas de {nome_amigavel} por tipo de escola')
    plt.xlabel('Tipo de Escola')
    plt.ylabel('Nota')
    plt.show()

# COMPARAÇÃO DAS MÉDIAS DE NOTAS POR REGIÃO E GÊNERO
# Calcular médias das notas por região e gênero
mean_scores_region_gender = data.groupby(['Regiao', 'TP_SEXO'])[notas_columns].mean().reset_index()

# Gráficos de comparação das médias por região e gênero
for nota, nome_amigavel in notas_renomeadas.items():
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Regiao', y=nota, hue='TP_SEXO', data=mean_scores_region_gender)
    plt.title(f'Comparação das médias de {nome_amigavel} por região e gênero')
    plt.xlabel('Região')
    plt.ylabel('Média da Nota')
    plt.legend(title='Gênero')
    plt.show()

# COMPARAÇÃO DAS MÉDIAS DE NOTAS POR TIPO DE ESCOLA E GÊNERO
# Calcular médias das notas por tipo de escola e gênero
mean_scores_school_gender = data.groupby(['Tipo_Escola', 'TP_SEXO'])[notas_columns].mean().reset_index()

# Gráficos de comparação das médias por tipo de escola e gênero
for nota, nome_amigavel in notas_renomeadas.items():
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Tipo_Escola', y=nota, hue='TP_SEXO', data=mean_scores_school_gender)
    plt.title(f'Comparação das médias de {nome_amigavel} por tipo de escola e gênero')
    plt.xlabel('Tipo de Escola')
    plt.ylabel('Média da Nota')
    plt.legend(title='Gênero')
    plt.show()

# CALCULAR A CORRELAÇÃO ENTRE AS NOTAS DAS DISCIPLINAS
correlation_matrix = data[notas_columns].corr()

print(correlation_matrix)

# VISUALIZAR A MATRIZ DE CORRELAÇÃO COM UM HEATMAP
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matriz de Correlação entre as Notas')
plt.show()

# ANÁLISE DE DESSE DESSEMPENHO POR REGIÃO E TIPO DE ESCOLA

# Médias das notas por região
mean_scores_region = data.groupby('Regiao')[notas_columns].mean().reset_index()

# Exibir médias das notas por região
print("Médias das notas por região:")
print(mean_scores_region)

# Comparação das médias das notas por tipo de escola e região
plt.figure(figsize=(12, 6))
sns.barplot(x='Regiao', y='NU_NOTA_MT', data=mean_scores_region)
plt.title('Comparação das Médias de Matemática por Região')
plt.xlabel('Região')
plt.ylabel('Média de Matemática')
plt.show()

# ANÁLISE DE DESSE DESSEMPENHO POR GÊNERO
# Médias das notas por gênero
mean_scores_gender = data.groupby('TP_SEXO')[notas_columns].mean().reset_index()

# Exibir médias das notas por gênero
print("Médias das notas por gênero:")
print(mean_scores_gender)

# Comparação das médias das notas por gênero e tipo de escola
plt.figure(figsize=(12, 6))
sns.barplot(x='TP_SEXO', y='NU_NOTA_MT', data=mean_scores_gender)
plt.title('Comparação das Médias de Matemática por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Média de Matemática')
plt.show()

# ANÁLISE DE DESSE DESSEMPENHO POR TIPO DE ESCOLA
# Médias das notas por tipo de escola
mean_scores_school = data.groupby('Tipo_Escola')[notas_columns].mean().reset_index()

# Exibir médias das notas por tipo de escola
print("Médias das notas por tipo de escola:")
print(mean_scores_school)

# Comparação das médias das notas por tipo de escola
plt.figure(figsize=(12, 6))
sns.barplot(x='Tipo_Escola', y='NU_NOTA_MT', data=mean_scores_school)
plt.title('Comparação das Médias de Matemática por Tipo de Escola')
plt.xlabel('Tipo de Escola')
plt.ylabel('Média de Matemática')
plt.show()

'''
   NU_INSCRICAO  NU_ANO  TP_FAIXA_ETARIA TP_SEXO  TP_ESTADO_CIVIL  \
0  210059085136    2023               14       M                2   
1  210059527735    2023               12       M                2   
2  210061103945    2023                6       F                1   
3  210060214087    2023                2       F                1   
4  210059980948    2023                3       F                1   

   TP_COR_RACA  TP_NACIONALIDADE  TP_ST_CONCLUSAO  TP_ANO_CONCLUIU  TP_ESCOLA  \
0            1                 1                1               17          1   
1            1                 0                1               16          1   
2            1                 1                1                0          1   
3            3                 1                2                0          2   
4            3                 1                2                0          2   

   ...  Q016  Q017  Q018 Q019  Q020 Q021  Q022  Q023  Q024  Q025  
0  ...     C     C     B    B     A    B     B     A     A     B  
1  ...     B     A     B    B     A    A     C     A     D     B  
2  ...     B     A     A    B     A    A     A     A     A     B  
3  ...     A     A     A    B     A    A     D     A     A     B  
4  ...     A     A     A    B     A    A     B     A     A     A  

[5 rows x 76 columns]
Index(['NU_INSCRICAO', 'NU_ANO', 'TP_FAIXA_ETARIA', 'TP_SEXO',
       'TP_ESTADO_CIVIL', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO',
       'TP_ANO_CONCLUIU', 'TP_ESCOLA', 'TP_ENSINO', 'IN_TREINEIRO',
...
       'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013',
       'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022',
       'Q023', 'Q024', 'Q025'],
      dtype='object')
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

TP_SEXO                 0
SG_UF_PROVA             0
TP_ESCOLA               0
NU_NOTA_CN         128608
NU_NOTA_CH         113231
NU_NOTA_LC         113231
NU_NOTA_MT         128608
NU_NOTA_REDACAO    113231
dtype: int64

TP_SEXO            0
SG_UF_PROVA        0
TP_ESCOLA          0
NU_NOTA_CN         0
NU_NOTA_CH         0
NU_NOTA_LC         0
NU_NOTA_MT         0
NU_NOTA_REDACAO    0
dtype: int64

   TP_SEXO SG_UF_PROVA  TP_ESCOLA  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  \
2        F          RS          1       502.0       498.9       475.6   
3        F          CE          2       459.0       508.5       507.2   
4        F          CE          2       402.5       379.2       446.9   
9        M          SP          1       564.7       630.3       610.4   
10       M          RN          1       644.9       620.2       626.9   

    NU_NOTA_MT  NU_NOTA_REDACAO    Regiao  
2        363.2            700.0       Sul  
3        466.7            880.0  Nordeste  
4        338.3            560.0  Nordeste  
9        680.2            600.0   Sudeste  
10       736.3            860.0  Nordeste  

   TP_SEXO SG_UF_PROVA  TP_ESCOLA  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  \
2        F          RS          1       502.0       498.9       475.6   
3        F          CE          2       459.0       508.5       507.2   
4        F          CE          2       402.5       379.2       446.9   
9        M          SP          1       564.7       630.3       610.4   
10       M          RN          1       644.9       620.2       626.9   

    NU_NOTA_MT  NU_NOTA_REDACAO    Regiao Tipo_Escola  
2        363.2            700.0       Sul           1  
3        466.7            880.0  Nordeste           2  
4        338.3            560.0  Nordeste           2  
9        680.2            600.0   Sudeste           1  
10       736.3            860.0  Nordeste           1  


   TP_SEXO SG_UF_PROVA  TP_ESCOLA  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  \
2        F          RS          1       502.0       498.9       475.6   
3        F          CE          2       459.0       508.5       507.2   
4        F          CE          2       402.5       379.2       446.9   
9        M          SP          1       564.7       630.3       610.4   
10       M          RN          1       644.9       620.2       626.9   

    NU_NOTA_MT  NU_NOTA_REDACAO    Regiao Tipo_Escola  Media_Notas  
2        363.2            700.0       Sul           1       507.94  
3        466.7            880.0  Nordeste           2       564.28  
4        338.3            560.0  Nordeste           2       425.38  
9        680.2            600.0   Sudeste           1       617.12  
10       736.3            860.0  Nordeste           1       697.66  


                    count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       370140.0  490.846568   84.807851  0.0  436.8  486.6  543.2   
NU_NOTA_CH       370140.0  525.811576   84.354966  0.0  472.3  531.1  584.0   
NU_NOTA_LC       370140.0  519.420604   72.429356  0.0  473.8  523.0  569.2   
NU_NOTA_MT       370140.0  524.188339  127.038761  0.0  425.9  510.1  614.1   
NU_NOTA_REDACAO  370140.0  647.492678  205.564103  0.0  520.0  640.0  820.0   

                    max  median     q1     q3  
NU_NOTA_CN        868.4   486.6  436.8  543.2  
NU_NOTA_CH        823.0   531.1  472.3  584.0  
NU_NOTA_LC        777.3   523.0  473.8  569.2  
NU_NOTA_MT        958.6   510.1  425.9  614.1  
NU_NOTA_REDACAO  1000.0   640.0  520.0  820.0  

Estatísticas para o gênero F:
                    count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       256157.0  484.814721   81.436690  0.0  433.2  479.5  534.3   
NU_NOTA_CH       256157.0  523.406654   82.090878  0.0  471.2  527.8  579.7   
NU_NOTA_LC       256157.0  519.102557   70.745106  0.0  474.1  522.0  567.5   
NU_NOTA_MT       256157.0  512.457955  121.929027  0.0  419.1  496.9  595.9   
NU_NOTA_REDACAO  256157.0  659.581585  201.606072  0.0  540.0  660.0  820.0   

                    max  median     q1     q3  
NU_NOTA_CN        868.4   479.5  433.2  534.3  
NU_NOTA_CH        823.0   527.8  471.2  579.7  
NU_NOTA_LC        777.3   522.0  474.1  567.5  
NU_NOTA_MT        958.6   496.9  419.1  595.9  
NU_NOTA_REDACAO  1000.0   660.0  540.0  820.0  


Estatísticas para o gênero M:
                    count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       113983.0  504.402096   90.478763  0.0  447.5  504.8  560.5   
NU_NOTA_CH       113983.0  531.216221   88.997299  0.0  475.1  538.6  593.6   
NU_NOTA_LC       113983.0  520.135359   76.073950  0.0  472.8  525.4  573.0   
NU_NOTA_MT       113983.0  550.550342  134.140816  0.0  445.4  544.7  649.6   
NU_NOTA_REDACAO  113983.0  620.324961  211.689018  0.0  520.0  620.0  780.0   

                    max  median     q1     q3  
...
NU_NOTA_MT        958.6   544.7  445.4  649.6  
NU_NOTA_REDACAO  1000.0   620.0  520.0  780.0  


Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

Estatísticas para a região Centro-Oeste:
                   count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       28415.0  494.063920   87.722224  0.0  440.5  490.6  546.9   
NU_NOTA_CH       28415.0  528.066644   83.227503  0.0  476.3  532.8  584.8   
NU_NOTA_LC       28415.0  521.629034   70.735648  0.0  477.8  524.3  569.3   
NU_NOTA_MT       28415.0  524.974869  128.968413  0.0  426.4  512.0  615.0   
NU_NOTA_REDACAO  28415.0  645.566074  201.734269  0.0  520.0  640.0  800.0   

                    max  median     q1     q3  
NU_NOTA_CN        833.7   490.6  440.5  546.9  
NU_NOTA_CH        823.0   532.8  476.3  584.8  
NU_NOTA_LC        749.2   524.3  477.8  569.3  
NU_NOTA_MT        958.6   512.0  426.4  615.0  
NU_NOTA_REDACAO  1000.0   640.0  520.0  800.0  


Estatísticas para a região Nordeste:
                    count        mean         std  min      25%    50%    75%  \
NU_NOTA_CN       150592.0  479.897353   81.978812  0.0  426.900  474.1  529.8   
NU_NOTA_CH       150592.0  512.119191   85.658496  0.0  455.175  515.6  571.4   
NU_NOTA_LC       150592.0  506.966913   73.837859  0.0  459.600  509.2  557.1   
NU_NOTA_MT       150592.0  506.844017  122.966555  0.0  411.700  487.6  589.2   
NU_NOTA_REDACAO  150592.0  638.265778  216.215165  0.0  520.000  640.0  820.0   

                    max  median       q1     q3  
...
NU_NOTA_MT        958.6   546.4  458.0  640.1  
NU_NOTA_REDACAO  1000.0   640.0  540.0  800.0  


Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

Estatísticas para o tipo de escola 1:
                    count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       201053.0  496.102463   88.670706  0.0  439.5  491.2  550.0   
NU_NOTA_CH       201053.0  530.682547   86.776501  0.0  475.1  535.9  591.0   
NU_NOTA_LC       201053.0  522.485823   74.154143  0.0  475.1  525.6  573.8   
NU_NOTA_MT       201053.0  525.643583  131.139152  0.0  424.0  509.8  618.9   
NU_NOTA_REDACAO  201053.0  644.011082  205.291825  0.0  520.0  640.0  820.0   

                    max  median     q1     q3  
NU_NOTA_CN        868.4   491.2  439.5  550.0  
NU_NOTA_CH        823.0   535.9  475.1  591.0  
NU_NOTA_LC        773.5   525.6  475.1  573.8  
NU_NOTA_MT        958.6   509.8  424.0  618.9  
NU_NOTA_REDACAO  1000.0   640.0  520.0  820.0  


Estatísticas para o tipo de escola 2:
                    count        mean         std  min    25%    50%    75%  \
NU_NOTA_CN       147648.0  474.840547   74.165095  0.0  428.5  473.6  523.6   
NU_NOTA_CH       147648.0  510.765330   77.944481  0.0  461.8  517.2  565.4   
NU_NOTA_LC       147648.0  508.180577   67.736863  0.0  466.5  513.1  555.1   
NU_NOTA_MT       147648.0  505.947656  112.757512  0.0  419.9  495.1  585.2   
NU_NOTA_REDACAO  147648.0  631.010241  204.882563  0.0  520.0  640.0  780.0   

                    max  median     q1     q3  
...
NU_NOTA_MT        958.6   651.0  555.25  722.4  
NU_NOTA_REDACAO  1000.0   840.0  700.00  900.0  


Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...



'''