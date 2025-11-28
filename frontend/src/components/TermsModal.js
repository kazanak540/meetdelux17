import React from 'react';
import { X, FileText, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';

const TermsModal = ({ isOpen, onClose, onAccept }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="sticky top-0 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-6 w-6" />
              <h2 className="text-xl font-bold">Kiralama Sözleşmesi</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-6 overflow-y-auto max-h-[calc(90vh-180px)] space-y-6">
            {/* Alert Box */}
            <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg">
              <div className="flex items-start">
                <AlertCircle className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                <p className="ml-3 text-sm text-amber-800">
                  Lütfen rezervasyonunuzu tamamlamadan önce aşağıdaki sözleşmeyi dikkatlice okuyun.
                </p>
              </div>
            </div>

            {/* Contract Text */}
            <div className="prose prose-sm max-w-none">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                MEETDELUX ETKİNLİK ALANI KİRALAMA ŞARTLARI VE KOŞULLARI
              </h1>

              <p className="text-gray-700 leading-relaxed mb-6">
                Bu belge, MeetDelux platformunu kullanan kiracı ("<strong>Müşteri</strong>") ile etkinlik alanını sağlayan 
                Otel ("<strong>Mekan Sahibi</strong>") arasındaki kiralama işleminin temel koşullarını ve MeetDelux'un bu 
                süreçteki rolünü belirler.
              </p>

              {/* Madde 1 */}
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h2 className="text-lg font-bold text-indigo-600 mb-3">
                  Madde 1: Tanımlar ve MeetDelux'un Rolü
                </h2>
                <div className="space-y-2 text-gray-700">
                  <p><strong>1.1. Platform:</strong> www.meetdelux.com adresinde yer alan, Müşteri ile Mekan Sahibi'ni bir araya getiren online aracılık platformudur.</p>
                  <p><strong>1.2. MeetDelux Rolü:</strong> MeetDelux, yalnızca Müşteri ile Mekan Sahibi arasında bir aracı ve rezervasyon kolaylaştırıcısıdır. MeetDelux, Mekan Sahibi değildir ve kiralanan alanın fiziksel durumu, hizmet kalitesi veya yasal uygunluğundan sorumlu değildir.</p>
                  <p><strong>1.3. Sözleşmenin Tarafları:</strong> Kiralama sözleşmesi, doğrudan Müşteri ile Mekan Sahibi (Otel) arasında kurulur.</p>
                </div>
              </div>

              {/* Madde 2 */}
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h2 className="text-lg font-bold text-indigo-600 mb-3">
                  Madde 2: Rezervasyon, Fiyatlandırma ve Komisyon
                </h2>
                <div className="space-y-2 text-gray-700">
                  <p><strong>2.1. Fiyatlar:</strong> Platformda listelenen fiyatlar, Mekan Sahibi tarafından belirlenir ve MeetDelux tarafından Mekan Sahibi adına Müşteriye sunulur. Fiyatlar, KDV dahildir.</p>
                  <p><strong>2.2. Komisyon:</strong> MeetDelux, Mekan Sahibi'nden (Otel) bir komisyon almaktadır. Müşteri'ye yansıtılan fiyata herhangi bir ek hizmet bedeli yansıtılmaz.</p>
                  <p><strong>2.3. Ödeme:</strong> Rezervasyonun kesinleşmesi için belirlenen tutar, Müşteri tarafından Platform aracılığıyla Mekan Sahibi'ne ödenir. Ödeme yöntemleri platformda belirtilir.</p>
                  <p><strong>2.4. Kesinleşme:</strong> Ödeme yapıldıktan sonra Mekan Sahibi'nin 48 saat içinde rezervasyonu onaylaması ile rezervasyon kesinleşir. Onaylanmayan rezervasyonlarda ödeme Müşteriye iade edilir.</p>
                </div>
              </div>

              {/* Madde 3 */}
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h2 className="text-lg font-bold text-indigo-600 mb-3">
                  Madde 3: İptal ve Değişiklik Koşulları
                </h2>
                <div className="space-y-2 text-gray-700">
                  <p><strong>3.1. İptal Politikası:</strong> Her Mekan Sahibi'nin kendine ait bir iptal politikası bulunmaktadır. Müşteri, rezervasyon yapmadan önce Mekan Sahibi'nin ilanında belirtilen İptal ve İade Şartları'nı okumakla yükümlüdür.</p>
                  <p><strong>3.2. Genel İptal Kuralı (Varsayılan):</strong> Mekan Sahibi'nin özel bir iptal politikası belirtmemesi durumunda, aşağıdaki varsayılan kurallar uygulanır:</p>
                  <ul className="list-disc ml-6 space-y-1">
                    <li>Etkinlik tarihine <strong>30 gün ve üzeri</strong> kala yapılan iptallerde ödenen tutarın <strong>%100</strong>'ü iade edilir.</li>
                    <li>Etkinlik tarihine <strong>15-29 gün</strong> kala yapılan iptallerde ödenen tutarın <strong>%50</strong>'si iade edilir.</li>
                    <li>Etkinlik tarihine <strong>14 gün ve daha az</strong> kala yapılan iptallerde iade yapılmaz.</li>
                  </ul>
                  <p><strong>3.3. Tarih Değişikliği:</strong> Tarih değişikliği talepleri, Mekan Sahibi'nin müsaitlik durumuna bağlıdır ve Mekan Sahibi'nin onayı olmadan yapılamaz.</p>
                </div>
              </div>

              {/* Madde 4 */}
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h2 className="text-lg font-bold text-indigo-600 mb-3">
                  Madde 4: Mekan Kullanımı ve Sorumluluklar
                </h2>
                <div className="space-y-2 text-gray-700">
                  <p><strong>4.1. Kullanım Amacı:</strong> Kiralanan alan, yalnızca rezervasyonda belirtilen etkinlik amacı (seminer, toplantı, balo vb.) için kullanılabilir.</p>
                  <p><strong>4.2. Müşteri Sorumluluğu:</strong> Müşteri, etkinlik sırasında Mekan Sahibi'ne ait tesiste ve kiralanan alanda oluşabilecek her türlü hasardan sorumludur ve bu hasarları tazmin etmekle yükümlüdür.</p>
                  <p><strong>4.3. Teknik ve Personel Hizmetleri:</strong> Kiralama fiyatına dahil olan/olmayan teknik ekipman (projeksiyon, ses sistemi) ve personel hizmetleri (catering, hostes) Mekan Sahibi'nin ilanında net olarak belirtilir. Ek hizmet talepleri için Müşteri, doğrudan Mekan Sahibi ile iletişime geçmelidir.</p>
                  <p><strong>4.4. Yasal Uygunluk:</strong> Müşteri, etkinliğin tüm yerel yasalara, yönetmeliklere ve Otel'in kurallarına uygun olarak gerçekleştirilmesinden tek başına sorumludur.</p>
                </div>
              </div>

              {/* Madde 5 */}
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h2 className="text-lg font-bold text-indigo-600 mb-3">
                  Madde 5: Uyuşmazlıkların Çözümü
                </h2>
                <div className="space-y-2 text-gray-700">
                  <p><strong>5.1. Arabuluculuk:</strong> Kiralama sürecinden doğan hizmet kalitesi veya mekân koşulları ile ilgili uyuşmazlıklarda, MeetDelux yalnızca bir arabuluculuk görevi üstlenebilir; ancak bir çözüm garantisi vermez.</p>
                  <p><strong>5.2. Hukuki Yetki:</strong> Kiralama sözleşmesinden doğan hukuki uyuşmazlıklar, Mekan Sahibi'nin bulunduğu yerdeki yetkili Mahkemeler ve İcra Daireleri tarafından çözümlenir.</p>
                </div>
              </div>

              {/* Final Notice */}
              <div className="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-r-lg mt-6">
                <p className="text-sm text-indigo-900 font-medium">
                  <strong>Önemli Not:</strong> Müşteri, rezervasyonunu tamamlama butonu veya ödeme işlemini gerçekleştirmesi ile yukarıdaki tüm Şart ve Koşulları peşinen kabul etmiş sayılır.
                </p>
              </div>
            </div>
          </div>

          {/* Footer Actions */}
          <div className="sticky bottom-0 bg-gray-50 px-6 py-4 border-t flex items-center justify-between">
            <Button
              variant="outline"
              onClick={onClose}
              className="px-6"
            >
              Kapat
            </Button>
            <Button
              onClick={() => {
                onAccept();
                onClose();
              }}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8"
            >
              Okudum, Kabul Ediyorum
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TermsModal;
