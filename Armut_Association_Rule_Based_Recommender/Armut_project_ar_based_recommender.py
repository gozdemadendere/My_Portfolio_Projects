###################################################
# PROJE: Armut | Association Rule Based Ürün Tavsiye Sistemi (AR Based Recommender System)
###################################################

# Association Rule Based Recommender:  Birliktelik analizi ile, sık olarak birlikte alınan ürünlere göre öneriler sunulur. (Sepet analizi)
# ARL yöntemi, kullanıcıların puan verme alışkanlıklarına dayanmaz ve sadece ürünler arasındaki ilişkileri baz alır.
# Kullanıcı bilgilerine ihtiyaç yok SepetID x Ürün dataframe'ine ihtiyaç var.


# Apriori Algoritması: Sepet analizi yöntemidir. Ürün birlikteliklerini ortaya çıkarır. Büyük veri setlerinde birliktelik kurallarını tespit etmek içindir.
# Support(X, Y) = Frequence(X,Y) / bütün işlemler   (X ve Y'nin birlikte görülme olasılığı)
# Confidence(X,Y) = Frequence(X,Y) / Frequence(X)   (X satın alındığında Y'nin de satın alınma olasılığı)
# Lift = Support(X, Y) / Support(X) * Support(Y)    (X satın alındığında Y'nin satın alınma olasılığı lift kadar artar)



## PROJE ADIMLARI ##
# 1. İş Problemi                        (Business Problem)
# 2. Veriyi Anlama & Hazırlama          (Data Understanding)
# 3. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
# 4. Birliktelik Kurallarının Çıkarılması
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak





#########################
# 1. İş Problemi
#########################

# Türkiye’nin en büyük online hizmet platformu olan Armut, hizmet verenler ile hizmet almak isteyenleri buluşturmaktadır.
# Bilgisayarın veya akıllı telefonunun üzerinden birkaç dokunuşla temizlik, tadilat, nakliyat gibi hizmetlere kolayca ulaşılmasını sağlamaktadır.
# Hizmet alan kullanıcıları ve bu kullanıcıların almış oldukları servis ve kategorileri içeren veri setini kullanarak Association Rule Learning ile ürün tavsiye sistemi oluşturulmak istenmektedir.


# Veri seti müşterilerin aldıkları servislerden ve bu servislerin kategorilerinden oluşmaktadır. Alınan her hizmetin tarih ve saat bilgisini içermektedir.

# UserId:      Müşteri numarası
# CategoryId:  Anonimleştirilmiş kategorilerdir. (Örnek : Temizlik, nakliyat, tadilat kategorisi)
# ServiceId:   Her kategoriye ait anonimleştirilmiş servislerdir. (Örnek : Temizlik kategorisi altında koltuk yıkama servisi) (Örnek: CategoryId’si 7 ServiceId’si 4 olan hizmet petek temizliği iken CategoryId’si 2 ServiceId’si 4 olan hizmet mobilya montaj)
# CreateDate:  Hizmetin satın alındığı tarih






#########################
# 2. Veriyi Anlama & Hazırlama
#########################

# Adım 1: armut_data.csv dosyasınız okutunuz.

# !pip install mlxtend
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

pd.set_option('display.max_columns', None)              # DataFrame'in gösterilecek maksimum sütun sayısını belirler. (None ise tüm sütunlar gelir)
pd.set_option('display.width', 500)                     # Çıktının yanyana gelmesi için genişlik ayarlar.
pd.set_option("display.precision", 2)                   # Float türündeki sayıların gösterilecek ondalık basamak sayısını belirler.
pd.set_option('display.expand_frame_repr', False)       # Geniş Dataframe'lerin tamamını terminal penceresine sığdırmak için kullanılır.
pd.set_option("display.max_rows", 100)                  # DataFrame'in gösterilecek maksimum satır sayısını belirler.

# pip install openpyxl
df_ = pd.read_csv("Armut_Project_association_rule_based_recommender/armut_data.csv")    # Sorun olursa:  df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011", engine="openpyxl")
df = df_.copy()


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
    print(dataframe.describe([0, 0.05, 0.1, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T)

# Use the function
check_df(df)

################################################


# Adım 2: ServiceId her bir CategoryID özelinde farklı bir hizmeti temsil etmektedir. ServiceID ve CategoryID'yi "_" ile birleştirerek hizmetleri temsil edecek yeni bir değişken oluşturunuz.

# String olarak birleştirme için, ServiceID ve CategoryID veri tiplerini string e çevirelim
df["Hizmet"] = df["ServiceId"].astype(str) + "_" + df["CategoryId"].astype(str)

# Adım 3: Association Rule Learning uygulayabilmek için bir sepet (fatura vb.) tanımı gerekmektedir. Burada sepet tanımı, her bir müşterinin bir ay içinde aldığı tüm hizmetlerdir.
# Örneğin; 2017'in 8.ayında alınan 9_4, 46_4 hizmetler bir sepeti, 2017’in 10.ayında alınan 9_4, 38_4  hizmetler başka bir sepeti ifade etmektedir.
# Sepetlerin unique bir ID ile tanımlanması gerekmektedir. Bunun için sadece yıl ve ay içeren yeni bir date değişkeni oluşturunuz. UserID ve yeni date değişkenini "_" ile birleştirirek ID adında yeni bir değişkene atayınız.

# Tarihsel işlemler için, CreateDate değişkenini tarihsel date type a çevirelim
df["CreateDate"] = pd.to_datetime(df["CreateDate"])

# Extract Year:  df['year'] = df['date'].dt.year      Extract Month:  df['month'] = df['date'].dt.month
# Yıl ve Ay'ı çıkarıp, string e çevirip, birleştirelim ve New_Date değişkeni oluşturalım
df["New_Date"] = (df["CreateDate"].dt.year).astype(str) + "-" + df["CreateDate"].dt.month.astype(str)

df["SepetID"] = df["UserId"].astype(str) + "_" + df["New_Date"].astype(str)






############################################
# 3. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
############################################

# Aşağıdaki gibi SepetID-Hizmet pivot table’i oluşturunuz. (Invoice-Product Matrix => burada SepetID-Hizmet Matrix)
# Nihai olarak varmak istediğimiz dataframe: (satırlarda invoice/transaction/sepetler, sütunlarda ürünler olacak, değerler True veya False olacak)

# Description/Hizmet     Urun1  Urun2  Urun3  Urun4  Urun5
# SepetID/InvoiceID
# 0_2017-08              False  False  False  False  False
# 0_2017-09              False  False  True   False  False
# 0_2018-01              False  False  False  True   False


# SepetID ve Hizmet'e göre gruplayalım  (SepetID ve Hizmet değerleri satırlarda yanyana gelecek)
df.groupby(['SepetID', 'Hizmet'])['Hizmet'].count()

# unstack ile pivot yaparız, yani 'SepetID' değerleri satırlara, 'Hizmet' değerleri ise sütunlara yerleştirilir
df.groupby(['SepetID', 'Hizmet'])['Hizmet'].count().unstack()

# notnull() ile: Bir hücrede değer True ise, o sepet için o hizmetin alındığını gösterir; aksi takdirde False olur.
invoice_product_df = df.groupby(['SepetID', 'Hizmet'])['Hizmet'].count().unstack().notnull()




#########################
# 4. Birliktelik Kurallarının Çıkarılması
#########################

# Bu kod, verilen dataframe üzerinde Apriori algoritmasını kullanarak sık öğe kümelerini (frequent itemsets) bulur.
frequent_itemsets = apriori(invoice_product_df,
                            min_support=0.01,  # min_support parametresi, sık öğe kümeleri oluştururken kullanılacak destek eşiğini belirler.
                            use_colnames=True) # use_colnames parametresi, öğelerin gerçek adlarını kullanıp kullanmama seçeneğini belirtir.


# Bu kod, birliktelik kurallarını çıkarmak için mlxtend kütüphanesindeki association_rules fonksiyonunu ve yukarıda oluşturduğumuz frequent_itemsets i kullanır.
rules = association_rules(frequent_itemsets,    # Sık öğe kümelerini içeren bir DataFrame.
                          metric="support",     # Burada "support" metriği seçilmiştir, yani destek değerine göre birliktelik kuralları oluşturulur.
                          min_threshold=0.01)   # Destek değeri için minimum eşik değeri 0.01 olarak belirlenmiştir.


# Sonuç dataframe inde her satır, bir kuralı temsil eder ve bu kuralda iki bileşen bulunur: antecedents (önceden koşul, X) ve consequents (sonuç, Y).
rules.head()





############################################
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak
############################################


# Bu fonksiyon, bir ürün ID'si verildiğinde, bu ürünle "en yüksek lift değerine" sahip ilişki kurallarını bulur ve bu kuralların consequents (sonuç) kısmındaki ürünleri öneri listesine ekler.
# Daha sonra bu öneri listesini, belirtilen sayıda öneri ile sınırlayarak döndürür.
def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)   # Yüksek lift değeri, iki ürünün birlikte satın alınma eğiliminin yüksek olduğunu gösterir. confidence'e göre de sıralanabilir insiyatife baglıdır.
    recommendation_list = []                                       # Tavsiye edilecek ürünler için boş bir liste oluşturuyoruz.

    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]


# En son 2_0 hizmetini alan bir kullanıcıya hizmet önerisinde bulununuz.
arl_recommender(rules, "2_0", 5)




