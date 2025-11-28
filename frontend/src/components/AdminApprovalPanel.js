import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';
import { Button } from './ui/button';
import { CheckCircle, XCircle, Building2, DoorOpen, Clock, AlertCircle, Eye, X, MapPin, Star, Phone, Mail, Globe } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminApprovalPanel = ({ onApprovalComplete }) => {
  const { user } = useContext(AuthContext);
  const [pendingHotels, setPendingHotels] = useState([]);
  const [pendingRooms, setPendingRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('hotels'); // 'hotels' or 'rooms'
  const [previewHotel, setPreviewHotel] = useState(null);
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    if (user && user.role === 'admin') {
      fetchPendingItems();
    }
  }, [user]);

  const fetchPendingItems = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const [hotelsRes, roomsRes] = await Promise.all([
        axios.get(`${API}/admin/hotels/pending`, { headers }),
        axios.get(`${API}/admin/rooms/pending`, { headers })
      ]);
      
      setPendingHotels(hotelsRes.data);
      setPendingRooms(roomsRes.data);
    } catch (error) {
      console.error('Error fetching pending items:', error);
      toast.error('Onay bekleyen öğeler yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const handleApproveHotel = async (hotelId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/admin/hotels/${hotelId}/approve`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Otel onaylandı!');
      fetchPendingItems();
      setShowPreview(false);
      onApprovalComplete && onApprovalComplete();
    } catch (error) {
      console.error('Error approving hotel:', error);
      toast.error('Otel onaylanırken hata oluştu');
    }
  };

  const handleRejectHotel = async (hotelId) => {
    const reason = prompt('Red nedeni (opsiyonel):');
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/admin/hotels/${hotelId}/reject`, { reason }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Otel reddedildi');
      fetchPendingItems();
      setShowPreview(false);
      onApprovalComplete && onApprovalComplete();
    } catch (error) {
      console.error('Error rejecting hotel:', error);
      toast.error('Otel reddedilirken hata oluştu');
    }
  };

  const handlePreviewHotel = (hotel) => {
    setPreviewHotel(hotel);
    setShowPreview(true);
  };

  const handleApproveRoom = async (roomId) => {
    try {
      await axios.put(`${API}/admin/rooms/${roomId}/approve`);
      toast.success('Salon onaylandı!');
      fetchPendingItems();
    } catch (error) {
      console.error('Error approving room:', error);
      toast.error('Salon onaylanırken hata oluştu');
    }
  };

  const handleRejectRoom = async (roomId) => {
    const reason = prompt('Red nedeni (opsiyonel):');
    try {
      await axios.put(`${API}/admin/rooms/${roomId}/reject`, null, {
        params: { reason }
      });
      toast.success('Salon reddedildi');
      fetchPendingItems();
    } catch (error) {
      console.error('Error rejecting room:', error);
      toast.error('Salon reddedilirken hata oluştu');
    }
  };

  if (!user || user.role !== 'admin') {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-center space-x-3">
          <AlertCircle className="h-6 w-6 text-red-600" />
          <p className="text-red-800">Bu sayfaya erişim yetkiniz yok.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Yönetici Onay Paneli</h1>
        <p className="text-gray-600">Onay bekleyen otelleri ve salonları görüntüleyin ve onaylayın</p>
      </div>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('hotels')}
          className={`pb-4 px-2 font-medium transition-colors relative ${
            activeTab === 'hotels'
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <div className="flex items-center space-x-2">
            <Building2 className="h-5 w-5" />
            <span>Oteller</span>
            {pendingHotels.length > 0 && (
              <span className="bg-red-500 text-white text-xs rounded-full px-2 py-0.5">
                {pendingHotels.length}
              </span>
            )}
          </div>
        </button>
        
        <button
          onClick={() => setActiveTab('rooms')}
          className={`pb-4 px-2 font-medium transition-colors relative ${
            activeTab === 'rooms'
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <div className="flex items-center space-x-2">
            <DoorOpen className="h-5 w-5" />
            <span>Salonlar</span>
            {pendingRooms.length > 0 && (
              <span className="bg-red-500 text-white text-xs rounded-full px-2 py-0.5">
                {pendingRooms.length}
              </span>
            )}
          </div>
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Yükleniyor...</p>
        </div>
      ) : (
        <>
          {/* Hotels Tab */}
          {activeTab === 'hotels' && (
            <div className="space-y-4">
              {pendingHotels.length === 0 ? (
                <div className="bg-gray-50 rounded-lg p-12 text-center">
                  <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Onay bekleyen otel yok</p>
                </div>
              ) : (
                pendingHotels.map((hotel) => (
                  <div key={hotel.id} className="bg-white rounded-lg shadow border border-gray-200 p-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <Building2 className="h-6 w-6 text-indigo-600" />
                          <h3 className="text-xl font-semibold text-gray-900">{hotel.name}</h3>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 mt-4">
                          <div>
                            <p className="text-sm text-gray-500">Şehir</p>
                            <p className="font-medium">{hotel.city}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Yıldız</p>
                            <p className="font-medium">{'⭐'.repeat(hotel.star_rating || 0)}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Telefon</p>
                            <p className="font-medium">{hotel.phone}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Email</p>
                            <p className="font-medium">{hotel.email}</p>
                          </div>
                        </div>
                        
                        {hotel.description && (
                          <div className="mt-4">
                            <p className="text-sm text-gray-500">Açıklama</p>
                            <p className="text-gray-700 mt-1">{hotel.description}</p>
                          </div>
                        )}
                        
                        {hotel.images && hotel.images.length > 0 && (
                          <div className="mt-4">
                            <p className="text-sm text-gray-500 mb-2">Fotoğraflar ({hotel.images.length})</p>
                            <div className="grid grid-cols-4 gap-2">
                              {hotel.images.slice(0, 4).map((img, idx) => (
                                <img 
                                  key={idx} 
                                  src={img} 
                                  alt={`Hotel ${idx + 1}`}
                                  className="w-full h-20 object-cover rounded"
                                />
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex flex-col space-y-2 ml-6">
                        <Button
                          onClick={() => handlePreviewHotel(hotel)}
                          variant="outline"
                          className="border-indigo-300 text-indigo-600 hover:bg-indigo-50"
                        >
                          <Eye className="h-4 w-4 mr-2" />
                          Önizle
                        </Button>
                        <Button
                          onClick={() => handleApproveHotel(hotel.id)}
                          className="bg-green-600 hover:bg-green-700 text-white"
                        >
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Onayla
                        </Button>
                        <Button
                          onClick={() => handleRejectHotel(hotel.id)}
                          variant="outline"
                          className="border-red-300 text-red-600 hover:bg-red-50"
                        >
                          <XCircle className="h-4 w-4 mr-2" />
                          Reddet
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Rooms Tab */}
          {activeTab === 'rooms' && (
            <div className="space-y-4">
              {pendingRooms.length === 0 ? (
                <div className="bg-gray-50 rounded-lg p-12 text-center">
                  <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Onay bekleyen salon yok</p>
                </div>
              ) : (
                pendingRooms.map((room) => (
                  <div key={room.id} className="bg-white rounded-lg shadow border border-gray-200 p-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <DoorOpen className="h-6 w-6 text-indigo-600" />
                          <h3 className="text-xl font-semibold text-gray-900">{room.name}</h3>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 mt-4">
                          <div>
                            <p className="text-sm text-gray-500">Kapasite</p>
                            <p className="font-medium">{room.capacity} kişi</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Alan</p>
                            <p className="font-medium">{room.area_sqm} m²</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Günlük Fiyat</p>
                            <p className="font-medium">{room.price_per_day} {room.currency}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Tip</p>
                            <p className="font-medium">{room.room_type}</p>
                          </div>
                        </div>
                        
                        {room.description && (
                          <div className="mt-4">
                            <p className="text-sm text-gray-500">Açıklama</p>
                            <p className="text-gray-700 mt-1">{room.description}</p>
                          </div>
                        )}
                        
                        {room.features && room.features.length > 0 && (
                          <div className="mt-4">
                            <p className="text-sm text-gray-500 mb-2">Özellikler</p>
                            <div className="flex flex-wrap gap-2">
                              {room.features.map((feature, idx) => (
                                <span key={idx} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                                  {feature}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {room.images && room.images.length > 0 && (
                          <div className="mt-4">
                            <p className="text-sm text-gray-500 mb-2">Fotoğraflar ({room.images.length})</p>
                            <div className="grid grid-cols-4 gap-2">
                              {room.images.slice(0, 4).map((img, idx) => (
                                <img 
                                  key={idx} 
                                  src={img} 
                                  alt={`Room ${idx + 1}`}
                                  className="w-full h-20 object-cover rounded"
                                />
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex flex-col space-y-2 ml-6">
                        <Button
                          onClick={() => handleApproveRoom(room.id)}
                          className="bg-green-600 hover:bg-green-700 text-white"
                        >
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Onayla
                        </Button>
                        <Button
                          onClick={() => handleRejectRoom(room.id)}
                          variant="outline"
                          className="border-red-300 text-red-600 hover:bg-red-50"
                        >
                          <XCircle className="h-4 w-4 mr-2" />
                          Reddet
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </>
      )}

      {/* Hotel Preview Modal */}
      {showPreview && previewHotel && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Otel Önizleme</h2>
              <button
                onClick={() => setShowPreview(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="p-6">
              {/* Hero Section */}
              <div className="relative h-48 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg mb-6">
                <div className="absolute inset-0 bg-black/20 rounded-lg"></div>
                <div className="relative h-full flex items-end p-6">
                  <div className="text-white">
                    <div className="flex items-center space-x-2 mb-2">
                      <MapPin className="h-5 w-5" />
                      <span>{previewHotel.city}</span>
                    </div>
                    <h1 className="text-3xl font-bold mb-2">{previewHotel.name}</h1>
                    <div className="flex items-center space-x-1">
                      {[...Array(previewHotel.star_rating || 5)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                      ))}
                      <span className="ml-2 text-indigo-100">{previewHotel.star_rating} yıldızlı otel</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Images Gallery */}
              {previewHotel.images && previewHotel.images.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Fotoğraflar</h3>
                  <div className="grid grid-cols-3 gap-4">
                    {previewHotel.images.map((image, idx) => (
                      <img
                        key={idx}
                        src={image}
                        alt={`${previewHotel.name} ${idx + 1}`}
                        className="w-full h-40 object-cover rounded-lg"
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Description */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Otel Hakkında</h3>
                <p className="text-gray-600">
                  {previewHotel.description || 'Bu otel modern seminer salonları ile iş dünyasının ihtiyaçlarını karşılayan premium hizmetler sunmaktadır.'}
                </p>
              </div>

              {/* Address */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Adres</h3>
                <p className="text-gray-600 flex items-start space-x-2">
                  <MapPin className="h-5 w-5 mt-0.5 text-gray-400" />
                  <span>{previewHotel.address}</span>
                </p>
              </div>

              {/* Contact Info */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">İletişim Bilgileri</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <Phone className="h-5 w-5 text-gray-400" />
                    <span className="text-gray-600">{previewHotel.phone}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Mail className="h-5 w-5 text-gray-400" />
                    <span className="text-gray-600">{previewHotel.email}</span>
                  </div>
                  {previewHotel.website && (
                    <div className="flex items-center space-x-3">
                      <Globe className="h-5 w-5 text-gray-400" />
                      <a
                        href={previewHotel.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-600 hover:text-indigo-700"
                      >
                        Web Sitesi
                      </a>
                    </div>
                  )}
                </div>
              </div>

              {/* Facilities */}
              {previewHotel.facilities && previewHotel.facilities.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Olanaklar</h3>
                  <div className="flex flex-wrap gap-2">
                    {previewHotel.facilities.map((facility, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm"
                      >
                        {facility}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex space-x-3 pt-6 border-t border-gray-200">
                <Button
                  onClick={() => handleApproveHotel(previewHotel.id)}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                >
                  <CheckCircle className="h-5 w-5 mr-2" />
                  Onayla ve Yayınla
                </Button>
                <Button
                  onClick={() => handleRejectHotel(previewHotel.id)}
                  variant="outline"
                  className="flex-1 border-red-300 text-red-600 hover:bg-red-50"
                >
                  <XCircle className="h-5 w-5 mr-2" />
                  Reddet
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminApprovalPanel;
