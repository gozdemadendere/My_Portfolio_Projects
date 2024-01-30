
#############################################
# MÜŞTERİ SEGMENTASYON ANALİZİ (CUSTOMER SEGMENTATION PROCESS)
# KURAL BAZLI SINIFLANDIRMA İLE POTANSİYEL MÜŞTERİ GETİRİSİ HESAPLAMA (RULE BASED CLASSIFICATION)
#############################################

# Müşteri segmentasyonu, benzer özelliklere, ihtiyaçlara ve davranışlara sahip müşterileri gruplara ayırma,
# ve bu gruplara özgü pazarlama stratejileri oluşturma sürecidir.

# Segmentasyonun amacı, yeni müşterilerin hangi segmentte yer aldığını belirleyerek,
# pazarlama stratejilerini desteklemek ve bu müşterilerin ortalama getiri beklentisini hesaplamaktır.





#############################################
# İŞ PROBLEMI / PROJE HEDEFLERİ
#############################################
# Bir oyun şirketi, müşteri özelliklerine dayanarak, seviye tabanlı yeni müşteri tanımları (persona) oluşturmayı
# ve bu tanımlara göre müşterileri segmentlere ayırmayı amaçlıyor.

# Ardından, bu segmentlere göre potansiyel yeni müşterilerin, şirkete ortalama gelir getirisini tahmin etmek istiyor.

# Örneğin: Türkiye’den IOS kullanan 25 yaşındaki bir erkek kullanıcının, ortalama getirisinin belirlenmesi hedefleniyor.





#############################################
# VERİ SETİ HİKAYESİ
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin ürünlerinin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı demografik bilgilerini içeriyor.
# Veri setinde her satış işlemi için bir kayıt bulunuyor, yani tablo tekilleştirilmemiştir.
# Bu, belirli demografik özelliklere sahip bir kullanıcının birden fazla alışveriş yapmış olabileceği anlamına geliyor.


# Price:    Müşterinin yaptığı harcama tutarı
# Source:   Müşterinin kullandığı cihaz türü
# Sex:      Müşterinin cinsiyeti
# Country:  Müşterinin ülkesi
# Age:      Müşterinin yaşı





#############################################
# PROJE AŞAMALARI
#############################################

# Veri setinin incelenmesi ve anlaşılması
# Veri manipülasyonu
# Müşteri tanımlarına göre segmentlerin oluşturulması (Segmentasyon işlemi)
# Her bir segment için ortalama gelir tahmininin yapılması
# Sonuçlara göre, yeni müşterilerin sınıflandırılması ve ne kadar gelir getirebileceğinin tahmin edilmesi


# 1) Dataframe i COUNTRY, SOURCE, SEX, AGE e gore gruplama ve karsisinda ortalama Price lari gorme
# 2) AGE_CAT isimli yeni bir age kategorisi sutunu olusturma
# 3) CUSTOMERS_LEVEL_BASED isimli yeni bir persona tanimlama sutunu olusturma (FRA_ANDROID_FEMALE_24_30 gibi)
# 4) Price ortalamalarina gore yeni bir SEGMENT sutunu olusturma (A,B,C,D segmentleri ile)
# 5) Yeni / potansiyel musteriler icin segment belirleme ve gelir tahminlemesi yapma




################# Uygulama Öncesi DataFrame #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17


################# Uygulama Sonrası DataFrame #####################

#         CUSTOMERS_LEVEL_BASED  PRICE SEGMENT
# 280     FRA_ANDROID_MALE_0_18  30.25       D
# 329      FRA_IOS_FEMALE_24_30  25.00       D
# 175      TUR_IOS_FEMALE_19_23  34.00       C
# 18   TUR_ANDROID_FEMALE_31_40  43.00       A
# 263    BRA_ANDROID_MALE_19_23  31.00       D





#############################################
# PROJE ADIMLARI
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

# import the libraries
import pandas as pd
import seaborn as sns

# Code ciktisi ayarlari
pd.set_option("display.max_columns", None)  # tum sutunlar gosterilsin
pd.set_option("display.width", 500)         # tum sutunlar yanyana gelsin
pd.set_option("display.precision", 2)       # loat degerler virgul sonrasi 2 basamakli gelsin


# read the csv file
df = pd.read_csv("/Users/gozdemadendere/Desktop/PycharmProjects/Python_Programming_Project/datasets/persona.csv")
# Projects altinda ilgili dosya uzerine gel, sag tikla, Copy Path e tikla, Path From.. tikla, 2 tirnak arasina gel, yapistir


# Functional Data Exploration
def explore_dataframe(dataframe, head=5):
    print("###################### First 5 Rows ######################")
    print(dataframe.head(head))
    print("###################### Last 5 Rows ######################")
    print(dataframe.tail(head))
    print("###################### Shape: Rows x Columns ######################")
    print(dataframe.shape)
    print("###################### General Info ######################")
    print(dataframe.info())
    print("###################### Null Values ######################")
    print(dataframe.isnull().sum().sort_values(ascending=False))
    print("###################### Statistical Info ######################")
    print(dataframe.describe().T)

explore_dataframe(df)


df.sample(5)

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

df["SOURCE"].unique()           # ['android', 'ios']

df["SOURCE"].nunique()          # 2 adet unique SOURCE vardır

df["SOURCE"].value_counts()     # android    2974,  ios        2026




# Soru 3: Kaç unique PRICE vardır?

df["PRICE"].unique()     # [39, 49, 29, 19, 59,  9]

df["PRICE"].nunique()    # 6 adet unique PRICE vardır





# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df["PRICE"].value_counts()

# or
df.groupby("PRICE").agg({"PRICE": "count"})




# Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df["COUNTRY"].value_counts()

# or
df.groupby("COUNTRY").agg({"COUNTRY": "count"})





# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("COUNTRY").agg({"PRICE": "sum"})

# ordering
df.groupby("COUNTRY").agg({"PRICE": "sum"}).sort_values(by="PRICE", ascending=False)






# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?

df["SOURCE"].value_counts()

# or
df.groupby("SOURCE").agg({"SOURCE": "count"})





# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby("COUNTRY").agg({"PRICE": "mean"})

# ordering
df.groupby("COUNTRY").agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)





# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("SOURCE").agg({"PRICE": "mean"})





# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})




#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})





#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)





#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()


agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False).reset_index()

# or
agg_df.reset_index(inplace=True)






#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################

# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'


# dtype görme
agg_df["AGE"].dtype   # int64


# dtype degistirme
agg_df["AGE"] = agg_df["AGE"].astype("category")

# tekrar dtype görme
agg_df["AGE"].dtype   # CategoricalDtype


# yeni degisken / sutun olusturma : apply lambda ile
agg_df["AGE_CAT"] = agg_df["AGE"].apply(lambda x: '0_18' if x <= 18 else ('19_23' if x <= 23
                                                                          else ('24_30' if x <= 30
                                                                                else ('31_40' if x <= 40
                                                                                      else '41_70'))))




# veya pd.cut() ile
agg_df["AGE_CAT"] = pd.cut(x=agg_df["AGE"], bins=[0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"])



# check the DataFrame
agg_df.sample(10)






#############################################
# GÖREV 6: Yeni level based müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################

# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18. Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

# customers_level_based sütununu oluşturma
agg_df["customers_level_based"] = agg_df["COUNTRY"] + "_" + agg_df["SOURCE"] + "_" + agg_df["SEX"] + "_" + agg_df["AGE_CAT"]

# sutundaki degerleri buyuk harfe cevirme  !!!!!
agg_df["customers_level_based"] = agg_df["customers_level_based"].str.upper()

# sutun ismini buyuk harfe cevirme         !!!!!
agg_df = agg_df.rename(columns={"customers_level_based": "CUSTOMERS_LEVEL_BASED"})

# sadece "customers_level_based" ve "PRICE" sutunlarini filtreleme
agg_df.loc[:, ["CUSTOMERS_LEVEL_BASED", "PRICE"]]

# customers_level_based degerlerini tekillestirme, yani groupby'a alma, ve price ortalamalarini gorme
agg_df.groupby("CUSTOMERS_LEVEL_BASED").agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)








#############################################
# GÖREV 7: Müşterileri CUSTOMERS_LEVEL_BASED sutununu baz alarak, PRICE’a göre 4 segmente ayırınız.
#############################################

# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre groupby yapıp price mean, max, min, sum’larını gosteriniz).

# Yeni bir Segment sutunu olustur, Price i 4 esit parcaya bolerek 4 farkli Segment olustur
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], q=4, labels=["D", "C", "B", "A"])
agg_df.sample(10)

agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "sum", "min", "max", "count"]})


# sadece "CUSTOMERS_LEVEL_BASED" ve "PRICE" sutunlarini filtreleme
agg_df.loc[:, ["CUSTOMERS_LEVEL_BASED", "PRICE", "SEGMENT"]].sample(5)





#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################


# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

# Bu kullaniciyi tanimlayalim
new_user = "TUR_ANDROID_FEMALE_31_40"

# Bu kullanici level i icin genel ozellikleri gorelim
agg_df.loc[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user ,:]    # A segmentine ait

# Bu kullanici level i icin Price ortalamasini gorelim
agg_df.loc[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user ,:].agg({"PRICE": "mean"})      # 41.833333




# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

# Bu kullaniciyi tanimlayalim
new_user2 = "FRA_IOS_FEMALE_31_40"

# Bu kullanici level i icin, genel ozellikleri gorelim
agg_df.loc[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user2, :]    # C segmentine ait

# Bu kullanici level i icin, Price ortalamasini gorelim
agg_df.loc[agg_df["CUSTOMERS_LEVEL_BASED"] == new_user2, :].agg({"PRICE": "mean"})     # 32.818182

