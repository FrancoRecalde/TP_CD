"""
Genera un CSV de muestra a partir de los archivos .dat del PAMAP2.
Recorta filas para que el archivo no supere MAX_MB megabytes.
"""

import pandas as pd
from pathlib import Path

MAX_MB = 10
DATA_PATH = Path(__file__).resolve().parent.parent / 'PAMAP2_Dataset' / 'Protocol'
OUT_PATH  = Path(__file__).resolve().parent.parent / 'data' / 'processed'

RAW_COLUMNAS = [
    'tiempo', 'actividad_id', 'frecuencia_cardiaca',
    'mano_temperatura',
    'mano_acel1_x', 'mano_acel1_y', 'mano_acel1_z',
    'mano_acel2_x', 'mano_acel2_y', 'mano_acel2_z',
    'mano_giro_x',  'mano_giro_y',  'mano_giro_z',
    'mano_magneto_x',  'mano_magneto_y',  'mano_magneto_z',
    'mano_orientacion_1', 'mano_orientacion_2', 'mano_orientacion_3', 'mano_orientacion_4',
    'pecho_temperatura',
    'pecho_acel1_x', 'pecho_acel1_y', 'pecho_acel1_z',
    'pecho_acel2_x', 'pecho_acel2_y', 'pecho_acel2_z',
    'pecho_giro_x',  'pecho_giro_y',  'pecho_giro_z',
    'pecho_magneto_x',  'pecho_magneto_y',  'pecho_magneto_z',
    'pecho_orientacion_1', 'pecho_orientacion_2', 'pecho_orientacion_3', 'pecho_orientacion_4',
    'tobillo_temperatura',
    'tobillo_acel1_x', 'tobillo_acel1_y', 'tobillo_acel1_z',
    'tobillo_acel2_x', 'tobillo_acel2_y', 'tobillo_acel2_z',
    'tobillo_giro_x',  'tobillo_giro_y',  'tobillo_giro_z',
    'tobillo_magneto_x',  'tobillo_magneto_y',  'tobillo_magneto_z',
    'tobillo_orientacion_1', 'tobillo_orientacion_2', 'tobillo_orientacion_3', 'tobillo_orientacion_4',
]


def cargar_sujeto(filepath: Path, sujeto_id: int) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep=r'\s+', header=None, names=RAW_COLUMNAS, engine='python')
    df['sujeto_id'] = sujeto_id
    return df


def main():
    OUT_PATH.mkdir(parents=True, exist_ok=True)
    out_file = OUT_PATH / 'pamap2_muestra.csv'

    print('Cargando archivos .dat...')
    dfs = []
    for sid in range(101, 110):
        filepath = DATA_PATH / f'subject{sid}.dat'
        if not filepath.exists():
            print(f'  [SKIP] {filepath.name} no encontrado')
            continue
        df = cargar_sujeto(filepath, sid)
        dfs.append(df)
        print(f'  subject{sid}: {len(df):,} filas')

    df_all = pd.concat(dfs, ignore_index=True)
    total = len(df_all)
    print(f'\nTotal unificado: {total:,} filas x {df_all.shape[1]} columnas')

    # Estimación de bytes por fila con muestra de 5000 filas
    sample_csv = df_all.head(5_000).to_csv(index=False)
    bytes_per_row = len(sample_csv.encode()) / 5_000
    max_bytes = MAX_MB * 1024 * 1024
    max_rows = int(max_bytes / bytes_per_row)

    if max_rows >= total:
        df_out = df_all
        print(f'El dataset completo cabe en {MAX_MB} MB — se exporta entero.')
    else:
        # Muestreo estratificado por sujeto_id para mantener representatividad
        frac = max_rows / total
        df_out = (
            df_all.groupby('sujeto_id', group_keys=False)
                  .apply(lambda g: g.sample(frac=frac, random_state=42), include_groups=False)
                  .reset_index(drop=True)
        )
        # La estimación puede ser imprecisa: recortar si el CSV escrito supera el límite
        df_out.to_csv(out_file, index=False)
        actual_bytes = out_file.stat().st_size
        if actual_bytes > max_bytes:
            trim_frac = max_bytes / actual_bytes
            df_out = df_out.sample(frac=trim_frac, random_state=42).reset_index(drop=True)
            print(f'Ajuste fino: recortado a {len(df_out):,} filas para cumplir el límite.')

        print(f'Recortado a {len(df_out):,} filas ({len(df_out)/total*100:.1f}%) para no superar {MAX_MB} MB.')

    df_out.to_csv(out_file, index=False)
    size_mb = out_file.stat().st_size / 1024 / 1024
    print(f'\nGuardado: {out_file}')
    print(f'Filas:    {len(df_out):,}')
    print(f'Tamaño:   {size_mb:.2f} MB')


if __name__ == '__main__':
    main()
