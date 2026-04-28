# Contexto del Proyecto — TPI Ciencia de Datos UTN FRC 2026
## Para Claude Code: leé esto completo antes de hacer cualquier cosa

---

## 1. Quién soy y qué estoy haciendo

Soy estudiante de Ingeniería en Sistemas de Información en UTN FRC (Córdoba, Argentina), cursando
Ciencia de Datos en 5K4, año 2026. Estoy haciendo el **Trabajo Práctico Integrador (TPI)** en grupo,
pero en la práctica voy a llevar el desarrollo técnico yo solo. El grupo tiene 8 integrantes (Grupo 15).

**Mi nombre:** Franco Recalde (legajo 94661). Soy el Product Owner del equipo Scrum.

---

## 2. El dataset elegido: PAMAP2

**Nombre completo:** PAMAP2 Physical Activity Monitoring Dataset  
**Fuente:** UCI Machine Learning Repository  
**URL oficial:** https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring  
**Autores originales:** A. Reiss y D. Stricker (DFKI, Alemania)  
**Licencia:** CC BY 4.0

### Descripción técnica del dataset
- **Sujetos:** 9 participantes (subject101.dat a subject109.dat)
- **Formato original:** archivos .dat separados por sujeto, sin header, valores separados por espacio
- **Frecuencia de muestreo IMU:** 100 Hz
- **Frecuencia de muestreo heart rate:** ~9 Hz (genera NaNs estructurales intercalados)
- **Columnas por archivo:** 54 columnas exactas (sin nombres de columna en el archivo)
- **Filas estimadas raw (100Hz, todos los sujetos):** >3.850.000
- **Filas tras downsampling a 10Hz:** ~194.000

### Estructura de columnas (54 en total, sin header)
```
Col 0:  timestamp (segundos)
Col 1:  activityID (entero, ver catálogo abajo)
Col 2:  heart_rate (bpm) — muestrea a ~9Hz, genera NaN frecuentes
Cols 3-19:  IMU hand (mano dominante) — 17 columnas
Cols 20-36: IMU chest (pecho)          — 17 columnas
Cols 37-53: IMU ankle (tobillo)        — 17 columnas
```

### Estructura de cada IMU (17 columnas repetidas × 3):
```
[imu]_temperature           (°C)
[imu]_acc1_x/y/z            (ms⁻², escala ±16g, 13-bit)
[imu]_acc2_x/y/z            (ms⁻², escala ±6g, 13-bit)
[imu]_gyro_x/y/z            (rad/s)
[imu]_mag_x/y/z             (μT)
[imu]_orient_1/2/3/4        ← INVÁLIDOS según documentación oficial, deben dropearse
```

### Catálogo de activityID
```
0  = other (transitorio entre actividades) ← EXCLUIR del dataset de trabajo
1  = lying
2  = sitting
3  = standing
4  = walking
5  = running
6  = cycling
7  = Nordic walking
9  = watching TV
10 = computer work
11 = car driving
12 = ascending stairs
13 = descending stairs
16 = vacuum cleaning
17 = ironing
18 = folding laundry
19 = house cleaning
20 = playing soccer
24 = rope jumping
```
Actividades del protocolo estándar (todos los sujetos): 1–7, 12–13  
Actividades opcionales: 9, 10, 11, 16–20, 24 (no las realizaron todos)

---

## 3. Lo que ya está decidido / hecho (Entrega 1)

- Dataset seleccionado: PAMAP2 ✓
- Plan de proyecto Scrum definido ✓
- Entrega 1 presentada y aprobada ✓
- Decisión de downsampling: 100Hz → 10Hz (cada 10 filas) ✓
- Variable target elegida: `activityID` (clasificación multiclase) ✓

---

## 4. Qué hay que hacer ahora: Entrega 2

**Fecha límite:** 06/05/2026 (Grupo A)

### Objetivos de la entrega (según enunciado del profesor)
1. Definir al menos 3 hipótesis/requerimientos para el análisis
2. Proceso ETL completo:
   - Análisis exploratorio visual y estadístico
   - Identificación y tratamiento de valores faltantes, erróneos, inconsistentes
   - Estrategia documentada para cada caso
   - Preparación del dataset objetivo final
3. Análisis de variables: relaciones, visualizaciones de patrones
4. Informe en formato paper científico (complementa Entrega 1)

### Las 3 hipótesis definidas para el proyecto
```
H1: Es posible clasificar con alta precisión el tipo de actividad física realizada
    a partir de las señales inerciales y de frecuencia cardíaca.
    Target: activityID (multiclase, 12 clases del protocolo estándar)
    Tipo: clasificación supervisada

H2: Las señales del acelerómetro permiten distinguir entre actividades de baja
    movilidad corporal (sitting, standing, watching TV) que a simple vista parecen
    similares desde el punto de vista inercial.
    Target: subconjunto de activityID {2, 3, 9}
    Tipo: clasificación supervisada (subproblema de H1)

H3: La frecuencia cardíaca puede agruparse en niveles de esfuerzo físico
    (bajo/medio/alto) y dichos niveles son predecibles a partir de las
    señales inerciales de las IMU.
    Target: nivel_esfuerzo (variable derivada categórica de 3 clases a partir de heart_rate)
    Tipo: clasificación supervisada con feature engineering previo
```

---

## 5. Decisiones de ETL ya tomadas (no negociables, están justificadas)

| Decisión | Justificación |
|----------|---------------|
| Drop columnas de orientación (4 cols × 3 IMUs = 12 cols) | Documentación oficial UCI dice explícitamente que son inválidas en esta recolección |
| Excluir activityID = 0 | Períodos transitorios sin actividad definida, ruido para el modelo |
| Agregar columna `subject_id` al unificar | Necesario para cross-validation leave-one-subject-out en Entrega 3 |
| Downsampling 100Hz → 10Hz (cada 10 filas) | Estándar en literatura HAR, reduce 3.8M → ~194K filas sin perder información relevante |
| Interpolación lineal para NaNs en heart_rate | Serie temporal fisiológica: la mediana global no tiene sentido, hay que respetar continuidad temporal |
| NO hacer Label Encoding en esta entrega | activityID ya es numérico; subject_id también. No es necesario. |

---

## 6. Estructura del repositorio

```
pamap2-tpi/
├── data/
│   ├── raw/          ← archivos .dat originales (NO commitear, están en .gitignore por tamaño)
│   ├── processed/    ← CSV consolidado tras ETL
│   └── external/     ← fuentes externas si se agregan
├── notebooks/
│   └── 01_ETL.ipynb  ← notebook principal para Entrega 2
├── reports/
│   └── entrega_2/    ← informe en PDF/DOCX + figuras exportadas
├── src/              ← funciones Python reutilizables (helpers, loaders)
├── .gitignore
└── README.md
```

**IMPORTANTE:** Los archivos .dat originales NO van al repo (son ~500MB). Se cargan desde Google Drive o localmente. Documentar el proceso de descarga en el README.

---

## 7. Nombres de columnas del dataset consolidado (después de ETL)

El CSV final debe tener exactamente estas columnas (sin las de orientación):

```python
COLUMN_NAMES = [
    'timestamp', 'activity_id', 'heart_rate',
    # IMU hand (mano) — 13 columnas válidas de 17
    'hand_temp',
    'hand_acc1_x', 'hand_acc1_y', 'hand_acc1_z',
    'hand_acc2_x', 'hand_acc2_y', 'hand_acc2_z',
    'hand_gyro_x', 'hand_gyro_y', 'hand_gyro_z',
    'hand_mag_x',  'hand_mag_y',  'hand_mag_z',
    # hand_orient_1/2/3/4 → OMITIDAS (inválidas)
    # IMU chest (pecho) — 13 columnas válidas
    'chest_temp',
    'chest_acc1_x', 'chest_acc1_y', 'chest_acc1_z',
    'chest_acc2_x', 'chest_acc2_y', 'chest_acc2_z',
    'chest_gyro_x', 'chest_gyro_y', 'chest_gyro_z',
    'chest_mag_x',  'chest_mag_y',  'chest_mag_z',
    # chest_orient_1/2/3/4 → OMITIDAS (inválidas)
    # IMU ankle (tobillo) — 13 columnas válidas
    'ankle_temp',
    'ankle_acc1_x', 'ankle_acc1_y', 'ankle_acc1_z',
    'ankle_acc2_x', 'ankle_acc2_y', 'ankle_acc2_z',
    'ankle_gyro_x', 'ankle_gyro_y', 'ankle_gyro_z',
    'ankle_mag_x',  'ankle_mag_y',  'ankle_mag_z',
    # ankle_orient_1/2/3/4 → OMITIDAS (inválidas)
    # Columna agregada en el proceso de unificación:
    'subject_id'   # 101 a 109
]
# Total: 3 + 13 + 13 + 13 + 1 = 43 columnas
```

---

## 8. Pasos del ETL en orden de ejecución

```
Paso 1: Carga y unificación
  - Leer cada subject_XXX.dat con pandas (sin header, sep=' ')
  - Asignar COLUMN_NAMES_RAW (54 columnas incluyendo orientación)
  - Agregar columna subject_id = número de sujeto (101..109)
  - Concatenar todos en un DataFrame único

Paso 2: Downsampling
  - Por sujeto y por actividad: tomar cada 10 filas (iloc[::10])
  - Esto preserva la continuidad temporal dentro de cada sesión

Paso 3: Drop columnas de orientación
  - Eliminar las 12 columnas de orientación (4 por IMU × 3 IMUs)
  - Documentar: según documentación UCI, datos inválidos en esta recolección

Paso 4: Exclusión activityID = 0
  - df = df[df['activity_id'] != 0]
  - Registrar cantidad de filas eliminadas

Paso 5: Tratamiento NaNs en heart_rate
  - Interpolación lineal por sujeto y sesión
  - df['heart_rate'] = df.groupby('subject_id')['heart_rate']
                         .transform(lambda x: x.interpolate(method='linear'))
  - Para NaNs al inicio/fin (boundary): forward-fill y backward-fill

Paso 6: Análisis de outliers en señales IMU
  - Calcular IQR por columna y por activityID (no global)
  - No eliminar automáticamente: flaggear y documentar
  - Las señales de sensores tienen outliers físicamente válidos (running, jumping)

Paso 7: Normalización (SOLO documentar la estrategia, aplicar en Entrega 3)
  - Estrategia elegida: StandardScaler (z-score) por columna
  - Motivo: distribuciones no uniformes entre sensores y unidades distintas

Paso 8: Feature engineering para H3
  - Derivar columna 'intensity_level' desde heart_rate:
    - bajo:  heart_rate <= percentil 33
    - medio: heart_rate entre percentil 33 y 66
    - alto:  heart_rate > percentil 66
  - Calcular percentiles SOLO sobre datos con heart_rate no-NaN

Paso 9: Guardar dataset limpio
  - data/processed/pamap2_clean.csv
  - Registrar shape final (filas × columnas)
```

---

## 9. Visualizaciones requeridas para el informe

Deben generarse y exportarse como PNG a `reports/entrega_2/figures/`:

```
Fig 1: % de nulos por columna (barras horizontales, ordenado descendente)
       — mostrar claramente que heart_rate tiene NaNs estructurales

Fig 2: Distribución de clases (activityID) — barras verticales con conteo
       — evidenciar desbalance de clases (problema para modelado en Entrega 3)

Fig 3: Estadísticos descriptivos — tabla o heatmap (mean, std, min, max)
       de las variables sensoriales principales

Fig 4: Serie temporal de aceleración (hand_acc1_x) para 3 actividades distintas
       (ej: lying, walking, running) — 30 segundos de muestra por actividad
       — muestra la naturaleza temporal del dato y diferencias entre clases

Fig 5: Heatmap de correlación entre variables de una misma IMU
       — usar variables de hand IMU para no saturar el gráfico

Fig 6: Boxplot de heart_rate por activityID
       — evidencia diferencias fisiológicas entre actividades (base de H3)

Fig 7: Conteo de registros por sujeto tras downsampling
       — verificar distribución equitativa entre sujetos
```

---

## 10. Tecnologías y restricciones

- **Lenguaje:** Python 3.x
- **Entorno:** Google Colab (el notebook tiene que funcionar ahí)
- **Librerías principales:** pandas, numpy, matplotlib, seaborn, scipy
- **NO usar sklearn en esta entrega** (eso es Entrega 3)
- **Formato del informe:** PDF (generado desde el notebook o redactado aparte)
- **Estilo de código:** funciones documentadas, celdas con markdown explicativo entre cada sección

---

## 11. Lo que NO hay que hacer (errores a evitar)

- ❌ No imputar heart_rate con media/mediana global — es serie temporal, usar interpolación lineal
- ❌ No eliminar outliers automáticamente en señales IMU — flaggear y documentar
- ❌ No aplicar Label Encoding — activityID ya es numérico
- ❌ No mezclar filas de distintos sujetos al interpolar — siempre groupby subject_id primero
- ❌ No subir los archivos .dat al repo de GitHub (son ~500MB en total)
- ❌ No aplicar StandardScaler en esta entrega — solo documentar la estrategia
- ❌ No ignorar el desbalance de clases — visualizarlo y mencionarlo como riesgo para Entrega 3

---

## 12. Referencia de la Entrega 1 (resumen)

El informe de la Entrega 1 ya documentó:
- Plan de proyecto Scrum (5 sprints)
- Roles: Franco Recalde = Product Owner, Emilio Sadir = Scrum Master
- Descripción completa del dataset PAMAP2
- Justificación de elección del dataset
- Calendario hasta junio 2026

No repetir esa información en el informe de la Entrega 2, solo referenciarla.

---

## 13. Formato del informe de Entrega 2

Basarse en el formato del informe de referencia (otro grupo de la misma cátedra, año 2025):

**Estructura:**
1. Objetivo de la entrega + link al Colab
2. Análisis exploratorio (con figuras numeradas + descripción de cada una)
3. Limpieza y preparación de datos (subsección por cada decisión de ETL)
4. Hipótesis definidas (las 3 de la sección 4 de este documento)
5. Conclusiones

**Formato general:**
- Font: Arial 11pt
- Márgenes: 2.5cm
- Header con: UTN FRC | Ciencia de Datos 2026 | 5K4 | Grupo 15
- Cada figura con: número, título en negrita, descripción en cursiva abajo
- Secciones con numeración (1., 2., 3…)
- Tablas con header en color (azul UTN: #1F4E79 o similar)

---

*Fin del contexto. Cualquier duda sobre decisiones técnicas, justificaciones o el dominio del problema: preguntar antes de asumir.*
