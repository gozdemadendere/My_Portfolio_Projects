#####################################################
# A/B Testing - Bidding (Teklif Verme) Yöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

# Hipotez testi: Bir inanışı/bir savı test etmek için kullanılan bir istatistiksel analiz yöntemidir.
# A/B Testing:   2 grup arasında bir değişikliğin etkisini ölçmek veya 2 gruba ait ortalama / oran karşılaştırması için kullanılır.
# Grup karşılaştırmalarında temel amaç, olası farklılıkların şans eseri ortaya çıkıp çıkmadığını test etmektir.


## PROJE ADIMLARI ##
# 1. İş Problemi     (Business Problem)
# 2. Veriyi Anlama & Hazırlama   (Data Understanding & Preparing)
# 3. A/B Testing     (Bağımsız İki Örneklem T Testi / Independent Two-Sample T-Test)




#####################################################
# 1. İş Problemi (Business Problem)
#####################################################

# Facebook kısa bir süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan "average bidding"’i tanıttı.
# Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximumbidding'den daha fazla dönüşüm getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.
# A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.
# Bombabomba.com için nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.


# Veri Seti Hikayesi
# Firmanın web site bilgilerini içeren bu veri setinde, kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra, buradan gelen kazanç bilgileri yer almaktadır.
# Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır. Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.
# Bu veri setleri AB_Testing.xlsx excel’inin ayrı sayfalarında yer almaktadır.


# Impression:  Reklam görüntüleme sayısı
# Click:       Görüntülenen reklama tıklama sayısı
# Purchase:    Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning:     Satın alınan ürünler sonrası elde edilen kazanç


# Amaç:
# Maximum Bidding ve Average Bidding için, satın alma (purchase) ortalamaları arasında karşılaştırma yapacağız. Bağımsız İki Örneklem T Testi kullanacağız.
# A/B Testing (Bağımsız İki Örneklem T Testi) : 2 grup ortalaması arasında karşılaştırma yapmak için kullanılır.




#####################################################
# 2. Veriyi Anlama & Hazırlama   (Data Understanding & Preparing)
#####################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal, chi2_contingency
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option("display.width", 500)
pd.set_option("display.precision", 2)
# pd.set_option('display.float_format', lambda x: '%.5f' % x)


# Excel'de var olan sheet name leri görelim:
file_path  = pd.ExcelFile("AB_Testing_Project_Two_Sample_T_Test/AB_Testing.xlsx")
sheet_names = file_path.sheet_names
print("Sheet Names in the Excel File:", sheet_names)    # 'Control Group', 'Test Group'





#####################################################
# 3. A/B Testing
#####################################################

# A/B Testing Adımları:

# 1) Hipotezlerin Tanımlanması
# 2) Varsayım Kontrolü
#   - Normallik Varsayımı
#   - Varyans Homojenliği Varsayımı
# 3) Hipotezlerin Test Edilmesi
#   - Varsayımlar sağlanıyorsa  : Bağımsız iki örneklem t testi (parametrik test)
#   - Varsayımlar sağlanmıyorsa : Mann-Whitney U testi (non-parametrik test)
# 4) Sonuçların p-value değerine göre yorumlanması (p < 0.05 ise H0 red)


# Notlar:
# Normallik Varsayımı hem kontrol grubu, hem de test grubu için sağlanmalıdır.
# Normallik Varsayımı sağlanmıyorsa, direkt mannwhitneyu testini uygularız. Sadece Varyans Homojenliği sağlanmıyorsa, iki örneklem t testi uygulanır ama argüman girilir (equal_var=True).
# Argüman girişi şu şekilde: test_stat, pvalue = ttest_ind(df_control['Purchase'], df_test['Purchase'], equal_var=True)
# Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




## Görev: Veriyi Hazırlama ve Analiz Etme

# AB_Testing.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

# Excel'de var olan sheet name leri görelim:
file_path  = pd.ExcelFile("AB_Testing_Project_Two_Sample_T_Test/AB_Testing.xlsx")
sheet_names = file_path.sheet_names
print("Sheet Names in the Excel File:", sheet_names)   # 'Control Group', 'Test Group'

# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
df_control = pd.read_excel("AB_Testing_Project_Two_Sample_T_Test/AB_Testing.xlsx", sheet_name='Control Group')
df_test = pd.read_excel("AB_Testing_Project_Two_Sample_T_Test/AB_Testing.xlsx", sheet_name='Test Group')

df_control.head()  # Kontrol grubuna Maximum Bidding değerleri atanmıştır.
df_test.head()     # Test grubuna Average Bidding değerleri atanmıştır.



# Kontrol ve test grubu verilerini analiz ediniz.

# Kontrol grubu (Maximum Bidding)
df_control.describe().T

# Test grubu (Average Bidding)
df_test.describe().T

# Yorum: Test grubu (Average Bidding) için Purchase değerleri daha yüksek görünüyor. (Nihai başarı ölçütü Purchase değerlerinin iyi olmasıydı.)



# Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

# Kontrol ve Test grubu dataframe lerine bir grup sütunu ekleyelim
df_control["Group"] = "control"
df_test["Group"] = "test"

df = pd.concat([df_control, df_test])
df




############################
# 1) Hipotezlerin Tanımlanması
############################


# H0: M1 = M2   : Kontrol grubu (Maximum Bidding) ve Test grubu (Average Bidding) satın alma (purchase) ortalamaları arasında, İstatistiksel Olarak Anlamlı bir Fark yoktur.
#                 (Yani, bu iki teklif stratejisi arasında belirgin bir performans farkı gözlemlenmemiştir.)

# H1: M1 != M2  : Kontrol grubu ve Test grubu satın alma (purchase) ortalamaları arasında, İstatistiksel Olarak Anlamlı bir Fark vardır.
#                 (Yani, bu iki teklif stratejisi arasında belirgin bir performans farkı vardır.)


# Kontrol ve test grubu için purchase(satın alma) ortalamalarını analiz ediniz.
df.groupby("Group").agg({"Purchase": "mean"})

#          Purchase
# Group
# control 550.89406
# test    582.10610

# Yorum: Test grubu (Average Bidding) için ortalama Purchase değeri daha yüksek görünüyor.




############################
# 2) Varsayım Kontrolü
#   - Normallik Varsayımı            (shapiro testi)
#   - Varyans Homojenliği Varsayımı  (levene testi)
############################

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını "Purchase" değişkeni üzerinden ayrı ayrı test ediniz.

# Normallik Varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.   (incelenen veri seti normal dağılıma uygundur.)
# H1: Normal dağılım varsayımı sağlanmamaktadır.

# shapiro testi, bir değişkenin dağılımının normal olup olmadığını test eder.
test_stat, pvalue = shapiro(df.loc[df["Group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.5891  !< 0.05 HO Reddedilemez  (H0: Normal dağılım varsayımı sağlanmaktadır.)

test_stat, pvalue = shapiro(df.loc[df["Group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.1541  !< 0.05 HO Reddedilemez  (H0: Normal dağılım varsayımı sağlanmaktadır.)

# Yorum: Kontrol ve Test grubu için p-value !< 0.05 oldugu icin, HO Reddedilemez. Yani, Normal dağılım varsayımı sağlanmaktadır. (Normallik varsayımı şartı hem kontrol hem de test grubu için sağlanmalıdır.)




# Varyans Homojenliği Varsayımı
# H0: Varyanslar Homojendir.
# H1: Varyanslar Homojen Değildir.

# levene testi, varyans homojenliğini test etmek için kullanılır.
test_stat, pvalue = levene(df.loc[df["Group"] == "control", "Purchase"],
                           df.loc[df["Group"] == "test", "Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.1083  !< 0.05 HO Reddedilemez  (H0: Varyanslar Homojendir.)

# Yorum: Kontrol ve Test grubu için p-value !< 0.05 oldugu icin, HO Reddedilemez. Yani, Varyanslar Homojendir.




############################
# 3) Hipotezlerin Test Edilmesi
#   - Varsayımlar sağlanıyorsa  : Bağımsız iki örneklem t testi (parametrik test)
#   - Varsayımlar sağlanmıyorsa : Mann-Whitney U testi (non-parametrik test)
############################

# Hem Normallik varsayımı hem de Varyans homojenliği varsayımı sağlandı : Bağımsız iki örneklem t testi uygulayalım (parametrik test)

test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "control", "Purchase"],
                           df.loc[df["Group"] == "test", "Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


alpha = 0.05
if pvalue > alpha:
    print("The p-value is larger than alpha. We can not reject the Null Hypothesis.")
else:
    print("The p-value is smaller than alpha. We can reject the Alternative Hypothesis.")



############################
# 4) Sonuçların p-value değerine göre yorumlanması (p < 0.05 ise H0 red)
############################

# p-value = 0.3493 p !< 0.05 , yani H0 Reddedilemez.

# H0: M1 = M2   : Kontrol grubu (Maximum Bidding) ve Test grubu (Average Bidding) satın alma (purchase) ortalamaları arasında, İstatistiksel Olarak Anlamlı bir Fark yoktur.
#                 (Yani, bu iki teklif stratejisi arasında belirgin bir performans farkı gözlemlenmemiştir.)





##############################################################
# Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
# Cevap: A/B Testing icin bağımsız iki örneklem t testi uyguladık. (parametrik test)

# Bu testin uygulanması için 2 ön koşul da sağlandı:
# 1) Normallik Varsayımı: Her iki grup için de verilerin normal dağılıma sahip olduğu varsayılır.
# 2) Varyans Homojenliği Varsayımı: Grupların varyanslarının homojen olduğu (eşit varyansa sahip olduğu) varsayılır. Yani, gruplar arasında veri dağılımının aynı olduğu varsayılır.



# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# Sonuç olarak, H0 hipotezini reddedemeyiz:
# H0: M1 = M2   : Kontrol grubu (Maximum Bidding) ve Test grubu (Average Bidding) satın alma (purchase) ortalamaları arasında, İstatistiksel Olarak Anlamlı bir Fark yoktur.
# Yani, Maximum Bidding ve Average Bidding teklif stratejileri arasında belirgin bir performans farkı gözlemlenmemiştir. Bu test sonucuna göre, müşterinin bir teklif verme yöntemini diğerine tercih etmesi için bir neden yoktur.

## Öneriler:
# A/B Testing sadece 80 gözlem için gerçekleştirildi. Bu gözlem sayısı arttırılabilir, farklı gruplar üzerinde de test işlemi devam ettirilebilir.
# Diğer faktörler de dikkate alınarak daha kapsamlı bir analiz yapılabilir:
# Earning metriği de incelenebilir ve farklı teklif stratejilerinin gelir üzerindeki etkisi değerlendirilebilir.
# Impression (reklam görüntüleme sayısı): Bu metrik üzerinde ek bir analizle, 2 teklif stratejisinin reklam performansı üzerindeki etkisi değerlendirilebilir.
# Segmentasyon Analizi:  Örneğin, Purchase metriğini kullanarak her bir segmentin teklif stratejilerine tepkisi değerlendirilebilir.



