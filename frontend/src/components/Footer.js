import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Phone, Mail, Instagram } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_turkce-translator-4/artifacts/jua4tf7e_IMG_0255.png" 
                alt="MeetDelux Logo" 
                className="h-12 w-12 object-contain"
              />
              <h3 className="text-2xl font-bold text-white">
                Meet<span className="text-indigo-400">Delux</span>
              </h3>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              Türkiye'nin en lüks seminer salonu ve toplantı merkezi rezervasyon platformu. 
              İşletmeniz için ideal mekanı bulun, hemen rezervasyon yapın.
            </p>
            
            {/* Social Media */}
            <div className="flex space-x-4">
              <a 
                href="https://www.instagram.com/meetdelux/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-indigo-400 transition-colors"
                aria-label="Instagram'da bizi takip edin"
              >
                <Instagram className="h-5 w-5" />
              </a>
              {/* Diğer sosyal medya hesapları açıldığında buraya eklenecek */}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Hızlı Linkler</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-400 hover:text-indigo-400 transition-colors">
                  Ana Sayfa
                </Link>
              </li>
              <li>
                <Link to="/rooms" className="text-gray-400 hover:text-indigo-400 transition-colors">
                  Salon Ara
                </Link>
              </li>
              <li>
                <Link to="/hotels" className="text-gray-400 hover:text-indigo-400 transition-colors">
                  Oteller
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-400 hover:text-indigo-400 transition-colors">
                  İletişim
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-white font-semibold mb-4">İletişim</h4>
            <ul className="space-y-3">
              <li className="flex items-start space-x-3">
                <MapPin className="h-5 w-5 text-indigo-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-400 text-sm">
                  Zorlu Center, Levazım<br />
                  Koru Sk. No:2<br />
                  34340 Beşiktaş<br />
                  İstanbul
                </span>
              </li>
              <li className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-indigo-400 flex-shrink-0" />
                <a 
                  href="tel:+905352439696" 
                  className="text-gray-400 hover:text-indigo-400 transition-colors"
                >
                  +90 535 243 96 96
                </a>
              </li>
              <li className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-indigo-400 flex-shrink-0" />
                <a 
                  href="mailto:info@meetdelux.com" 
                  className="text-gray-400 hover:text-indigo-400 transition-colors"
                >
                  info@meetdelux.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-gray-400 text-sm">
              © {new Date().getFullYear()} MeetDelux. Tüm hakları saklıdır.
            </p>
            <div className="flex space-x-6 text-sm">
              <Link to="/privacy" className="text-gray-400 hover:text-indigo-400 transition-colors">
                Gizlilik Politikası
              </Link>
              <Link to="/terms" className="text-gray-400 hover:text-indigo-400 transition-colors">
                Kullanım Koşulları
              </Link>
              <Link to="/contact" className="text-gray-400 hover:text-indigo-400 transition-colors">
                İletişim
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
