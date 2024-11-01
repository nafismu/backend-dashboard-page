from flask import Blueprint, jsonify

motivation_card_blueprint = Blueprint('motivation_card', __name__)

@motivation_card_blueprint.route('/', methods=['GET'])
def get_customer_growth_data():
    # Data yang akan dikirim ke frontend
    motivationalQuotes = [
    "Percayalah pada dirimu sendiri dan semua yang kamu mampu capai.",
    "Setiap hari adalah kesempatan baru untuk menjadi lebih baik.",
    "Kesuksesan tidak datang dengan mudah, tetapi usaha keras akan membawa hasil.",
    "Langkah kecil hari ini adalah awal dari perjalanan besar esok hari.",
    "Jangan takut gagal, karena dari kegagalan kita belajar menjadi lebih kuat.",
    "Tidak ada yang mustahil selama kamu yakin dan berusaha.",
    "Berani bermimpi adalah langkah pertama menuju kesuksesan.",
    "Rintangan adalah bagian dari perjalanan, hadapilah dengan tegar.",
    "Jangan menunggu waktu yang tepat, mulailah sekarang!",
    "Kegigihan adalah kunci untuk membuka pintu kesuksesan.",
    "Mimpimu adalah harapan bagi masa depanmu, jangan pernah menyerah.",
    "Setiap usaha tidak akan sia-sia, hasilnya akan datang pada waktunya.",
    "Kunci keberhasilan adalah fokus dan konsistensi.",
    "Ketika satu pintu tertutup, pintu lain terbuka.",
    "Perjalanan seribu mil dimulai dengan satu langkah kecil.",
    "Belajarlah dari kemarin, hiduplah untuk hari ini, dan berharaplah untuk esok.",
    "Keberhasilan besar membutuhkan waktu, nikmati prosesnya.",
    "Selalu ada cahaya setelah gelap, teruslah melangkah maju.",
    "Bangkit setiap kali terjatuh adalah tanda kesuksesan.",
    "Tidak ada batasan untuk mencapai apa yang kamu inginkan.",
    "Semua pencapaian besar dimulai dari mimpi kecil.",
    "Kamu lebih kuat dari yang kamu kira, jangan pernah meragukan dirimu.",
    "Jangan biarkan kegagalan menghalangimu, teruslah mencoba.",
    "Kebahagiaan adalah hasil dari usaha yang tulus.",
    "Keberhasilan adalah milik mereka yang tidak pernah berhenti mencoba.",
    "Jika kamu ingin sukses, mulai dari sekarang!",
    "Jangan pernah meremehkan kekuatan tekadmu.",
    "Kamu adalah penentu masa depanmu, buatlah keputusan yang tepat.",
    "Semakin banyak tantangan, semakin kuat dirimu.",
    "Sukses adalah hasil dari usaha dan kesabaran."
];

    return jsonify(motivationalQuotes)