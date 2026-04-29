---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #000000
color: #00FF00
style: |
  section {
    font-family: 'Courier New', Courier, monospace;
    background: radial-gradient(circle, #2a0035 0%, #000000 100%);
    border: 4px solid #FF00FF;
    text-shadow: 2px 2px #000000, 0 0 10px #00FF00;
  }
  h1 {
    color: #FF00FF;
    text-transform: uppercase;
    font-size: 60px;
    border-bottom: 2px dashed #00FF00;
  }
  h2, h3 {
    color: #00FFFF;
  }
  footer {
    color: #FF00FF;
  }
  section::after {
    content: " [ SYSTEM: READY ] ";
    position: absolute;
    bottom: 20px;
    right: 20px;
    font-size: 15px;
    color: #00FF00;
  }
---

# **🛸 NEMO REAL ESTATE EDA 2026**
### [ RETRO-FUTURISM ANALYSIS ]

> MISSION: ANALYZE GANGNAM-STATION NODES
> STATUS: DECODING...

Gemini CLI // Cyber-Analysis Unit

---

## **1. DATABASE OVERVIEW**

- **DATASET**: NEMO HYPER-PLATFORM
- **NODES**: 673 ENTRIES FOUND
- **VARS**: 40 DIMENSIONS
- **TARGET**: DEPOSIT / RENT / PREMIUM
- **LOCATION**: GANGNAM-YEOKSAM QUADRANT

<!--
발표자 노트:
Y2K 감성으로 새롭게 단장한 네모 부동산 EDA 발표를 시작합니다. 2000년대 초반의 사이버틱한 분위기로 데이터를 해석해 보겠습니다. 분석 대상은 강남과 역삼 지역의 673개 매물 노드입니다. 보증금과 월세, 권리금이라는 핵심 변수를 통해 이 거대한 데이터 생태계를 탐험해 보겠습니다.
-->

---

## **2. BUSINESS SECTOR LOGS**

- **PRIMARY**: 'OTHERS' (48.3%) >> F&B >> SERVICE
- **SUB-NODES**: CAFE / MULTI-USE / STARTUP-HUB
- **ANALYSIS**: 
  - HIGH FLEXIBILITY IN SPACE USAGE
  - CAFE CLUSTERING DETECTED

<!--
발표자 노트:
업종 로그를 분석해 보겠습니다. 기타 업종이 48%로 압도적인데, 이는 공간의 용도가 정해지지 않은 자유로운 '데이터 공간'이 많음을 뜻합니다. 특히 카페와 다용도 점포의 강세는 밀레니엄 세대의 유연한 창업 트렌드를 그대로 보여주고 있습니다.
-->

---

## **3. PRICE TYPE & SECTOR FREQ**

<style>
img { width: 450px; border: 3px solid #00FFFF; box-shadow: 0 0 15px #00FFFF; }
</style>

![가격 유형](../images/price_type_dist.png) ![업종 빈도](../images/biz_large_freq.png)

- **MODE**: RENTAL ONLY (>99%)
- **TRIANGLE**: OTHERS / FOOD / SERVICE

<!--
발표자 노트:
시각화 화면입니다. 사이버 블루 테두리로 강조된 그래프를 봐주세요. 시장은 99% 이상 임대 위주로 돌아가고 있습니다. 매매는 거의 '희귀 아이템' 수준이죠. 음식점과 서비스업이 상권의 기둥 역할을 하며 견고한 삼각 구도를 형성하고 있습니다.
-->

---

## **4. DEPOSIT & RENT MATRIX**

![보증금](../images/deposit_dist.png) ![월세](../images/rent_dist.png)

- **CONCENTRATION**: < 100M DEPOSIT / 5M RENT
- **CORRELATION**: **0.948** (ULTRA-STABLE)

<!--
발표자 노트:
가격 매트릭스를 분석합니다. 보증금과 월세의 상관계수는 0.948로, 거의 완벽한 정비례 관계를 보여줍니다. 데이터 시스템이 매우 안정적으로 작동하고 있다는 뜻이죠. 대부분의 매물이 보증금 1억 미만 구간에 밀집해 있어, 진입 장벽이 명확히 구분된 양상을 보입니다.
-->

---

## **5. PREMIUM & SPACE RATIO**

![권리금](../images/premium_dist.png) ![면적대비 월세](../images/size_rent_scatter.png)

- **VALUATION**: PREMIUM AVG > DEPOSIT AVG
- **ANOMALY**: HIGH RENT IN SMALL NODES (LOCATION VALUE)

<!--
발표자 노트:
권리금과 면적의 관계입니다. 권리금 평균이 보증금을 넘어서는 현상은 이 상권의 '영업 가치'가 얼마나 높은지 증명합니다. 산점도에서 보이는 이상치들은 면적을 초월한 '입지 가치'의 파편들입니다. 작은 공간이라도 핵심 노드에 위치하면 엄청난 임대료를 형성합니다.
-->

---

## **6. VERTICAL VALUE & USER REACTION**

![층별가치](../images/area_price_by_floor.png) ![조회수대비찜](../images/view_fav_reg.png)

- **LEVEL**: UNDERGROUND & HIGH-FLOOR RE-VALUED
- **CONVERSION**: TARGETING 'ALZZA' NODES

<!--
발표자 노트:
층별 가치와 유저 반응입니다. 1층만이 정답이 아닌 시대입니다. 지하나 고층의 특화 공간들이 높은 평당가를 기록하고 있죠. 조회수 대비 찜 횟수가 높은 알짜 매물들을 시스템적으로 필터링하여 사용자에게 최적의 매칭을 제공해야 합니다.
-->

---

## **7. KEYWORD TF-IDF SCAN**

![키워드](../images/keyword_tfidf.png)

- **TOP SCAN**: YEOKSAM / GANGNAM / STATION
- **META**: NO-PREMIUM / INTERIOR / CLEAN

<!--
발표자 노트:
마지막 키워드 스캔 결과입니다. 역삼, 강남 등 위치 정보가 시스템의 최상위 메타데이터로 작동합니다. 동시에 '무권리', '인테리어' 같은 키워드는 사용자들이 비용 절감을 가장 강력한 파라미터로 생각하고 있음을 시각적으로 보여줍니다.
-->

---

## **8. STRATEGIC PROTOCOL**

1. **SPACE**: MAXIMIZE VERTICAL VALUE (B1 / 3F+)
2. **FINANCE**: PROTOCOL FOR HIGH PREMIUM LOANS
3. **MARKETING**: USE TARGET KEYWORDS FOR HIGH CTR
4. **HYBRID**: ADAPTIVE MULTI-USE SPACE DESIGN

<!--
발표자 노트:
최종 전략 프로토콜입니다. 1. 지하나 고층의 수직적 가치를 극대화하십시오. 2. 높은 권리금 부담을 덜어줄 금융 프로토콜을 설계하십시오. 3. 위치 기반 키워드로 마케팅 효율을 높이십시오. 4. 다양한 용도로 변신 가능한 하이브리드 공간을 제안하십시오.
-->

---

# **SYSTEM SHUTDOWN.**
#### ANY QUESTIONS? [ ISSUE #1 ]
