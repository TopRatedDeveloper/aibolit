import subprocess
import pandas as pd
import os


DIR_TO_CREATE = 'target/03'
current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
print('Start metrics calculation...')
f = open("./_tmp/pmd_out.csv", "w")
subprocess.call([
    './_tmp/pmd-bin-6.22.0-SNAPSHOT/bin/run.sh', 'pmd',
    '-cache', './_tmp/cache',
    '-d', './target/01', '-R', 'ruleset.xml', '-f', 'csv'
], stdout=f)
print('Metrics have calculated.')


df = pd.read_csv('./_tmp/pmd_out.csv')
df['class'] = 0
df.loc[df['Description'].str.contains("The class"), 'class'] = 1
rows_to_remove = df[df['class'] == 1][['File', 'class', 'Rule']]\
    .groupby(['File', 'Rule']).filter(lambda x: len(x) > 1)['File']\
    .unique().tolist()

df[df.Rule == 'CyclomaticComplexity']['Description'].str\
    .extract(r'complexity of (\d+)', expand=True)
df['cyclo'] = df['Description'].str\
    .extract(r'cyclomatic complexity of (\d+)', expand=True).astype(float)
df['ncss'] = df['Description'].str\
    .extract(r'NCSS line count of (\d+)', expand=True).astype(float)
df['npath'] = df['Description']\
    .str.extract(r'NPath complexity of (\d+)', expand=True).astype(float)

class_cyclo = df[df['class'] == 1][['File', 'cyclo']].copy().dropna()\
    .reset_index().set_index('File')
avg_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy()\
    .dropna().groupby('File').mean() \
    .reset_index() \
    .set_index('File') \
    .rename({'cyclo': 'cyclo_method_avg'}, axis='columns')

min_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'cyclo': 'cyclo_method_min'}, axis='columns')
max_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'cyclo': 'cyclo_method_max'}, axis='columns')

avg_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').mean().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_avg'}, axis='columns')
min_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_min'}, axis='columns')
max_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_max'}, axis='columns')

class_ncss = df[df['class'] == 1][['File', 'ncss']].copy().dropna()\
    .groupby('File').sum().reset_index().set_index('File')


avg_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').mean().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_avg'}, axis='columns')
min_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_min'}, axis='columns')
max_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_max'}, axis='columns')

keys = pd.DataFrame(df.File.unique(), columns=['File']).set_index('File')
keys = keys.drop(rows_to_remove, axis=0)
metrics = keys.join(class_cyclo, how='inner')\
    .join(avg_method_cyclo, how='left')\
    .drop(columns=['index'])\
    .join(min_method_cyclo, how='left')\
    .join(max_method_cyclo, how='left')\
    .join(avg_method_npath, how='left')\
    .join(min_method_npath, how='left')\
    .join(max_method_npath, how='left')\
    .join(class_ncss, how='left')\
    .join(avg_method_ncss, how='left')\
    .join(min_method_ncss, how='left')\
    .join(max_method_ncss, how='left')\
    .reset_index()\
    .rename({'File': 'filename'}, axis='columns')\


if not os.path.isdir(DIR_TO_CREATE):
    os.makedirs(DIR_TO_CREATE)

metrics['filename'] = metrics.filename.str.replace(current_location + '/', '')
metrics.to_csv(DIR_TO_CREATE + '/' + 'pmd_metrics.csv', sep=';', index=False)
