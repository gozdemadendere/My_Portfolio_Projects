
###################################################
# PROJE: Rating Products & Sorting Reviews on AMAZON
###################################################

## PROJE ADIMLARI ##
# 1. İş Problemi                        (Business Problem)
# 2. Veriyi Anlama                      (Data Understanding)
# 3. Ürünlerin puanlarının hesaplanması (Rating Products)
# 4. Müşteri yorumlarının sıralanması   (Sorting Reviews)




###################################################
# 1. İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden biri, "ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır". (Rating Products)
# Bu problemin çözümü daha fazla müşteri memnuniyeti sağlar, satıcılar için ürünün öne çıkmasını ve satın alanlar için de sorunsuz bir alışveriş deneyimini sağlar.

# Bir diğer problem ise "ürünlere verilen yorumların doğru bir şekilde sıralanmasıdır". (Sorting Reviews)
# Yanıltıcı yorumların öne çıkması, ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi hem de müşteri kaybına neden olacaktır.
# Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken, müşteriler ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.


## Veri Seti Hikayesi
# Amazon ürün verilerini içeren bu veri seti, ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID:       Kullanıcı ID’si
# asin:             Ürün ID’si
# reviewerName:     Kullanıcı Adı
# helpful:          Faydalı değerlendirme derecesi (up ratings)
# reviewText:       Değerlendirme
# overall:          Ürün rating’i
# summary:          Değerlendirme özeti
# unixReviewTime:   Değerlendirme zamanı
# reviewTime:       Değerlendirme zamanı Raw
# day_diff:         Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes:      Değerlendirmenin faydalı bulunma sayısı
# total_vote:       Değerlendirmeye verilen oy sayısı





###################################################
# 2. Veriyi Anlama (Data Understanding)
###################################################

# import the libraries
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option("display.max_columns", None)  # DataFrame'in gösterilecek maksimum sütun sayısı (None ise tüm sütunlar gelir)
pd.set_option("display.max_rows", 100)      # DataFrame'in gösterilecek maksimum satır sayısı
pd.set_option('display.width', 500)         # Çıktının yanyana gelmesi için genişlik ayarlar.
pd.set_option("display.precision", 2)       # Float türündeki sayıların gösterilecek ondalık basamak sayısını belirler.
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv("Amazon_Project_Rating_Products_Sorting_Reviews/amazon_review.csv")


#############################
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

#############################






###################################################
# 3) Rating Products (Ürünlerin puanlarının hesaplanması)
###################################################

####################
# 1. Average
####################

# Average Rating'i Güncel Yorumlara Göre Hesaplayınız. (Ürünün Ortalama Puanını Hesaplayınız.)
df["overall"].mean()   # 4.58



####################
# 2. Time-Based Weighted Average
####################

# Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
# Puan Zamanlarına Göre Ağırlıklı Ortalama: Yeni, başarılı ve trend olan ürünlerin öne çıkabilmesi için, zamansal bir şekilde ortalama alma yöntemidir.

# Bugüne ait tarihi girelim
df["reviewTime"].max()  # son tarih: ('2014-12-07 00:00:00')
current_date = pd.to_datetime('2014-12-08 00:00:00')

# reviewTime değişkenini, tarihsel data type a çevirelim
df["reviewTime"] = pd.to_datetime(df["reviewTime"])

# days sütunu oluşturalım : current_date den, her puanlamaya ait tarihi çıkaralım ve gün cinsine çevirelim
df["days"] = (current_date - df["reviewTime"]).dt.days



# Bazı pratikler yapalım:
# Verisetindeki son 30 günde yapılan puanlamalar ortalaması:
df.loc[df["days"] <= 30, "overall"].mean()                           # 4.74242

# Verisetindeki son 1 ay-3 ay arası yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean()     # 4.80314

# Verisetindeki son 3 ay-6 ay arası yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean()    # 4.64948

# Verisetindeki 6 aydan daha eski yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 180), "overall"].mean()                         # 4.57337



## Puanlama Zamanlarına Göre Ağırlıklı Puan Ortalaması Hesaplama Fonksiyonu
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "overall"].mean() * w4 / 100

# Tarihe göre Ağırlıklı Puan Ortalaması:
time_based_weighted_average(df)   # 4.69

# Yorum: Tarihe göre Ağırlıklı Puan Ortalaması: 4.69 iken, Dataframe e ait genel puanlama ortalaması 4.58 idi.




## Görev: Ağırlıklandırılmış puanlamada her bir zaman diliminin ortalamasını karşılaştırıp yorumlayınız.

# Verisetindeki son 30 günde yapılan puanlamalar ortalaması:
df.loc[df["days"] <= 30, "overall"].mean()                           # 4.74242

# Verisetindeki son 1 ay-3 ay arası yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean()     # 4.80314

# Verisetindeki son 3 ay-6 ay arası yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean()    # 4.64948

# Verisetindeki 6 aydan daha eski yapılan puanlamalar ortalaması:
df.loc[(df["days"] > 180), "overall"].mean()                         # 4.57337

# Yorum: Güncel olarak yapılan puanlamalar daha yüksek. Eski puanlamalar daha düşük. Zamanla gelen puan ort. artışı, "ürünün popülerliğinde veya kullanıcı memnuniyetinde" hafif bir artma olduğunu gösterebilir.

# Son 30 Gün: Ort. puanlama 4.74'tür. Kullanıcılar son dönemde üründen memnun olmuş olabilirler. Veya "ürünün belirli bir özelliği dikkat çekmiş veya tanıtımı yapılmış" olabilir.
# Son 30 Günden Eski 3 Aydan Yeni: Ort. puanlama 4.80'dir. Son 30 gün içindeki puanlamalardan bir miktar daha yüksek görünmektedir.
# Son 3 Aydan Eski - 6 Aydan Yeni: Ortalama puanlama 4.64'tür. Bu dönemdeki puanlama biraz daha düşüktür, ancak yine yüksektir.







###################################################
# 4. Sorting Reviews (Müşteri yorumlarının sıralanması)
###################################################
# Yorumun veya ürünün düşük/yüksek puanlı olmasıyla ilgilenmiyoruz. Kullanıcıya, en faydalı sonucu ulaştırmaya çalışıyoruz.

## Görev: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.


## Adım 1. helpful_no Değişkenini Üretiniz

# total_vote değişkeni:  Bir yoruma verilen toplam up ratings-down ratings sayısıdır. up, helpful demektir.
# helpful_yes değişkeni: Yararlı oy sayısı. (up ratings)

# helpful_no değişkenini üretelim: (hem up hem down ratings lere ihtiyacımız var, elimizde sadece helpful_yes yani up ratings var)
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]



## Adım 2. Şu Skorları Hesaplayıp Veriye Ekleyiniz:
###################################################
# 1) Up-Down Difference Score = (up ratings) − (down ratings)
# 2) Average rating Score = (up ratings) / (all ratings)
# 3) Wilson Lower Bound Score
###################################################


###########
# 1) Up-Down Difference Score = (up ratings) − (down ratings)
###########
# Yorumlardaki beğeni sayısına göre sıralama yapar.

def score_up_down_diff(helpful_yes, helpful_no):
    return helpful_yes - helpful_no

# Üstte oluşturduğumuz fonksiyonu uygulatarak, Dataframe de yeni bir sütun oluşturalım.
df["score_pos_neg_diff"] = df.apply(lambda x: score_up_down_diff(x["helpful_yes"], x["helpful_no"]), axis=1)




###########
# 2) Average rating Score = (up ratings) / (all ratings)
###########

def score_average_rating(helpful_yes, helpful_no):
    if helpful_yes + helpful_no == 0:
        return 0
    return helpful_yes / (helpful_yes + helpful_no)

# Üstte oluşturduğumuz fonksiyonu uygulatarak, Dataframe de yeni bir sütun oluşturalım.
df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)




###########
# 3) Wilson Lower Bound Score
###########

# WLB Skoru, ürün veya yorum sıralamalarında kullanılan istatistiksel bir yöntemdir.
# Yoruma ait puanı ve yorum yapan "müşterinin yorum sayısını da dikkate alarak" sıralama yapar. Müşterinin yorum sayısı, yorumun ne kadar güvenilir olduğunu belirtir. !
# Wilson Lower Bound yöntemi, yorumların güvenilirliği ve puanların istatistiksel olarak anlamlı olup olmadığını değerlendirmek için Bayes Teoremi matematiksel formülünden faydalanır.


def wilson_lower_bound(helpful_yes, helpful_no, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = helpful_yes + helpful_no
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * helpful_yes / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


# Üstte oluşturduğumuz fonksiyonu uygulatarak, Dataframe de yeni bir sütun oluşturalım.
df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)






## Adım 3. 20 Yorumu Belirleyiniz.

top_20_reviews = df.sort_values(by="wilson_lower_bound", ascending=False).head(20)

# Yorum:
# Müşteriler için daha faydalı olabilecek yorumları en üste çıkardık. Yorumun pozitif veya negatif olması bunu etkilemedi. Örnek:
# 1. ve 2. yorumdaki müşteriler, ürünün performansı hakkında olumlu bilgiler sunmuşlar ve 5 puan vermişlerdir.
# 3. ve 4. yorumdaki müşteriler, ürünün belirli sorunları veya dezavantajları olduğunu belirtmiş ve 1 puan vermişlerdir.



