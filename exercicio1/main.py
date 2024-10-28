import pandas as pd

# Carregar o dataset
titanic_df = pd.read_csv('titanic.csv')

print("\n\n\n\t\t######## TITANIC ########\n\n\n")
print('\nAgrupar dados por Classe e Gênero e calcular estatísticas descritivas para a idade\n')
age_distribution = titanic_df.groupby(['Pclass', 'Sex'])['Age'].describe()
print(age_distribution)

# Criando faixas etárias
titanic_df['AgeGroup'] = pd.cut(titanic_df['Age'], bins=[0, 12, 18, 35, 50, 80], 
                                labels=['Criança', 'Adolescente', 'Jovem Adulto', 'Adulto', 'Idoso'])

# Calculando a taxa de sobrevivência por faixa etária, definindo o parâmetro `observed`
survival_rate_age_group = titanic_df.groupby('AgeGroup', observed=False)['Survived'].mean()
print(survival_rate_age_group)

# Estatísticas descritivas de tarifa para cada grupo de sobrevivência
fare_survival_relation = titanic_df.groupby('Survived')['Fare'].describe()
print(fare_survival_relation)
