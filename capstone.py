import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# Layout
st.set_page_config(
    page_title='Capstone Dorothea',
    layout='wide'
)

# Title
st.markdown("<h1 style='text-align: center; color: #DE3163;'>Apakah Pendidikan suatu <i>Privilage</i> bagi Perempuan?</h1>", unsafe_allow_html=True)
st.write('Ketidaksetaraan gender masih dirasakan oleh para perempuan di hampir seluruh bagian dunia hingga saat ini. Tidak terkecuali dalam bidang pendidikan. Kesempatan mengenyam pendidikan masih dianggap sebagai *privilage* milik segelintir perempuan. Apakah betul? Mari kita bedah data-datanya.')
st.write('---')

# Viz 1 : World Map, Gender Gap Across the World ====================================================================================
# Data source: https://genderdata.worldbank.org/indicators/se-prm-cmpl-zs/?gender=gender-gap

st.subheader('Ketidaksetaraan Gender dalam Pendidikan di Dunia')

st.write('Berdasarkan data tingkat penyelesaian pendidikan dasar (*primary completion rate*), secara umum laki-laki memiliki kesempatan lebih besar untuk menyelesaikan pendidikan dasar dibandingkan dengan perempuan. Bahkan terdapat perbedaan hingga sebesar **36\%** pada kesempatan penyelesaian pendidikan dasar laki-laki dan perempuan di Afganistan. It’s a *blue, blue* world!')
df1 = pd.read_csv('world_primary_completion.csv')

fig1 = px.choropleth(df1, 
                    locations="country_code",
                    color="gender_gap",
                    hover_name="country",
                    hover_data={
                        'country_code': False,
                        'gender_gap' : ':.2f',
                        'completion_rate_female': ':.2f',
                        'completion_rate_male' : ':.2f'
                    },
                    color_continuous_scale=["blue","blue","white","red"])
st.write(fig1)

# Viz 2 : Line Chart, Gender Gap in Various Level of Education ========================================================================
# Data source: https://databank.worldbank.org/source/gender-statistics
# https://towardsdatascience.com/a-multi-page-interactive-dashboard-with-streamlit-and-plotly-c3182443871a

st.subheader('Ketidaksetaraan Pencapaian Pendidikan di Berbagai Jenjang')

st.write('Jika dilihat dari jenjang pendidikannya, jumlah perempuan yang dapat menyelesaikan pendidikan di jenjang pendidikan dasar, menengah bawah, dan menengah atas selalu lebih rendah dibandingkan jumlah laki-laki.')
df_gender = pd.read_csv('male_female_edlvl.csv')

col1_edlvl, col2_edlvl= st.columns([1,2])
with col1_edlvl:
    edlist = df_gender['ed_lvl'].unique()
    ed_lvl = st.selectbox("Pilih tingkat pendidikan:", edlist)

    st.write('Terdapat perbedaan kesempatan pencapaian pendidikan antara laki-laki dengan perempuan sebesar:')
    
    ed_name = 'dasar'
    if ed_lvl == 'primary':
        ed_name = 'dasar'
        st.metric("", "2.8%")
    elif ed_lvl == 'lower_secondary':
        ed_name = 'menengah bawah'
        st.metric("", "2.7%")
    else:
        ed_name = 'menengah atas'
        st.metric("", "1.4%")
    st.write('di jenjang pendidikan ', ed_name, '.')
with col2_edlvl:
    fig2 = px.line(df_gender[df_gender['ed_lvl']==ed_lvl],
                    x = 'year',
                    y = ['male','female'],
                    # labels=dict()
                    color_discrete_sequence=['blue','#DE3163'],)
    fig2.update_layout(
        xaxis_title='Tahun',
        yaxis_title=ed_lvl,
        legend_title='Gender'
    )
    st.plotly_chart(fig2)

# Viz 3 : Scatter Plot, Correlation Between Expected Years of Schooling and Employment ================================================

st.subheader('Korelasi Ekspektasi Durasi Sekolah & Pekerjaan')

df_emp = pd.read_csv('edu_vs.csv')
df_emp = df_emp.dropna()

col1_emp, col2_emp= st.columns([2,1])
with col1_emp:
    fig3 = px.scatter(df_emp,
                    x='school_life',
                    y='employment',
                    hover_name='country',
                    color_discrete_sequence=['#DE3163'],
                    trendline='ols')
                    # labels=dict())
    fig3.update_layout(
        xaxis_title='Ekspektasi Durasi Sekolah (tahun)',
        yaxis_title='Angka Partisipasi Kerja (%)',
        legend_title='Gender'
    )
    st.plotly_chart(fig3)
with col2_emp:
    corr_emp = df_emp['school_life'].corr(df_emp['employment'], method='pearson')
    st.write('')
    st.write('Ekspektasi durasi sekolah para perempuan di berbagai negara di dunia berkorelasi secara positif terhadap tingkat partisipasi kerja (*employment*).')
    st.metric('Koefisien Korelasi Spearman (rho)', format(corr_emp,'.2f'))
    st.write('Artinya, pemberdayaan ekonomi pada perempuan dapat dimulai melalui pendidikan. Semakin tinggi atau semakin lama perempuan dapat mengeyam pendidikan, maka semakin besar pula kemungkinan mereka dapat memperoleh pekerjaan.')

# Viz 4 : Scatter Plot, Correlation Between Years of Education and Child Mortality ====================================================

st.subheader('Korelasi Rata-rata Durasi Sekolah & Tingkat Mortalitas Anak')

df3 = pd.read_csv('childmortality_vs_education.csv')

col1_mor, col2_mor= st.columns([2,1])
with col1_mor:
    fig4 = px.scatter(df3,
                    x='mean_schooling',
                    y='child_mortality',
                    hover_name='country',
                    color_discrete_sequence=['#DE3163'],
                    trendline='ols')
    fig4.update_layout(
        xaxis_title='Rata-rata Durasi Sekolah (tahun)',
        yaxis_title='Tingkat Mortalitas Anak (%)',
        legend_title='Gender'
    )
    st.plotly_chart(fig4)
with col2_mor:
    corr_mor = df3['mean_schooling'].corr(df3['child_mortality'],method='pearson')
    st.write('')
    st.write('Hal yang lebih mengejutkan adalah terdapat korelasi negatif (berbanding terbalik) antara durasi sekolah perempuan dengan angka kematian anak.')
    st.metric('Koefisien Korelasi Spearman (rho)', round(corr_mor,2))
    st.write('Tingkat pendidikan perempuan dapat berbanding terbalik dengan tingkat kematian anak karena perempuan dengan tingkat pendidikan yang lebih tinggi cenderung memiliki kesadaran yang lebih tinggi tentang kesehatan dirinya sendiri dan anak-anaknya.')

# Viz 5 : Bar Plot, Indonesia =========================================================================================================
# Data Source: https://bps.go.id/indicator/28/1468/2/angka-melek-huruf-penduduk-umur-15-59-tahun-menurut-jenis-kelamin.html
# & https://bps.go.id/indicator/28/1431/2/rata-rata-lama-sekolah-penduduk-umur-15-tahun-menurut-jenis-kelamin.html 

st.write('---')
st.header('Bagaimana dengan Kesetaraan Gender dalam Pendidikan di Indonesia?')

df_indo = pd.read_csv('indo.csv')
df_indo['Tahun'] = df_indo['Tahun'].astype(str)

col1_id, col2_id = st.columns(2)
with col1_id:
    fig5 = px.line(df_indo[df_indo['Aspek']=='Melek Huruf'],
                    x = 'Tahun',
                    y = ['Laki-laki','Perempuan'],
                    color_discrete_sequence=['blue','#DE3163'],
                    width=575, height=400)
    fig5.update_layout(
        yaxis_title='Angka Melek Huruf (%)',
        # legend_title='Gender'
        showlegend=False,
        yaxis_range=[95,100]
    )
    st.plotly_chart(fig5)
with col2_id:
    fig6 = px.line(df_indo[df_indo['Aspek']=='Lama Sekolah'],
                    x = 'Tahun',
                    y = ['Laki-laki','Perempuan'],
                    color_discrete_sequence=['blue','#DE3163'],
                    width=600, height=400)
    fig6.update_layout(
        yaxis_title='Lama Sekolah (tahun)',
        legend_title='Gender',
        yaxis_range=[7,10]
        # xaxis_range=[2014,2022]
    )
    st.plotly_chart(fig6)
st.write('Berdasarkan data hingga tahun 2021, masih terdapat ketidaksetaraan gender dalam bidang pendidikaan di Indonesia jika dilihat dari angka melek huruf dan rata-rata lama/durasi sekolah perempuan dibandingkan dengan laki-laki. Kabar baiknya, kesenjangan pendidikan antara laki-laki dan perempuan secara umum semakin menipis tiap tahunnya.')
st.write('Namun, tentunya masih diperlukan upaya-upaya untuk memperjuangkan kesempatan pendidikan bagi para perempuan,baik di Indonesia maupun dunia.')

# Kesimpulan ==========================================================================================================================
st.write('---')
# col1_simp, col2_simp= st.columns([1,6])
# with col1_simp:
#     st.subheader('Kesimpulan')
# with col2_simp:
#     st.write('1. Ketidaksetaraan gender dalam pendidikan masih dirasakan di hampir seluruh bagian dunia, termasuk di Indonesia.')
#     st.write('2. Pendidikan perempuan berkorelasi secara positif dengan angka partisipasi kerja dan berkorelasi negatif dengan tingkat kematian anak.')
#     st.write('')
col1_sou, col2_sou= st.columns([1,6])
with col1_sou:
    st.subheader('Data Source')
with col2_sou:
    st.write('bps.go.id')

col1_cre, col2_cre = st.columns([6,2])
with col1_cre:
    ''
with col2_cre:
    st.markdown('DQ Lab Tetris II - Capstone Project')
    st.markdown('Dorothea Claresta P (039)')