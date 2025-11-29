import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';

const WhatsAppButton = () => {
  const [isHovered, setIsHovered] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  // WhatsApp numarası (uluslararası format)
  const phoneNumber = '905352439696';
  
  // Varsayılan mesaj
  const defaultMessage = 'Merhaba! MeetDelux üzerinden otel ve toplantı salonu hakkında bilgi almak istiyorum.';
  
  const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(defaultMessage)}`;

  const handleClick = () => {
    window.open(whatsappUrl, '_blank');
  };

  return (
    <>
      {/* WhatsApp Floating Button */}
      <div className="fixed bottom-6 right-6 z-50">
        {/* Tooltip */}
        {showTooltip && (
          <div className="absolute bottom-full right-0 mb-2 px-4 py-2 bg-gray-900 text-white text-sm rounded-lg shadow-lg whitespace-nowrap animate-fade-in">
            WhatsApp ile iletişime geç
            <div className="absolute bottom-0 right-6 transform translate-y-1/2 rotate-45 w-2 h-2 bg-gray-900"></div>
          </div>
        )}

        {/* Button */}
        <button
          onClick={handleClick}
          onMouseEnter={() => {
            setIsHovered(true);
            setShowTooltip(true);
          }}
          onMouseLeave={() => {
            setIsHovered(false);
            setShowTooltip(false);
          }}
          className={`
            flex items-center justify-center
            w-14 h-14 sm:w-16 sm:h-16
            bg-[#25D366] hover:bg-[#128C7E]
            text-white rounded-full
            shadow-lg hover:shadow-2xl
            transition-all duration-300 ease-in-out
            ${isHovered ? 'scale-110' : 'scale-100'}
            group
          `}
          aria-label="WhatsApp ile iletişime geç"
        >
          {/* WhatsApp Icon */}
          <MessageCircle 
            className="w-7 h-7 sm:w-8 sm:h-8 group-hover:rotate-12 transition-transform duration-300" 
            strokeWidth={2}
          />
          
          {/* Pulse Animation */}
          <span className="absolute w-full h-full rounded-full bg-[#25D366] opacity-75 animate-ping"></span>
        </button>

        {/* Badge (Yeni mesaj göstergesi - opsiyonel) */}
        <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white text-xs font-bold shadow-md animate-pulse">
          1
        </div>
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
    </>
  );
};

export default WhatsAppButton;
