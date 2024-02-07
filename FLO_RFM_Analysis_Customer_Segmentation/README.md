## FLO | RFM Analizi ile Müşteri Segmentasyonu  (Customer Segmentation with RFM Analysis)

RFM analizi; Recency, Frequency, Monetary metriklerinden faydalanarak, müşteri segmentasyonu için kullanılan bir tekniktir.

Müşterilerin satın alma alışkanlıkları üzerinden segmentlere ayrılmasını, ve bu segmentler özelinde stratejiler geliştirilmesini sağlar.

- Recency   = Analiz tarihi - Müşterinin son satın alma tarihi
- Frequency = Müşterinin toplam satın alma sayısı   (toplam işlem veya fatura sayısı)
- Monetary  = Müşterinin TOPLAM Harcama tutarı

______________________________


### 1. İŞ PROBLEMİ / PROJE HEDEFİ

Türkiye ayakkabı pazarının öncü firmalarından FLO, müşterilerini satın alma alışkanlıkları üzerinden segmentlere ayırmak ve bu segmentler özelinde stratejiler geliştirmek istiyor.

Veri seti, son alışverişlerini 2020 - 2021 yıllarında OmniChannel (hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.


______________________________

### 2. PROJE AŞAMALARI

1. Veriyi Anlama (Data Understanding)
2. Veri Hazırlama (Data Preparation)
3. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics: Recency, Frequency, Monetary sütunlarını olusturma)
4. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
5. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)

______________________________

### 3. PROJE SONUÇLARI

#### Soru 1:
Oluşturulan Müşteri Segmentleri & Segment Bazlı Recency, Frequency ve Monetary Ortalamaları nasıldır?

<img width="600" alt="Screen Shot 2024-02-07 at 11 46 30 AM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/7594c4ab-b765-4d3a-b91a-8dd416f2455c">

<img width="400" alt="Screen Shot 2024-02-07 at 11 51 24 AM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/5107b094-98e4-4e76-84f8-3f1a3bb27f1f">


#### Müşteri Segmentlerine Göre Öneriler:

- **Champions (Şampiyonlar):**                          En değerli müşteriler. Özel teşviklerle ve VIP müşteri programları ile memnuniyetleri artırılabilir.
- **Loyal Customers (Sadık Müşteriler):**                Düzenli alışveriş yapan müşteriler. Satışları artırmak için mevcut alışveriş alışkanlıklarına uygun ürün ve hizmetler önerilebilir.
- **Potential Loyalists (Potansiyel Sadık Müşteriler):** Sadık müşteri olma potansiyeline sahip olanlar. Daha fazla alışveriş yapmaları için özel tekliflerle teşvik edilebilirler.
- **Promising (Umut Vadedenler):**                       Potansiyel değer taşıyan müşteriler. Yeni ürünler veya kampanyalarla ilgileri çekilebilir.
- **New Customers (Yeni Müşteriler):**                   Yeni müşterilere hoş geldin teklifleri sunulabilir ve ilk alışverişlerinde indirimler sağlanabilir.
- **Need Attention (Dikkat Edilmesi Gerekenler):**       Memnuniyetsiz veya şikayetçi müşteriler. Sorunlarını çözmek için özel ilgi gösterilmelidir. Geri ödeme veya değişim gibi çözümler sunulabilir.
- **Can't Lose (Kaybedilemeyecekler):**                  Potansiyel müşteri kaybı riski olanlar. Elde tutmak için özel teklifler sunulabilir.
- **At Risk (Risk Altındakiler):**                       Kaybedilmesi riski olan müşteriler. Özel indirimler veya kampanyalarla tekrar kazanılmaya çalışılabilir.
- **About to Sleep (Uyumak Üzere Olanlar):**             Az alışveriş yapan müşteriler. Aktif hale getirmek için özel teklifler sunulabilir.
- **Hibernating (Uykuda Olanlar):**                      Alışveriş yapmayan eski müşteriler. Geri kazanmak için özel teklifler ve hatırlatıcı mesajlar gönderilebilir.


__________________________________

#### Soru 2 :
FLO bünyesine dahil edilen yeni bir kadın ayakkabı markasının tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçilmek isteniliyor.

Bu müşterilerin "sadık müşterilerden (champions, loyal_customers) ve kadın kategorisinden alışveriş yapan kişiler" olması planlandı. Bu profildeki müşterilerin id numaralarını bulunuz.


<img width="600" alt="Screen Shot 2024-02-07 at 12 10 33 PM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/10ef2888-7a8d-4f5e-96e8-873c1adef770">

__________________________________


#### Soru 3 :
FLO Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır.

Bu indirimle ilgili kategorilerle ilgilenen "geçmişte iyi müşterilerden olan ama uzun süredir alışveriş yapmayan" ve "yeni gelen müşteriler" özel olarak hedef alınmak isteniliyor. Bu profildeki müşterilerin id numaralarını bulunuz.

<img width="600" alt="Screen Shot 2024-02-07 at 12 09 42 PM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/2e3f94fb-2677-4932-b06e-b0994ca90052">


__________________________________
### Sonuç:

Bu projede RFM analizi sonucunda elde edilen müşteri segmentlerini, şirket kullanarak pazarlama stratejilerini geliştirebilir ve uzun vadeli başarı için müşterileriyle daha güçlü ilişkiler kurabilir.

