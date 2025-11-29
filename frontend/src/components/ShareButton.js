import React, { useState } from 'react';
import { Share2, Facebook, Twitter, Link2, Check } from 'lucide-react';
import { MessageCircle } from 'lucide-react';

const ShareButton = ({ title, url, description }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const shareUrl = url || window.location.href;
  const shareTitle = title || 'MeetDelux - Toplantı ve Balo Salonu';
  const shareDescription = description || 'Bu otele göz atın!';

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleWhatsAppShare = () => {
    const text = `${shareTitle}\n\n${shareDescription}\n\n${shareUrl}`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
  };

  const handleFacebookShare = () => {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`, '_blank');
  };

  const handleTwitterShare = () => {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareTitle)}`, '_blank');
  };

  return (
    <div className="relative">
      {/* Share Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <Share2 className="w-4 h-4 text-gray-600" />
        <span className="text-sm font-medium text-gray-700">Paylaş</span>
      </button>

      {/* Share Menu */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setIsOpen(false)}
          />

          {/* Menu */}
          <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden">
            <div className="py-2">
              {/* WhatsApp */}
              <button
                onClick={handleWhatsAppShare}
                className="w-full flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-center w-8 h-8 bg-[#25D366] rounded-full">
                  <MessageCircle className="w-4 h-4 text-white" />
                </div>
                <span className="text-sm font-medium text-gray-700">WhatsApp'ta Paylaş</span>
              </button>

              {/* Facebook */}
              <button
                onClick={handleFacebookShare}
                className="w-full flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-center w-8 h-8 bg-[#1877F2] rounded-full">
                  <Facebook className="w-4 h-4 text-white" fill="currentColor" />
                </div>
                <span className="text-sm font-medium text-gray-700">Facebook'ta Paylaş</span>
              </button>

              {/* Twitter */}
              <button
                onClick={handleTwitterShare}
                className="w-full flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-center w-8 h-8 bg-[#1DA1F2] rounded-full">
                  <Twitter className="w-4 h-4 text-white" fill="currentColor" />
                </div>
                <span className="text-sm font-medium text-gray-700">Twitter'da Paylaş</span>
              </button>

              {/* Divider */}
              <div className="my-2 border-t border-gray-200" />

              {/* Copy Link */}
              <button
                onClick={handleCopyLink}
                className="w-full flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-center w-8 h-8 bg-gray-200 rounded-full">
                  {copied ? (
                    <Check className="w-4 h-4 text-green-600" />
                  ) : (
                    <Link2 className="w-4 h-4 text-gray-600" />
                  )}
                </div>
                <span className="text-sm font-medium text-gray-700">
                  {copied ? 'Kopyalandı!' : 'Linki Kopyala'}
                </span>
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ShareButton;
