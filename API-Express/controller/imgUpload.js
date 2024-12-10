const { Storage } = require('@google-cloud/storage');
const multer = require('multer');
const multerGoogleStorage = require('multer-cloud-storage');
const path = require('path');
const connection = require("../server");  // Pastikan server.js menggunakan koneksi dengan pool atau koneksi callback

// Inisialisasi Google Cloud Storage
const storage = new Storage();
const bucketName = 'capstone-profile'; // Ganti dengan nama bucket Anda
const bucket = storage.bucket(bucketName);

// Konfigurasi multer untuk Google Cloud Storage
const upload = multer({
    storage: multerGoogleStorage.storageEngine({
        bucket: bucketName, // Nama bucket Google Cloud
        projectId: 'learned-balm-442802-r6', // ID Project Google Cloud
        keyFilename: path.join(__dirname, '..', 'config', 'credential.json'), // Path ke file kredensial yang benar
        destination: (req, file, cb) => {
            cb(null, 'profile-pictures/'); // Folder dalam bucket
        },
        filename: (req, file, cb) => {
            const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
            cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
        }
    }),
    limits: { fileSize: 5 * 1024 * 1024 }, // Maksimum ukuran file 5MB
    fileFilter: (req, file, cb) => {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!allowedTypes.includes(file.mimetype)) {
            return cb(new Error('Only JPEG, PNG, and JPG images are allowed!'));
        }
        cb(null, true);
    }
});

// Fungsi untuk menangani upload profil ke Google Cloud Storage
const uploadProfileImage = (req, res) => {
    const file = req.file;
    if (!file) {
        return res.status(400).json({ message: 'Please upload a valid image!' });
    }
    // Dapatkan URL gambar yang diunggah
    const fileUrl = `https://storage.googleapis.com/${bucketName}/profile-pictures/${file.filename}`;

    const userId = req.user.id_user; // ID pengguna dari autentikasi

    // Periksa apakah URL gambar sudah ada
    connection.query(
        'SELECT id_images FROM profile_images WHERE user_id = ?',
        [userId],
        (err, existingImage) => {
            if (err) {
                console.error('Query error:', err);
                return res.status(500).json({ message: 'Database error' });
            }
            if (existingImage.length > 0) {
                // Perbarui URL gambar jika sudah ada
                connection.query(
                    'UPDATE profile_images SET image_url = ? WHERE user_id = ?',
                    [fileUrl, userId],
                    (err) => {
                        if (err) {
                            console.error('Update error:', err);
                            return res.status(500).json({ message: 'Failed to update image URL' });
                        }
                        res.status(200).json({
                            message: 'Profile image updated successfully!',
                            fileUrl,
                        });
                    }
                );
            } else {
                // Tambahkan entri baru jika belum ada
                connection.query(
                    'INSERT INTO profile_images (user_id, image_url) VALUES (?, ?)',
                    [userId, fileUrl],
                    (err) => {
                        if (err) {
                            console.error('Insert error:', err);
                            return res.status(500).json({ message: 'Failed to upload image' });
                        }
                        res.status(200).json({
                            message: 'Profile image uploaded successfully!',
                            fileUrl,
                        });
                    }
                );
            }
        }
    );
};

const editProfileImage = (req, res) => {
    const file = req.file;
    if (!file) {
        return res.status(400).json({ message: 'Please upload a valid image!' });
    }

    const fileUrl = `https://storage.googleapis.com/${bucketName}/profile-pictures/${file.filename}`;
    const userId = req.user.id_user;

    // Ambil URL gambar lama dari database
    connection.query(
        'SELECT image_url FROM profile_images WHERE user_id = ?',
        [userId],
        (err, result) => {
            if (err) {
                console.error('Query error:', err);
                return res.status(500).json({ message: 'Database error' });
            }

            if (result.length > 0) {
                const oldImageUrl = result[0].image_url;

                // Hapus gambar lama dari Google Cloud Storage
                const oldFileName = oldImageUrl.split('/').pop();
                const oldFile = bucket.file(`profile-pictures/${oldFileName}`);
                oldFile.delete()
                    .then(() => {
                        // Perbarui URL gambar di database
                        connection.query(
                            'UPDATE profile_images SET image_url = ? WHERE user_id = ?',
                            [fileUrl, userId],
                            (err) => {
                                if (err) {
                                    console.error('Update error:', err);
                                    return res.status(500).json({ message: 'Failed to update image URL' });
                                }
                                res.status(200).json({
                                    message: 'Profile image updated successfully!',
                                    fileUrl,
                                });
                            }
                        );
                    })
                    .catch((err) => {
                        console.error('Error deleting old image:', err);
                        return res.status(500).json({ message: 'Failed to delete old image' });
                    });
            } else {
                return res.status(404).json({ message: 'No image found for this user' });
            }
        }
    );
};

const getProfileImage = (req, res) => {
    const userId = req.user.id_user; // Ambil ID pengguna dari middleware autentikasi

    // Ambil data pengguna dan gambar
    connection.query(
        `SELECT u.email, p.image_url
        FROM user u
        LEFT JOIN profile_images p ON u.id_user = p.user_id
        WHERE u.id_user = ?`, // Gunakan ? sebagai placeholder
        [userId], // Parameter query yang menggantikan ?
        (err, rows) => {
            if (err) {
                console.error('Query error:', err);
                return res.status(500).json({ message: 'Database error' });
            }
            if (rows.length === 0) {
                return res.status(404).json({ message: 'User not found!' });
            }

            res.status(200).json({
                message: 'get image success!',
                user: rows[0], // Mengembalikan data pengguna dan gambar
            });
        }
    );
};

const deleteProfileImage = (req, res) => {
    const userId = req.user.id_user;

    // Ambil URL gambar lama dari database
    connection.query(
        'SELECT image_url FROM profile_images WHERE user_id = ?',
        [userId],
        (err, result) => {
            if (err) {
                console.error('Query error:', err);
                return res.status(500).json({ message: 'Database error' });
            }

            if (result.length > 0) {
                const oldImageUrl = result[0].image_url;

                // Hapus gambar dari Google Cloud Storage
                const oldFileName = oldImageUrl.split('/').pop();
                const oldFile = bucket.file(`profile-pictures/${oldFileName}`);
                oldFile.delete()
                    .then(() => {
                        // Hapus entri gambar dari database
                        connection.query(
                            'DELETE FROM profile_images WHERE user_id = ?',
                            [userId],
                            (err) => {
                                if (err) {
                                    console.error('Delete error:', err);
                                    return res.status(500).json({ message: 'Failed to delete image from database' });
                                }
                                res.status(200).json({ message: 'Profile image deleted successfully!' });
                            }
                        );
                    })
                    .catch((err) => {
                        console.error('Error deleting image from cloud storage:', err);
                        return res.status(500).json({ message: 'Failed to delete image from storage' });
                    });
            } else {
                return res.status(404).json({ message: 'No image found for this user' });
            }
        }
    );
};

// Ekspor controller dan upload middleware
module.exports = {
    upload,
    uploadProfileImage,
    getProfileImage,
    editProfileImage,
    deleteProfileImage
};
