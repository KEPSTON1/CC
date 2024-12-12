# Step
- Open this code on your Visual Studio Code and running this code
- Copy the url server and paste in the postman, Example: 

# Prediksi
####	URL
-	/predict
####	Method
-	POST
####	Request Body
{ <br>
  "Menjadi marah karena hal-hal kecil/sepele": 3, <br>
  "Mulut terasa kering": 3, <br>
  "Tidak dapat melihat hal yang positif dari suatu kejadian": 3, <br> 
  "Merasakan gangguan dalam bernapas (napas cepat, sulit bernapas)": 3, <br>
  "Merasa sepertinya tidak kuat lagi untuk melakukan suatu kegiatan": 3, <br>
  "Cenderung bereaksi berlebihan pada situasi": 3, <br>
  "Kelemahan pada anggota tubuh": 3, <br>
  "Kesulitan untuk relaksasi/bersantai": 3, <br>
  "Cemas yang berlebihan dalam suatu situasi namun bisa lega jika hal/situasi itu berakhir": 3, <br>
  "Merasa pesimis dalam segala hal": 2, <br>
  "Mudah merasa kesal": 3, <br> 
  "Merasa banyak menghabiskan energi karena cemas": 3, <br>
  "Merasa sedih dan depresi": 2, <br>
  "Tidak sabaran": 3, <br>
  "Merasa kelelahan": 3, <br>
  "Kehilangan minat pada banyak hal (misal: makan, ambulasi, sosialisasi)": 2, <br>
  "Merasa diri tidak layak": 3, <br>
  "Mudah tersinggung": 3, <br>
  "Berkeringat (misal: tangan berkeringat) tanpa stimulasi oleh cuaca maupun latihan fisik": 3, <br>
  "Ketakutan tanpa alasan yang jelas": 0, <br> 
  "Merasa hidup tidak berharga": 0, <br>
  "Sulit untuk beristirahat": 1, <br>
  "Kesulitan dalam menelan": 1, <br>
  "Tidak dapat menikmati hal-hal yang saya lakukan": 0, <br>
  "Perubahan kegiatan jantung dan denyut nadi tanpa stimulasi oleh latihan fisik": 3, <br>
  "Merasa hilang harapan dan putus asa": 1, <br>
  "Mudah marah": 0, <br>
  "Mudah panik": 3, <br>
  "Kesulitan untuk tenang setelah sesuatu yang mengganggu": 1, <br>
  "Takut diri terhambat oleh tugas-tugas yang tidak biasa dilakukan": 1, <br>
  "Sulit untuk antusias pada banyak hal": 2, <br>
  "Sulit mentoleransi gangguan-gangguan terhadap hal yang sedang dilakukan": 3, <br>
  "Berada pada keadaan tegang": 1, <br>
  "Merasa tidak berharga": 1, <br>
  "Tidak dapat memaklumi hal apapun yang menghalangi anda untuk menyelesaikan hal yang sedang Anda lakukan": 1, <br>
  "Merasa ketakutan": 1, <br>
  "Merasa tidak ada harapan untuk masa depan": 1, <br>
  "Merasa tidak berarti": 1, <br>
  "Mudah gelisah": 0, <br>
  "Khawatir dengan situasi saat diri Anda mungkin menjadi panik dan mempermalukan diri sendiri": 0, <br>
  "Gemetar": 1, <br> 
  "Sulit untuk meningkatkan inisiatif dalam melakukan sesuatu": 0,<br> 
  "Apakah anda sudah yakin dengan seluruh pertanyaan anda": 3 <br>
} <br>
#### Response
{ <br>
    "Kategori_Depresi": "Parah", <br>
    "Kategori_Kecemasan": "Sangat Parah", <br>
    "Kategori_Stres": "Parah", <br>
    "Prediksi_Depresi": 0.9853578805923462, <br>
    "Prediksi_Kecemasan": 0.001631899387575686, <br>
    "Prediksi_Stres": 0.003162162145599723, <br>
    "Skor_Depresi": 21, <br>
    "Skor_Kecemasan": 28, <br>
    "Skor_Stres": 28 <br>
}

# getHistory
####	URL
-	/history
####	Method
-	GET
####	Request Body
o	Authorization: bearer token
#### Response
{ <br>
    "history": [ <br>
        { <br>
            "created_at": "Tue, 03 Dec 2024 03:32:26 GMT", <br>
            "id": 2, <br> 
            "kategori_depresi": "Parah", <br>
            "kategori_kecemasan": "Sangat Parah", <br>
            "kategori_stres": "Parah", <br>
            "prediksi_depresi": 0.985358, <br>
            "prediksi_kecemasan": 0.0016319, <br>
            "prediksi_stres": 0.00316216, <br>
            "skor_depresi": 21, <br>
            "skor_kecemasan": 28, <br>
            "skor_stres": 26 <br>
        } <br>
    ] <br>
}


# deleteHistory
####	URL
-	/delete/id
#	Method
-	DELETE
####	Request Body
o	Authorization: bearer token
#### Response
{ <br>
    "message": "Data with id 2 successful deleted" <br>
}


