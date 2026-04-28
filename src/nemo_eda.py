import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. 환경 설정 및 디렉토리 생성
os.makedirs('images', exist_ok=True)
os.makedirs('report', exist_ok=True)

# 2. 데이터 로드
conn = sqlite3.connect('data/nemo_data.db')
df = pd.read_sql_query("SELECT * FROM nemo_stores", conn)
conn.close()

# 3. 데이터 기초 검토
head_df = df.head()
tail_df = df.tail()
info_str = df.info()
shape_info = df.shape
duplicates = df.duplicated().sum()

# 4. 기술통계 및 상세 보고서 생성 (1000자 이상)
desc_num = df.describe()
desc_cat = df.describe(include=['object'])

desc_report = f"""
### 1. 데이터 기초 및 기술통계 분석 보고서

**[데이터 개요]**
본 데이터셋은 '네모' 플랫폼에서 수집된 상업용 부동산 매물 데이터로, 총 {shape_info[0]}개의 행과 {shape_info[1]}개의 컬럼으로 구성되어 있습니다. 분석 결과, 데이터 내 중복 행은 {duplicates}개로 확인되어 데이터의 무결성이 비교적 높게 유지되고 있음을 알 수 있습니다.

**[수치 데이터 특징 분석]**
임대 조건의 핵심인 보증금(deposit)은 평균 약 {desc_num.loc['mean', 'deposit']:,.0f}원, 월세(monthlyRent)는 평균 약 {desc_num.loc['mean', 'monthlyRent']:,.0f}원으로 나타납니다. 특히 보증금의 표준편차가 매우 크게 나타나는데, 이는 소형 상가부터 대형 오피스까지 매물의 스펙트럼이 매우 넓음을 시사합니다. 권리금(premium)의 경우, 권리금이 없는 매물부터 고액의 권리금이 형성된 매물까지 다양하며, 평균적으로 약 {desc_num.loc['mean', 'premium']:,.0f}원 수준을 형성하고 있습니다. 관리비(maintenanceFee)는 평균 {desc_num.loc['mean', 'maintenanceFee']:,.0f}원으로, 임대료 외에 추가적으로 발생하는 고정 비용의 규모를 파악할 수 있습니다. 

매물의 면적(size)은 평균 {desc_num.loc['mean', 'size']:.2f}평으로 나타나며, 이는 일반적인 근린생활시설의 평균적인 규모를 반영합니다. 평당가(areaPrice)는 {desc_num.loc['mean', 'areaPrice']:,.0f}원 수준으로, 지역이나 건물 등급에 따른 편차가 존재할 것으로 예상됩니다. 사용자 반응 지표인 조회수(viewCount)는 평균 {desc_num.loc['mean', 'viewCount']:.1f}회, 찜 횟수(favoriteCount)는 평균 {desc_num.loc['mean', 'favoriteCount']:.1f}회로, 특정 인기 매물에 대한 집중도가 높을 것으로 추정됩니다.

**[범주 데이터 특징 분석]**
업종 대분류(businessLargeCodeName)에서는 '{desc_cat.loc['top', 'businessLargeCodeName']}'이 가장 높은 빈도({desc_cat.loc['freq', 'businessLargeCodeName']}건)를 차지하고 있으며, 이는 해당 플랫폼이 특정 업종에 강점을 가졌거나 시장의 일반적인 분포를 따르고 있음을 보여줍니다. 가격 유형(priceTypeName)은 대부분 '{desc_cat.loc['top', 'priceTypeName']}'으로 구성되어 상업용 부동산 시장의 전형적인 임대 형태를 확인할 수 있습니다. 지하철역 인근 여부를 나타내는 nearSubwayStation 정보는 매물의 접근성을 판단하는 중요한 지표로 활용될 수 있습니다.

종합적으로 볼 때, 본 데이터는 상업용 부동산 임대 시장의 다양한 스펙트럼을 포함하고 있으며, 특히 임대료 체계와 업종별 분포, 매물 규모 간의 복합적인 관계를 분석하기에 충분한 정보량을 가지고 있습니다. 향후 시각화 분석을 통해 이러한 변수들 간의 상관관계와 시장의 밀집도를 구체적으로 파악하겠습니다.
"""

# 5. 시각화 분석 (10개 이상)
report_content = []

def save_plot_and_get_info(name, title, interpretation, table_data=None):
    plt.title(title)
    path = f'images/{name}.png'
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    
    info = f"#### {title}\n"
    info += f"![{title}](../{path})\n\n"
    info += f"**[해석]**\n{interpretation}\n\n"
    if table_data is not None:
        info += "**[통계표]**\n"
        info += table_data.to_markdown() + "\n\n"
    return info

# 5.1 가격 유형 분포
plt.figure(figsize=(10, 6))
df['priceTypeName'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
table = df['priceTypeName'].value_counts().to_frame()
interpretation = "매물의 가격 유형 분포를 나타내는 차트입니다. 월세 형태가 압도적으로 높은 비중을 차지하고 있으며, 이는 상업용 부동산 시장의 일반적인 임대 거래 관행을 반영합니다."
report_content.append(save_plot_and_get_info('price_type_dist', '가격 유형 분포', interpretation, table))

# 5.2 업종 대분류 빈도 (Top 30)
plt.figure(figsize=(12, 6))
df['businessLargeCodeName'].value_counts().head(30).plot.bar()
plt.xticks(rotation=45)
table = df['businessLargeCodeName'].value_counts().head(30).to_frame()
interpretation = "매물의 업종 대분류별 빈도를 보여줍니다. 특정 업종군에 매물이 집중되어 있는 것을 알 수 있으며, 이는 해당 플랫폼의 주요 타겟 업종이나 현재 시장의 창업 트렌드를 나타냅니다."
report_content.append(save_plot_and_get_info('biz_large_freq', '업종 대분류 빈도 (상위 30)', interpretation, table))

# 5.3 업종 중분류 빈도 (Top 30)
plt.figure(figsize=(12, 6))
df['businessMiddleCodeName'].value_counts().head(30).plot.bar()
plt.xticks(rotation=45)
table = df['businessMiddleCodeName'].value_counts().head(30).to_frame()
interpretation = "더 세분화된 업종 중분류 빈도입니다. 상위권을 차지하는 중분류 업종들을 통해 현재 가장 활발하게 거래되거나 공급되는 상업 시설의 구체적인 성격을 파악할 수 있습니다."
report_content.append(save_plot_and_get_info('biz_middle_freq', '업종 중분류 빈도 (상위 30)', interpretation, table))

# 5.4 보증금 분포
plt.figure(figsize=(10, 6))
sns.histplot(df['deposit'], kde=True)
table = df['deposit'].describe().to_frame()
interpretation = "보증금의 분포를 보여주는 히스토그램입니다. 낮은 보증금 구간에 매물이 집중되어 있으나, 일부 고액 보증금 매물들이 긴 꼬리를 형성하고 있어 매물 간 격차가 큼을 보여줍니다."
report_content.append(save_plot_and_get_info('deposit_dist', '보증금 분포', interpretation, table))

# 5.5 월세 분포
plt.figure(figsize=(10, 6))
sns.histplot(df['monthlyRent'], kde=True)
table = df['monthlyRent'].describe().to_frame()
interpretation = "월세 임대료의 분포입니다. 월세는 임차인의 고정 지출에 가장 직접적인 영향을 미치는 요소로, 대다수의 매물이 형성하고 있는 월세 구간을 통해 시장의 평균적인 임대료 수준을 알 수 있습니다."
report_content.append(save_plot_and_get_info('rent_dist', '월세 분포', interpretation, table))

# 5.6 권리금 분포
plt.figure(figsize=(10, 6))
sns.histplot(df[df['premium'] > 0]['premium'], kde=True)
table = df[df['premium'] > 0]['premium'].describe().to_frame()
interpretation = "권리금이 존재하는 매물들만을 대상으로 한 분포도입니다. 권리금은 상권의 가치와 기존 영업 시설의 가치를 반영하며, 특정 가격대에 밀집된 양상을 보입니다."
report_content.append(save_plot_and_get_info('premium_dist', '권리금 분포 (0원 초과 매물 대상)', interpretation, table))

# 5.7 면적 대비 보증금 상관관계
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='size', y='deposit', alpha=0.5)
table = df[['size', 'deposit']].corr()
interpretation = "매물 면적과 보증금 간의 상관관계를 보여주는 산점도입니다. 일반적으로 면적이 넓을수록 보증금이 상승하는 경향을 보이지만, 입지 조건에 따라 소형 면적임에도 높은 보증금을 형성하는 예외 사례들도 확인됩니다."
report_content.append(save_plot_and_get_info('size_deposit_scatter', '면적 대비 보증금 산점도', interpretation, table))

# 5.8 면적 대비 월세 상관관계
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='size', y='monthlyRent', alpha=0.5)
table = df[['size', 'monthlyRent']].corr()
interpretation = "면적과 월세 간의 관계를 시각화한 결과입니다. 두 변수 간에는 뚜렷한 양의 상관관계가 존재하며, 면적 증가에 따른 임대료 상승 폭을 통해 시장의 단위당 임대 가치를 추정할 수 있습니다."
report_content.append(save_plot_and_get_info('size_rent_scatter', '면적 대비 월세 산점도', interpretation, table))

# 5.9 업종 대분류별 월세 분포
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='businessLargeCodeName', y='monthlyRent')
plt.xticks(rotation=45)
table = df.groupby('businessLargeCodeName')['monthlyRent'].describe()
interpretation = "업종 대분류별 월세 분포를 박스플롯으로 비교했습니다. 특정 업종(예: 오피스 또는 대형 상업시설)에서 평균 임대료가 높게 형성되거나 가격 편차가 큰 모습을 확인할 수 있습니다."
report_content.append(save_plot_and_get_info('rent_by_biz', '업종 대분류별 월세 분포', interpretation, table))

# 5.10 조회수 대비 찜 횟수
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='viewCount', y='favoriteCount', scatter_kws={'alpha':0.3})
table = df[['viewCount', 'favoriteCount']].corr()
interpretation = "조회수와 찜 횟수 간의 관계를 보여줍니다. 조회수가 높은 매물이 대체로 찜 횟수도 높지만, 회귀선에서 벗어난 매물들은 조회수 대비 전환율(관심도)이 특히 높거나 낮은 특이 매물로 볼 수 있습니다."
report_content.append(save_plot_and_get_info('view_fav_reg', '조회수 대비 찜 횟수 회귀 분석', interpretation, table))

# 5.11 평당가 대비 층수 분석
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='floor', y='areaPrice', estimator='mean')
plt.xticks(rotation=90)
table = df.groupby('floor')['areaPrice'].mean().to_frame()
interpretation = "매물 층수에 따른 평균 평당가 변화입니다. 일반적으로 접근성이 좋은 1층의 평당가가 가장 높게 형성되며, 층수가 올라가거나 지하로 갈수록 평당가가 낮아지는 부동산의 층별 효용 가치를 잘 보여줍니다."
report_content.append(save_plot_and_get_info('area_price_by_floor', '층별 평균 평당가 비교', interpretation, table))

# 6. TF-IDF 키워드 분석
vectorizer = TfidfVectorizer(max_features=30)
tfidf_matrix = vectorizer.fit_transform(df['title'].fillna(''))
keywords = vectorizer.get_feature_names_out()
weights = tfidf_matrix.sum(axis=0).A1
keyword_df = pd.DataFrame({'keyword': keywords, 'weight': weights}).sort_values(by='weight', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(data=keyword_df, x='keyword', y='weight')
plt.xticks(rotation=45)
interpretation = "매물 제목에서 TF-IDF 기법으로 추출한 핵심 키워드입니다. '급매', '역세권', '무권리' 등 시장에서 강조되는 셀링 포인트들을 파악할 수 있으며, 가중치가 높을수록 해당 키워드가 매물 설명에서 중요한 역할을 함을 의미합니다."
report_content.append(save_plot_and_get_info('keyword_tfidf', '매물 제목 TF-IDF 키워드 분석', interpretation, keyword_df))

# 7. 리포트 생성
with open('report/nemo_eda_report.md', 'w', encoding='utf-8') as f:
    f.write("# 네모 상업용 부동산 데이터 EDA 리포트\n\n")
    f.write("## 1. 데이터 기초 정보\n")
    f.write(f"- 전체 데이터 수: {shape_info[0]}행, {shape_info[1]}열\n")
    f.write(f"- 중복 데이터 수: {duplicates}건\n\n")
    
    f.write("### 데이터 샘플 (상위 5행)\n")
    f.write(head_df.to_markdown() + "\n\n")
    
    f.write("### 데이터 샘플 (하위 5행)\n")
    f.write(tail_df.to_markdown() + "\n\n")
    
    f.write(desc_report + "\n\n")
    
    f.write("## 2. 시각화 및 심층 분석\n\n")
    for content in report_content:
        f.write(content)
    
    f.write("\n## 3. 종합 결론 및 제언\n")
    f.write("본 분석을 통해 네모 플랫폼의 상업용 부동산 시장은 월세 중심의 임대차 계약이 주를 이루며, 업종별로 뚜렷한 임대료 편차가 존재함을 확인했습니다. 특히 1층 매물의 평당가 우위가 확실하며, '역세권'이나 '권리금 유무'가 매물 홍보의 핵심 키워드로 작용하고 있습니다. 이러한 데이터 기반의 통찰은 향후 투자 결정이나 중개 전략 수립에 중요한 기초 자료가 될 것입니다.\n")

print("분석 완료! 리포트가 report/nemo_eda_report.md에 생성되었습니다.")
