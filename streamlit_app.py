
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="StoryDes",
    page_icon="✨",
    layout="wide"
)

# CSS sederhana
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    h1 {
        letter-spacing: -1px;
    }

    .intro {
        font-size: 18px;
        color: #777777;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("✨ StoryDes")
st.markdown(
    '<p class="intro">Selamat datang di ruang digital StoryDes. '
    'Temukan ide, cerita, dan inspirasi di sini.</p>',
    unsafe_allow_html=True
)

st.divider()

# Navigasi
menu = st.sidebar.radio(
    "Navigasi",
    ["Beranda", "Tentang", "Kontak"]
)

if menu == "Beranda":
    st.header("Beranda")
    st.write(
        "Ini adalah halaman utama aplikasi. "
        "Kamu bisa mengembangkan bagian ini sesuai kebutuhan."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Jelajahi Ide")
        st.write("Kumpulkan ide dan temukan inspirasi baru.")

    with col2:
        st.subheader("Mulai Berkarya")
        st.write("Kembangkan gagasanmu menjadi sesuatu yang menarik.")

elif menu == "Tentang":
    st.header("Tentang StoryDes")
    st.write(
        "StoryDes merupakan ruang digital yang dapat "
        "dikembangkan untuk berbagi cerita, tulisan, atau informasi."
    )

elif menu == "Kontak":
    st.header("Hubungi Kami")

    with st.form("form_kontak"):
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        pesan = st.text_area("Pesan")

        kirim = st.form_submit_button("Kirim Pesan")

        if kirim:
            if nama.strip() and email.strip() and pesan.strip():
                st.success(
                    "Formulir berhasil divalidasi. "
                    "Pengiriman pesan ke email belum diaktifkan."
                )
            else:
                st.warning("Silakan lengkapi semua kolom.")

st.divider()
st.caption("© 2026 StoryDes | Dibuat dengan Streamlit")
