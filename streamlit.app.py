import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go


df= pd.read_csv("Data_Kota_Banda_Aceh.csv", sep=";", header=None, skiprows=1, index_col=False)

nama_kolom = [
    "Kota", "Tahun", "DBH_PAJAK", "DBH_SDA", "DBH_Lainnya", "DAU_Grant",
    "DAU_Earmark", "DAK_Fisik", "DAK_Nonfisik", "PAD", "ICT",
    "bm_pendidikan", "bm_kesehatan", "bm_perumahan", "bm_lingkungan",
    "bm_ekonomi", "bm_infrastruktur", "bm_pariwisata",
    "bm_perlindungan_sosial", "KEMISKINAN", "PENGANGGURAN", "KETIMPANGAN",
    "IPM", "PE",
]

df = df.iloc[:, 1:25]
df.columns = nama_kolom

# Mengambil 3 variabel saja ("Tahun" sebagai penanda observasi)
df = pd.DataFrame({
    "Tahun": df["Tahun"].astype(int),
    "PAD": df["PAD"].astype(float),
    "Pengangguran": df["PENGANGGURAN"].astype(float),
    "Kemiskinan": df["KEMISKINAN"].astype(float),
})


# Memisahkan variabel independen dan dependen
X = df[["PAD", "Pengangguran"]]
y = df["Kemiskinan"]

# Menambahkan Intercept
X_model = sm.add_constant(X)

# Estimasi MODEL OLS
model = sm.OLS(y, X_model)
results = model.fit()

# Menampilkan Ringkasan Hasil Regresi
print("\n")
print("=" * 78)
print("                 HASIL REGRESI LINEAR BERGANDA")
print("=" * 78)
print(results.summary())


# Mengambil Koefisien Regresi
intercept = results.params["const"]
coef_pad = results.params["PAD"]
coef_pengangguran = results.params["Pengangguran"]

r_squared = results.rsquared
adjusted_r_squared = results.rsquared_adj


# Membuat Persamaan Regresi
persamaan = (
    f"Ŷ = {intercept:.3f}"
    f" + ({coef_pad:.3f}) X₁"
    f" + ({coef_pengangguran:.3f}) X₂"
)

print("\n")
print("=" * 78)
print("                       PERSAMAAN REGRESI")
print("=" * 78)
print(persamaan)
print("X₁ = PAD, X₂ = Pengangguran, Ŷ = Kemiskinan")

print(f"\nR²          = {r_squared:.4f}")
print(f"Adjusted R² = {adjusted_r_squared:.4f}")


# Menghitung Nilai Prediksi
df["Prediksi"] = results.predict(X_model)
print("\n")
print("=" * 70)
print("                 DATA AKTUAL & PREDIKSI")
print("=" * 70)
print(df[["Tahun", "PAD", "Pengangguran", "Kemiskinan", "Prediksi"]].round(2))


# Membuat GRID untuk Bidang Regresi
x1 = np.linspace(
    df["PAD"].min(),
    df["PAD"].max(),
    40)

x2 = np.linspace(
    df["Pengangguran"].min(),
    df["Pengangguran"].max(),
    40)

X1, X2 = np.meshgrid(x1, x2)


# Menghitung Nilai Y pada Bidang Regresi
Y = intercept + coef_pad * X1 + coef_pengangguran * X2


# Membuat Figure 3D
fig = go.Figure()


# 13. Menampilkan Data Aktual
fig.add_trace(
    go.Scatter3d(
        x=df["PAD"],
        y=df["Pengangguran"],
        z=df["Kemiskinan"],
        mode="markers",
        marker=dict(
            size=7,
            color="red",
            opacity=0.9
        ),

        name="Data Aktual",
        text=[
            f"Tahun {t}"
            for t in df["Tahun"]
        ],

        hovertemplate=(
            "<b>%{text}</b><br>"
            "PAD: %{x}<br>"
            "Pengangguran: %{y}<br>"
            "Kemiskinan: %{z}"
            "<extra></extra>"
        ),
    )
)


# Menampilkan Bidang Regresi
fig.add_trace(
    go.Surface(
        x=X1, y=X2, z=Y,
        opacity=0.60,
        colorscale="Viridis",
        name="Regression Plane",
        hovertemplate=(
            "PAD: %{x:.2f}<br>"
            "Pengangguran: %{y:.2f}<br>"
            "Prediksi Y: %{z:.2f}"
            "<extra></extra>"
        ),
    )
)


# Mengatur Tampilan Grafik
fig.update_layout(
    title={
        "text": (
            "REGRESI LINEAR BERGANDA 3D"
            "<br>"
            f"<sup>{persamaan} | "
            f"R² = {r_squared:.3f}</sup>"
        ),
        "x": 0.5,
    },
    scene={
        "xaxis": {"title": "PAD (X₁)"},
        "yaxis": {"title": "Pengangguran (X₂)"},
        "zaxis": {"title": "Kemiskinan (Y)"},
    },
    width=1000,
    height=750,
    margin={"l": 0, "r": 0, "b": 0, "t": 100},
    legend={"x": 0.02, "y": 0.98},
)


# MENAMPILKAN GRAFIK
fig.show()
