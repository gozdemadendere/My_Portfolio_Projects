####################################################################################################
# PROJECT : FLO | RFM Analizi ile Müşteri Segmentasyonu (Customer Segmentation with RFM Analysis)
####################################################################################################

# RFM analizi; Recency, Frequency, Monetary metriklerinden faydalanarak, müşteri segmentasyonu için kullanılan bir tekniktir.
# Müşterilerin satın alma alışkanlıkları üzerinden segmentlere ayrılmasını, ve bu segmentler özelinde stratejiler geliştirilmesini sağlar.

# Recency   = Analiz tarihi - Müşterinin son satın alma tarihi
# Frequency = Müşterinin toplam satın alma sayısı   (toplam işlem veya fatura sayısı)
# Monetary  = Müşterinin TOPLAM Harcama tutarı


#### PROJE ADIMLARI ####
# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics: Recency, Frequency, Monetary sütunlarını olusturma)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Project's Business Questions
# 8. BONUS: Tüm Sürecin Fonksiyonlaştırılması





###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# Türkiye ayakkabı pazarının öncü firmalarından FLO, müşterilerini satın alma alışkanlıkları üzerinden segmentlere ayırmak ve bu segmentler özelinde stratejiler geliştirmek istiyor.
# Ayrıca aşağıda, 7. adımda "Project's Business Questions" bölümunde yer alan soruların cevaplanması bekleniyor.

# Veri Seti Hikayesi
# Veri seti, son alışverişlerini 2020 - 2021 yıllarında OmniChannel (hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.

# Değişkenler
# master_id                         : Eşsiz müşteri numarası
# order_channel                     : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel                : En son alışverişin yapıldığı kanal
# first_order_date                  : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date                   : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online            : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline           : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online       : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline      : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online  : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12       : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi





##################################################################################
# 2. Veriyi Anlama (Data Understanding)
##################################################################################

# Import libraries
import datetime as dt
import pandas as pd

pd.set_option('display.max_columns', None)    # tüm sütunlar gelsin
pd.set_option("display.width", 500)           # tüm sütunlar "yanyana" gelsin
pd.set_option("display.precision", 3)         # float türündeki sayılarda virgül sonrasi 3 basamak olsun
pd.set_option('display.float_format', '{:.0f}'.format)  # float türündeki sayıları tam sayı olarak görüntülememizi saglar.
# pd.set_option('display.max_rows', None)
# pd.set_option('display.float_format', lambda x: '%.3f' % x)


# Read the data from CSV
df_ = pd.read_csv("/Users/gozdemadendere/Desktop/PycharmProjects/CRM_Analytics/FLO_project_RFM_customer_segmentation/flo_data_20k.csv")
df = df_.copy()


# a. İlk 10 gözlem
df.head(10)

# b. Değişken isimleri
df.columns

# c. Boyut
df.shape   # (19945 satir, 12 sutun/degisken)

# d. Betimsel istatistik (sayisal degiskenlere ait)
df.describe()
# Yorum 1:  min alisveris sayilari ve harcama tutarlari 1 veya 1den buyuk olmali, oyle gorunuyor
# Yorum 2: %75 ile %100 yani max arasinda bayagi fark olanlar var, aykirilik var: online'da %75lik degerde bu gibi aykiri degerleri analizden cikarmak isteriz
# Yorum 3: ornegin online'da mean 3, %50lik deger 2, tutarli gorunuyor

# e. Boş değerler
df.isnull().sum()  # null / NaN deger yok, olsaydi silebilirdik, veya doldurabilirdik.

# f. Değişken tipleri incelemesi
df.dtypes   # tarihsel degiskenler object gorunuyor > date e cevrilmeli
df.info()


################################################
# Exploratory Data Analysis Function : Displays basic characteristics of the DataFrame.

def check_df(dataframe, head=5):
    print("__________________________________________________________________ FIRST 5 ROWS __________________________________________________________________ ")
    print(dataframe.head(head))
    print("__________________________________________________________________  LAST 5 ROWS __________________________________________________________________ ")
    print(dataframe.tail(head))
    print("__________________________________________________________________  DATA SHAPE ___________________________________________________________________ ")
    print(dataframe.shape)
    print("_________________________________________________________________  GENERAL INFO __________________________________________________________________ ")
    print(dataframe.info())
    print("__________________________________________________________________  NULL VALUES __________________________________________________________________ ")
    print(dataframe.isnull().sum().sort_values(ascending=False))
    print("_______________________________________________________________  DUPLICATED VALUES _______________________________________________________________ ")
    print(dataframe.duplicated().sum())
    print("____________________________________________________________________ DESCRIBE ____________________________________________________________________ ")
    print(dataframe.describe([0, 0.05, 0.1, 0.25, 0.50, 0.95, 0.99, 1]).T)

# Use the function
check_df(df)

################################################





##################################################################################
# 3. Veri Hazırlama (Data Preparation)
##################################################################################

# 1) Omnichannel, müşterilerin hem online hem offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.

# total_order_number ve total_customer_value isimli 2 yeni sutun olusturalim:
df["total_order_number"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_customer_value"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

# master_id sutun ismini customer_id olarak degistirelim
df = df.rename(columns={"master_id": "customer_id"})


# 2) Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.dtypes

# Tarihsel değerleri datetime nesnelerine dönüştürelim
df["first_order_date"] = pd.to_datetime(df["first_order_date"])
df["last_order_date"] = pd.to_datetime(df["last_order_date"])
df["last_order_date_online"] = pd.to_datetime(df["last_order_date_online"])
df["last_order_date_offline"] = pd.to_datetime(df["last_order_date_offline"])

# 3) Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
(df.groupby("order_channel").agg({"customer_id": "count", "total_order_number": "mean", "total_customer_value": "mean"}).sort_values(by="customer_id", ascending=False))
# Sonuc: Total musteri sayisi buyukten kucuge:  Android App > Mobile > Ios App > Desktop

# 4) En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df.groupby("customer_id").agg({"total_customer_value": "sum"}).sort_values(by="total_customer_value", ascending=False).head(10)

# 5) En fazla siparişi veren ilk 10 müşteriyi sıralayınız. (offline ve online toplaminda)
df.groupby("customer_id").agg({"total_order_number": "sum"}).sort_values(by="total_order_number", ascending=False).head(10)





##################################################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
##################################################################################

# Recency:    Analiz tarihi - Müşterinin son satın alma tarihi
# Frequency:  Müşterinin toplam satın alma sayısı  (Toplam işlem/fatura sayısı)
# Monetary:   Müşterinin TOPLAM Harcama tutarı

## KEY NOTES !!!
# Frequency ve ardından Recency daha önemli metriklerdir.
# RFM skorları üzerinden segmentler oluşturulurken, Monetary metriği kullanılmaz! Çünkü zaten Recency ve Frequency varsa, otomatik olarak Monetary de gelir.


### 1) Analizin yapıldığı günü tanımlayalım.  Dataframe deki en son satın alma tarihi 30 Mayıs 2021 ise:
df["last_order_date"].max()    # dataframe deki en son satın alma tarihi !!
today_date = dt.datetime(2021, 6, 1)

### 2) Müşteri özelinde Recency, Frequency ve Monetary metriklerini hhesaplayalım (3 yeni sütun oluşturarak)
# Gerekirse Customer ID ye göre gruplayalım, müşterileri tekilleştirelim (Customer ID ler burada her satirda tek, gruplammaya gerek yoktur.)
# Customer ID e gore gruplama ornegi, rfm.py dosyasinda mevcut !!

rfm = pd.DataFrame()
rfm["customer_id"] = df["customer_id"]
rfm["recency"] = (today_date - df["last_order_date"]).dt.days
rfm["frequency"] = df["total_order_number"]
rfm["monetary"] = df["total_customer_value"]


### 3) Genel olarak degerleri kontrol edelim
rfm.describe().T
# Baktigimizda, monetary ve frequency min degeri >= 1 gorunuyor, mantikli (aksi takdirde sunu yapardik: rfm = rfm.loc[rfm["monetary"] > 0, :]  )

rfm["frequency"].describe([0.2, 0.4, 0.6, 0.8])
rfm["recency"].describe([0.2, 0.4, 0.6, 0.8])






##################################################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
##################################################################################

## RFM metriklerini RFM skorlarına çevirmedeki amaç:
# Farklı ölçek türlerine sahip RFM metriklerini aynı ölçek türüne çevirme
# RFM metrikleri üzerinde bir nevi standartlaştırma işlemi uygulama
# RFM metriklerini birbirleri ile kıyaslanabilir formata getirme

## Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevirelim
rfm["recency_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’un tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

# recency_score ve frequency_score ve monetary_score'un tek bir değişken olarak ifade edilmesi ve RFM_SCORE olarak kaydedilmesi
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))


# Örnek: Aşağıdaki kodun çıktısı bize hangi RFM segmentini verir? : champions! (Recency=5, Frequency=5)
rfm.loc[rfm["RF_SCORE"] == "55", :]

# Örnek: Aşağıdaki kodun çıktısı bize hangi RFM segmentini verir? : hibernating! (Recency=1, Frequency=1)
rfm.loc[rfm["RF_SCORE"] == "11", :]





##################################################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
##################################################################################

### 1) RFM Score larına göre Segment Map i oluşturma
# regex ile yapacağız  (: raw string demektir)

seg_map = {
    r'[1-2][1-2]': 'hibernating',           # 1.elemanda 1 veya 2   &   2.elemanda 1 veya 2 varsa
    r'[1-2][3-4]': 'at_Risk',               # 1.elemanda 1 veya 2   &   2.elemanda 3 veya 4 varsa
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',                # 1.elemanda 3          &   2.elemanda 3 varsa
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


### 2) Yeni bir segment sütunu olustur: RF_SCORE sütunundaki değişkenleri, seg_map içine bakarak değiştir
# regex=True : eğer seg_map içindeki keys & values düzenli ifadeler ise, bu desenleri eşleştir
rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

### 3) csv dosyası olarak kaydedelim.  (kodu çalıştır, Project'te CRM_Analytics sağ tıkla, Reload from Disk tıkla, dosya orada)
rfm.to_csv("rfm.csv")



# GÖREV: RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
# Mesela bir departman bizden, cant_loose segmentine ait musterilerin id lerini istediyse: segment i cant_loose olanlarin index bilgileri, yani Customer ID leri !!
rfm.loc[rfm["segment"] == "cant_loose", :].index

# bir dataframe olusturalim
new_df = pd.DataFrame()
new_df["cant_loose_customer_id"] = rfm.loc[rfm["segment"] == "cant_loose", :].index

#  csv dosyası olarak kaydedelim.
new_df.to_csv("cant_loose_customers.csv")





##################################################################################
# 7. PROJECT'S BUSINESS QUESTIONS
##################################################################################

##########
# GÖREV 1:
##########
# Segmentlerin recency, frequency ve monetary ortalamalarını inceleyiniz.
rfm.groupby("segment").agg({"recency": ["mean", "count"], "frequency": ["mean", "count"], "monetary": ["mean", "count"]})
# veya rfm[["recency", "frequency", "monetary", "segment"]].groupby("segment").agg(["mean", "count"])

#                          recency       frequency       monetary
#                        mean count      mean count     mean count
# segment
# about_to_sleep       113.79  1629      2.40  1629   359.01  1629
# at_Risk              241.61  3131      4.47  3131   646.61  3131
# cant_loose           235.44  1200     10.70  1200  1474.47  1200
# champions             17.11  1932      8.93  1932  1406.63  1932
# hibernating          247.95  3604      2.39  3604   366.27  3604
# loyal_customers       82.59  3361      8.37  3361  1216.82  3361
# need_attention       113.83   823      3.73   823   562.14   823
# new_customers         17.92   680      2.00   680   339.96   680
# potential_loyalists   37.16  2938      3.30  2938   533.18  2938
# promising             58.92   647      2.00   647   335.67   647




##########
# GÖREV 2:
##########
# FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Bu markanın ürün fiyatları genel müşteri tercihlerinin üstünde.
# Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçilmek isteniliyor.
# Bu müşterilerin "sadık müşterilerden (champions, loyal_customers) ve kadın kategorisinden alışveriş yapan kişiler" olması planlandı.
# Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.

rfm.head()  # sadık müşteriler burada segment sutununda: loyal_customers
df.head()   # kadın kategorisi bu df de interested_in_categories_12 sutununda: KADIN kelimesini iceren satirlar


# rfm dataframe inde segment = loyal_customers olanlari secelim
loyal_customers_df = rfm.loc[rfm["segment"].isin(["champions", "loyal_customers"]), :]
loyal_customers_df.reset_index(inplace=True) # asagidaki merge islemi icin, index sutunu olmaasi gerek!

# df dataframe inde KADIN kategorisinden alisveris yapanlari filtreleyelim
kadin_cat_df = df.loc[df["interested_in_categories_12"].str.contains("KADIN")]

# bu 2 df i ortak customer_id leri uzerinden birlestirelim
# !! dataframe lere ait, sadece istedigim sutunlari sectim !!
merged_df = pd.merge(loyal_customers_df[["customer_id", "segment"]], kadin_cat_df[["customer_id", "interested_in_categories_12"]], how="inner", on="customer_id")

# csv dosyası olarak kaydedelim.
merged_df.to_csv("yeni_marka_hedef_müşteri_id.csv")




##########
# GÖREV 3:
##########
# FLO Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır.
# Bu indirimle ilgili kategorilerle ilgilenen "geçmişte iyi müşterilerden olan ama uzun süredir alışveriş yapmayan" ve "yeni gelen müşteriler" özel olarak hedef alınmak isteniliyor.
# Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv olarak kaydediniz.

rfm.head()  # burada segment sutununda, cant_loose, at_Risk ve new_customers olanlar
df.head()   # ERKEK, COCUK kategorisi bu df de interested_in_categories_12 sutununda: ERKEK veya COCUK kelimelerini iceren satirlar


# rfm dataframe inde segment = cant_loose, at_Risk ve new_customers olanlari secelim
new_df = rfm.loc[rfm["segment"].isin(["cant_loose", "at_Risk", "new_customers"]), :]

# df dataframe inde ERKEK veya COCUK kategorisinden alisveris yapanlari filtreleyelim
erkek_cocuk_df = df.loc[ (df["interested_in_categories_12"].str.contains("ERKEK")) | (df["interested_in_categories_12"].str.contains("COCUK")) ]

# bu 2 df i ortak customer_id leri uzerinden birlestirelim
# !! dataframe lere ait, sadece istedigim sutunlari sectim !!
merged_df = pd.merge(new_df[["customer_id", "segment"]], erkek_cocuk_df[["customer_id", "interested_in_categories_12"]], how="inner", on="customer_id")

### csv dosyası olarak kaydedelim.
merged_df.to_csv("indirim_hedef_müşteri_ids.csv")






##################################################################################
# 8. Tüm Sürecin Fonksiyonlaştırılması (Functionalization)
##################################################################################

df = df_.copy()

def create_rfm(dataframe):
    # Veriyi Hazırlma
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # RFM METRIKLERININ HESAPLANMASI
    dataframe["last_order_date"].max()  # 2021-05-30
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).astype('timedelta64[D]')
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # RF ve RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency","frequency","monetary","RF_SCORE","RFM_SCORE","segment"]]


rfm_df = create_rfm(df)


### NOTES !
# 1) Bu fonksiyon içindeki adımlar, ayrı ayrı fonksiyonlar şeklinde de yazılabilir. return çıktıları sonraki adıma ait fonksiyonda kullanılabilir.
# 2) Bu fonksiyonu örneğin her ay çalıştırıyorsak, dataframe içeriği değişmiş olabileceğinden, çıktıların doğruluğunu mutlaka kontrol etmeliyiz.(fonksiyon öncesi adımlarda da)





