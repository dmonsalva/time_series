import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# 1. Importar los datos y establecer el índice en 'date'
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# 2. Filtrar datos para eliminar el 2.5% superior e inferior
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

# 3. Función para dibujar el gráfico de líneas
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["value"], color="red", linewidth=1)

    # Configurar título y etiquetas
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Guardar y mostrar el gráfico
    fig.savefig("line_plot.png")
    plt.show()
    return fig

# 4. Función para dibujar el gráfico de barras
def draw_bar_plot():
    # Crear DataFrame con promedios mensuales agrupados por año
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Crear el gráfico de barras
    fig = df_bar.plot(kind="bar", figsize=(12, 6), legend=True).figure

    # Configurar etiquetas y leyenda
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # Guardar y mostrar el gráfico
    fig.savefig("bar_plot.png")
    plt.show()
    return fig

# 5. Función para dibujar los diagramas de caja
def draw_box_plot():
    # Crear DataFrame para los gráficos de caja
    df_box = df.copy()
    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.strftime("%b")  # Nombres abreviados de meses

    # Crear la figura y los subgráficos
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Gráfico de caja por año
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Gráfico de caja por mes
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], order=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Guardar y mostrar el gráfico
    fig.savefig("box_plot.png")
    plt.show()
    return fig

# 6. Ejecutar funciones para verificar la salida
if __name__ == "__main__":
    print("Generando gráfico de líneas...")
    draw_line_plot()

    print("Generando gráfico de barras...")
    draw_bar_plot()

    print("Generando diagramas de caja...")
    draw_box_plot()
    