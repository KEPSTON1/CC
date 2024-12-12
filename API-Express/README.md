# How to connect the API
- Run this code on Visual Studio Code
- Copy the port server example https://localhost:3000 and paste in the postman
- Follow the method bellow by adding slash like https://localhost:3000/register
- Finnaly you can access the API


# Register
####	URL
- /register <br>
####	Method
-	POST
####	Request Body
o	email as string <br>
o	first_name as string <br>
o	last_name as string <br>
o	password as string <br>
o	phone as string <br>
o	gender as enum <br>
o	age as int <br>
#### Response
{ <br>
    "message": "Registrasi Akun Berhasil" <br>
}

# Login
####	URL
-	/login
####	Method
-	POST
####	Request Body
o	email as string <br>
o	password as string <br>
####	Response
{<br>
    "success": true, <br>
    "message": "Token JWT tergenerate!", <br>
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZF91c2VyIjozLCJpYXQiOjE3MzI3OTE2NjcsImV4cCI6MTczMjc5MzEwN30.l-e4CvtG3eKLSp82AttBynj0PjLzcinqpGUA6iHhvkk",
    "currUser": 3 <br>
}

# Get Profile
####	URL
-	/profile
####	Method
-	GET
####	Request Body
o	Authorization : Bearer Token <br>
####	Response 
{ <br>
    "success": true, <br>
    "user": { <br>
        "id_user": 3, <br>
        "email": "john.doe@example.com", <br>
        "first_name": "John", <br>
        "last_name": "Doe", <br>
        "password": "482c811da5d5b4bc6d497ffa98491e38", <br>
        "phone": "081234567890", <br>
        "gender": "male", <br>
        "age": 30, <br>
        "created_at": "2024-11-25T02:24:28.000Z", <br>
        "updated_at": "2024-11-25T02:24:28.000Z" <br>
    } <br>
}

# Edit Profile
####	URL
-	/profile/edit
####	Method
-	PUT
####	Request Body
•	{ <br>
•	  "first_name": "putri", <br>
•	  "last_name": "tanjung", <br>
•	  "phone": "081234567890", <br>
•	  "gender": "female", <br>
•	  "age": "29" <br>
####	Response
{ <br>
    "success": true, <br>
    "message": "Profil berhasil diperbarui" <br>
}

# Delete Profile
####	URL
-	/profile/delete
####	Method
-	DELETE
####	Request Body
o	Authorization : Bearer Token
####	Response
{ <br>
    "success": true, <br>
    "message": "Account deleted successfully" <br>
}


# Location
####	URL
-	/ getStore?latitude=-6.2088&longitude=106.8456&keyword=mental health di bali  (search keyword)
####	Method
-	GET
####	Request Body
o	Authorization : Bearer Token
####	Response
{ <br>
            "nama": "Denpasar Mental Health Centre (DMHC) and Wellness", <br>
            "alamat": "Jl. Padang Gajah Jalan Utara RS Balimed No.8, Padangsambian, Kec. Denpasar Bar., Kota Denpasar, Bali 80117, Indonesia",<br>
            "rating": 4.8, <br> 
            "fotoUrl": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=AdDdOWpvFnWXk0s5B9oUSMnF23aJER23j18NYvUudV0enqMEG3-I9eL3jibq3Z1jZ2co68TUy55Mdo8sM0jYnFoJZPTTeBzdl3IzPilWxZ1GQORo5wXY0-VSFd54vyaFVzKxrydevwfowVdyIJXreagW8fpvA9fDZBb0BllKN-Xi-FRCKD3E&key=AIzaSyAufZE3SGF_4vIS2J_lVpgFakj4E3Okh6s", <br>
            "jamBuka": "12:00", <br>
            "jamTutup": "20:00",  <br>
            "nomorHP": "0896-3820-7300", <br>
            "whatsappUrl": "" <br>
        }

# Article
####	URL
-	/article
####	Method
-	GET
####	Request Body
o	Authorization : Bearer Token
####	Response
"articles": [<br>
        { <br>
            "source": { <br>
                "id": null, <br>
                "name": "Liputan6.com" <br>
            }, <br>
            "author": "Dyah Puspita Wisnuwardani", <br>
            "title": "Cegah Masalah Mental dengan Skrining Kesehatan Jiwa Rutin, Akses Mudah di Puskesmas", <br>
            "description": "Direktur Kesehatan Jiwa Kemenkes, dr. Imran Pambudi, MPHM, menyampaikan bahwa anjuran skrining kesehatan jiwa berlaku bagi semua kelompok usia, mulai dari anak-anak hingga lanjut usia (lansia).", <br>
            "url": "https://www.liputan6.com/health/read/5761160/cegah-masalah-mental-dengan-skrining-kesehatan-jiwa-rutin-akses-mudah-di-puskesmas", <br>
            "urlToImage": "https://cdn0-production-images-kly.akamaized.net/VfmpOzZKka2800- Bm1tXInBd4I4=/1200x675/smart/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3952795/original/022709500_1646411289-priscilla-du-preez-F9DFuJoS9EU-unsplash.jpg", <br>
            "publishedAt": "2024-10-27T06:05:31Z", <br>
            "content": "Liputan6.com, Jakarta - Untuk menjaga kesehatan jiwa masyarakat, Kementerian Kesehatan (Kemenkes) RI menganjurkan agar setiap individu menjalani skrining kesehatan jiwa minimal satu kali setahun. Skr… [+1611 chars]" <br>
        }





