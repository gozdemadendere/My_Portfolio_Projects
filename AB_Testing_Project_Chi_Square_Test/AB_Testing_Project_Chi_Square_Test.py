#####################################################
# A/B Testing - Montana State University Kütüphanesi Websitesi Buton Performanslarının Karşılaştırılması
#####################################################

# Hipotez testi: Bir inanışı/bir savı test etmek için kullanılan bir istatistiksel analiz yöntemidir.
# A/B Testing:   2 grup arasında bir değişikliğin etkisini ölçmek veya 2 gruba ait ortalama / oran karşılaştırması için kullanılır.
# Grup karşılaştırmalarında temel amaç, olası farklılıkların şans eseri ortaya çıkıp çıkmadığını test etmektir.


## PROJE ADIMLARI ##
# 1. İş Problemi     (Business Problem)
# 2. Veriyi Anlama & Hazırlama   (Data Understanding & Preparing)
# 3. A/B Testing     (Ki-Kare Testi / Chi-square Test)




#####################################################
# 1. İş Problemi (Business Problem)
#####################################################

# Montana State University Kütüphanesi, öğrencilerin kitap ve makale bulmak için kullandığı bir web sitesine sahiptir.
# Ana sayfada, kütüphane resminin altında, bir arama çubuğu ve “Find”, “Request”, “Interact” (Bul, Talep Et, Etkileşim) olmak üzere 3 büyük öğe/buton bulunmaktadır.
# Bu butonlar, kütüphane hakkında önemli bilgilere ve hizmetlere erişim sağlar.


# Ancak, Web Analizi, "Interact" (Etkileşim) butonunun, ironik bir şekilde, neredeyse hiç etkileşimi olmadığını göstermektedir.
# 3 kategorinin her birinin performansını ölçmenin yolu, tıklama oranı (click-through rate = CTR) ile yapılır.
# Bu çevrimiçi pazarlamada yaygın bir terimdir ve genellikle bir reklamın görüntülendiği sayıya bölünen tıklama sayısını açıklar.


# Bu projenin temel amacı, Montana State University web sitesindeki "Interact" butonundaki farklı metinlerin CTR'sini (tıklama oranı) test etmek için bir A/B Testi gerçekleştirmektir.
# Web sitesi ekibi, "Interact" (Etkileşim) butonuna karşı test etmek için 4 farklı yeni sürüm/metin belirledi: Connect, Learn, Help, Services.


# İzlenecek metrikler şunlardır:
# Ana sayfadaki tıklama oranı (Click-through rate = CTR): Butondaki tıklama sayısının sayfa ziyaretlerinin toplamına bölünmesi. Kullanıcıları çekmek için kategori başlığının başlangıç yeteneğinin bir ölçüsü olarak seçildi.
# Kategori sayfaları için terk oranı (Drop-off rate):     Belirli bir sayfadan siteyi terk eden ziyaretçilerin yüzdesi, kategori sayfasının kullanıcı beklentilerini karşılama yeteneğinin bir ölçüsü olarak seçildi.
# Ana sayfaya dönüş oranı (Homepage-return rate ):        Kütüphane ana sayfasından kategori sayfasına geçen ve ardından ana sayfaya geri dönen kullanıcıların yüzdesi. Kategori sayfasının kullanıcı beklentilerini karşılama yeteneği olarak seçildi.





#####################################################
# 2. Veriyi Anlama & Hazırlama   (Data Understanding & Preparing)
#####################################################

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option("display.width", 500)
pd.set_option("display.precision", 4)


# import data
interact = pd.read_csv("AB_Testing_Project_Chi_Square_Test/Data/Interact - Element list Homepage Version 1, 5-29-2013.csv")
help = pd.read_csv("AB_Testing_Project_Chi_Square_Test/Data/Help - Element list Homepage Version 4 , 5-29-2013.csv")
connect = pd.read_csv("AB_Testing_Project_Chi_Square_Test/Data/Connect - Element list Homepage Version 2, 5-29-2013.csv")
learn = pd.read_csv("AB_Testing_Project_Chi_Square_Test/Data/Learn - Element list Homepage Version 3 , 5-29-2013.csv")
services = pd.read_csv("AB_Testing_Project_Chi_Square_Test/Data/Services - Element list Homepage Version 5 , 5-29-2013.csv")

interact.head()
help.head()
connect.head()
learn.head()
services.head(50)


# Veriyi Hazırlama

# Observed results
Click = [42, 38, 45, 53, 21]    # Her kategori için tıklanma sayıları, örnek: services butonu varken, services a tıklanma sayısı gibi.)
No_click = [10241, 3142, 2019, 2689, 2726] # Her kategori için tıklanmama sayıları, yani geri kalan tıklamalar)

# Create a dataframe
observed = pd.DataFrame([Click, No_click],
                        columns=["interact", "help", "services", "connect", "learn"],
                        index=["Click", "No_click"])

observed

observed_expanded = observed.copy()
observed_expanded


# Add the totals of each row
observed_expanded["Total"] = observed_expanded["interact"] + observed_expanded["help"] + observed_expanded["services"] + \
                             observed_expanded["connect"] + observed_expanded["learn"]

# Add the totals of each column
observed_expanded.loc["Total", :] = observed_expanded.sum()


# Combining all the versions in a dataframe
interact_clicks=interact.loc[[9]]
interact_clicks['visits'] = 10283
interact_clicks['total_clicks']=3714
interact_clicks

help_clicks=help.loc[[7]]
help_clicks['visits'] = 3180
help_clicks['total_clicks']=1717
help_clicks

services_clicks=services.loc[[7]]
services_clicks['visits'] = 2064
services_clicks['total_clicks']=1348
services_clicks

connect_clicks=connect.loc[[6]]
connect_clicks['visits'] = 2742
connect_clicks['total_clicks']=1587
connect_clicks

learn_clicks=learn.loc[[10]]
learn_clicks['visits'] = 2747
learn_clicks['total_clicks']=1652
learn_clicks

all_versions_clicks = pd.concat([interact_clicks,help_clicks,services_clicks,connect_clicks,learn_clicks])
all_versions_clicks

# We can find the CTR by dividing number of clicks values by visits
all_versions_clicks["CTR"] = (all_versions_clicks["No. clicks"] / all_versions_clicks["visits"]) * 100

all_versions_clicks.sort_values(by="CTR", ascending=False)



# Creating CTR Dataframe
CTR = [0.408441, 1.194969, 2.180233, 1.932896, 0.764470]
columns = ["interact", "help", "services", "connect", "learn"]

CTR_df = pd.DataFrame([CTR],
                           columns = [columns],
                           index = ["CTR"])

CTR_df

# For CTR:
# “Services” and “Connect” are the best performers.
# “Interact” and “Learn” are the worst performers,
#  services > connect > help > learn > interact

# Bu bize bazı sürümlerin diğerlerinden daha iyi (veya daha kötü) performans gösterdiğini söylüyor.
# En iyi sürümün (services) en kötü sürümden (interact) daha iyi performans gösterdiğinden emin olabiliriz.
# Ancak aralarındaki farkların istaistiksel olarak anlamlı olduğundan olduğundan emin olamayız, bunu test edeceğiz







#####################################################
# 3. A/B Testing     (Ki-Kare Testi / Chi-square Test)
#####################################################

# A/B Testing Adımları:

# 1) Hipotezlerin Tanımlanması
# 2) Hipotezlerin Test Edilmesi
# 3) Sonuçların p-value değerine göre yorumlanması (p < 0.05 ise H0 red)




### TEST 1 ###
############################
# 1) Hipotezlerin Tanımlanması
############################

# H0: CRT(interact) = CRT(help) = CRT(services) = CRT(connect) = CRT(learn)
# Buton versiyonları arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu buttnlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)

# H1: # Buton versiyonları arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark vardır.
# (Yani, bu butonlar arasında belirgin bir performans farkı vardır. Biri veya birileri daha iyi performans sergiilemiştir.)


############################
# 2) Hipotezlerin Test Edilmesi
############################

from scipy import stats
chisq, pvalue, df, expected = stats.chi2_contingency(observed, correction=False)

chisq  # 96.74

pvalue # 4.85

expected

df

alpha = 0.05
if pvalue > alpha:
    print("The p-value is larger than alpha. We can not reject the H0 Hypothesis")
else:
    print("The p-value is smaller than alpha. We reject the H0 Hypothesis")

# The p-value is smaller than alpha. We reject the H0 Hypothesis

# H0: CRT(interact) = CRT(help) = CRT(services) = CRT(connect) = CRT(learn)
# Buton versiyonları arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)





### TEST 2 ###
# H0 hipotezini reddettik, yani butonlar arasında bir performans farkı bulunuyor.
# Bunu çözmek için olası bir yaklaşım, adayları daraltmaktır: en kötü performansı göstereni eleyelim ve testi yeniden yapalım.
# Bu durumda “Interact”ı bırakacağız. (services > connect > help > learn > interact)

observed = observed.drop("interact", axis=1)
observed

############################
# 1) Hipotezlerin Tanımlanması
############################

# Null Hypothesis ( 𝐻0 ) : CRT(help) = CRT(services) = CRT(connect) = CRT(learn)
# 4 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)


# Alternative Hypothesis ( 𝐻𝐴 ) :
# 4 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark vardır.
# (Yani, bu butonlar arasında belirgin bir performans farkı vardır. )


############################
# 2) Hipotezlerin Test Edilmesi
############################

from scipy import stats
chisq, pvalue, df, expected = stats.chi2_contingency(observed, correction=False)

chisq  # 22.45

pvalue # 5.25

expected

df

alpha = 0.05
if pvalue > alpha:
    print("The p-value is larger than alpha. We can not reject the H0 Hypothesis")
else:
    print("The p-value is smaller than alpha. We reject the H0 Hypothesis")

# The p-value is smaller than alpha. We reject the H0 Hypothesis

# H0: CRT(interact) = CRT(help) = CRT(services) = CRT(connect) = CRT(learn)
# Buton versiyonları arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)







### TEST 3 ###
# H0 hipotezini reddettik, yani butonlar arasında bir performans farkı bulunuyor.
# Adayları daraltıyoruz: En kötü performans gösteren ikinci adayı eleyip testi yeniden yapıyoruz.
# Bu durumda Learn'ü bırakacağız. (services > connect > help > learn > interact)

observed = observed.drop("learn", axis=1)
observed

############################
# 1) Hipotezlerin Tanımlanması
############################

# Null Hypothesis ( 𝐻0 ) : CRT(help) = CRT(services) = CRT(connect)
# 3 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)


# Alternative Hypothesis ( 𝐻𝐴 ) :
# 3 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark vardır.
# (Yani, bu butonlar arasında belirgin bir performans farkı vardır. )


############################
# 2) Hipotezlerin Test Edilmesi
############################

from scipy import stats
chisq, pvalue, df, expected = stats.chi2_contingency(observed, correction=False)

chisq  # 8.57

pvalue # 0.013

expected

df

alpha = 0.05
if pvalue > alpha:
    print("The p-value is larger than alpha. We can not reject the H0 Hypothesis")
else:
    print("The p-value is smaller than alpha. We reject the H0 Hypothesis")

# The p-value is smaller than alpha. We reject the H0 Hypothesis

# H0: CRT(interact) = CRT(help) = CRT(services) = CRT(connect)
# Buton versiyonları arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)




### TEST 4 ###
# H0 hipotezini reddettik, yani butonlar arasında bir performans farkı bulunuyor.
# Adayları daraltıyoruz: En kötü performans gösteren üçüncü adayı eleyip testi yeniden yapıyoruz.
# Bu durumda help'i bırakacağız. (services > connect > help > learn > interact)

observed = observed.drop("help", axis=1)
observed

############################
# 1) Hipotezlerin Tanımlanması
############################

# Null Hypothesis ( 𝐻0 ) : CRT(services) = CRT(connect)
# 2 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)


# Alternative Hypothesis ( 𝐻𝐴 ) :
# 2 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark vardır.
# (Yani, bu butonlar arasında belirgin bir performans farkı vardır. )


############################
# 2) Hipotezlerin Test Edilmesi
############################

from scipy import stats
chisq, pvalue, df, expected = stats.chi2_contingency(observed, correction=False)

chisq  # 0.36

pvalue # .54

expected

df

alpha = 0.05
if pvalue > alpha:
    print("The p-value is larger than alpha. We can not reject the H0 Hypothesis")
else:
    print("The p-value is smaller than alpha. We reject the H0 Hypothesis")

# The p-value is larger than alpha. We can not reject the H0 Hypothesis

# H0: CRT(services) = CRT(connect)
# 2 buton versiyonu arasında dönüşüm açısından İstatistiksel Olarak Anlamlı bir Fark yoktur.
# (Yani, bu butonlar arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)


##############################################################
# Sonuçların Analizi
##############################################################

# Yapılan hipotez testleri sonucunda, Services ve Connect butonları, diğer 3 butona göre istatistiksel olarak anlamlı bir performans farkı göstermiştir.
# Ancak Services ve Connect butonları arasında dönüşüm açısından istatistiksel olarak anlamlı bir fark yoktur.
# (Yani, bu 2 buton arasında belirgin bir performans farkı gözlemlenmemiştir. Görülen farklılıklar tesadüften kaynaklanmaktadır.)

## Öneriler:
# Services ve Connect'in tıklanma oranı (click-through rate = CTR), diğer butonlara göre daha iyidir (ve Services butonunun tıklanma oranı daha yüksektir.).
# Ancak bu 2 sürümün de tıklama alma olasılığı eşit olup, gözlemlenen farklılıklar şans eseridir. Bundan sonra sadece bu iki versiyona odaklanabiliriz.

# Aşağıdaki sebeplerden dolayı kütüphanenin ana sayfasının değiştirilmesi ve tasarımın "Services" butonu ile kullanıma sunulması önemle tavsiye edilir:
# Services, tüm seçenekler arasında en iyi tıklama oranını (click-through rate = CTR) gösterir.
# Services sürümünde, Ana sayfaya dönüş oranı (Homepage-return rate) daha düşük olduğundan, istedikleri kullanıcılara bilgi verme konusunda daha iyidir.
# Öğrenciler Connect yerine Services sürümünü daha çok sevdiklerini belirtmişlerdir.
