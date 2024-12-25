import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Carregar os dados dos arquivos CSV
data_abril2018 = pd.read_csv('abril2018.csv')
data_abril2019 = pd.read_csv('abril2019.csv')

# Verificar as primeiras linhas para entender a estrutura dos dados
print(data_abril2018.head())
print(data_abril2019.head())

# Juntar os dados dos dois anos
data = pd.concat([data_abril2018, data_abril2019], ignore_index=True)

# Pre-processamento: Seleção de variáveis relevantes
# Aqui estou utilizando 'price' como a variável dependente e algumas variáveis como independentes
# Você pode ajustar conforme necessário, incluindo mais ou menos variáveis

# Convertendo 'price' para tipo numérico, removendo o símbolo de dólar e outras possíveis formatações
data['price'] = data['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Variáveis independentes (X) e dependente (y)
X = data[['accommodates', 'bathrooms', 'bedrooms', 'beds', 'square_feet', 'availability_30', 'availability_365']]  # Exemplo de variáveis independentes
y = data['price']

# Eliminar valores nulos, pois o modelo não lida bem com NaN
X = X.dropna()
y = y[X.index]  # Garantir que o target (y) tenha o mesmo número de registros após o drop

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo Random Forest
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Importância das variáveis
importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by="Importance", ascending=False)

# Gráfico de importância das variáveis
plt.figure(figsize=(10, 6))
plt.barh(importance_df["Feature"], importance_df["Importance"], color="skyblue")
plt.xlabel("Importância")
plt.ylabel("Variáveis")
plt.title("Importância das Variáveis no Modelo")
plt.gca().invert_yaxis()
plt.show()

# Gráfico de preços reais vs previstos
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color="purple")
plt.xlabel("Preço Real")
plt.ylabel("Preço Previsto")
plt.title("Preços Reais vs Previstos")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--")
plt.show()
