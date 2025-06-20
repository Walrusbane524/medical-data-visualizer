import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')
# 2
df['BMI'] = df['weight']/((df['height'] / 100) ** 2)
df['overweight'] = (df['BMI'] > 25.).astype(int)

df = df.drop('BMI', axis=1)

# 3
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] != 0, 'cholesterol'] = 1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] != 0, 'gluc'] = 1

# 4
def draw_cat_plot():

    fig, ax = plt.subplots(1)

    # 5
    columns = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    df_cat = df[columns][df['cardio'] == 0].melt(var_name='variable', value_name='value')

    # 6
    df_cat['cardio'] = 0

    df_cat_with_cardio = df[columns][df['cardio'] == 1].melt(var_name='variable', value_name='value')
    df_cat_with_cardio['cardio'] = 1

    df_cat = pd.concat([df_cat, df_cat_with_cardio], ignore_index=True)
    
    # 7
    g = sns.catplot(data=df_cat, x='variable', col='cardio', hue="value", kind='count')
    g.set_ylabels("total")

    # 9
    g.figure.savefig('catplot.png')
    return g.figure


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr()

    # 13
    mask = pd.DataFrame(np.triu(np.ones_like(corr, dtype=bool)))
    mask = mask.set_axis(corr.columns, axis=1)
    mask = mask.set_axis(corr.index, axis=0)

    # 14
    fig, ax = plt.subplots(1)

    # 15
    sns.heatmap(data=corr, mask=mask, ax=ax, annot=True, fmt=".1f")

    # 16
    fig.savefig('heatmap.png')
    return fig