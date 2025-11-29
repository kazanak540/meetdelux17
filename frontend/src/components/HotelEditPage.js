import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { ArrowLeft, Save, Building2 } from 'lucide-react';
import { toast } from 'sonner';
import GooglePlacesAutocomplete from './GooglePlacesAutocomplete';
import ImageUpload from './ImageUpload';
import ImageUploader from './ImageUploader';
import VideoUpload from './VideoUpload';
import Video360Upload from './Video360Upload';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HotelEditPage = () => {
  const { hotelId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [hotel, setHotel] = useState(null);
  const [activeTab, setActiveTab] = useState('info'); // info, services
  const [extraServices, setExtraServices] = useState([]);
  const [showAddService, setShowAddService] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [serviceForm, setServiceForm] = useState({
    name: '',
    description: '',
    price: 0,
    currency: 'EUR',
    unit: 'piece',
    category: 'catering',
    service_type: '',
    duration_minutes: null,
    capacity_per_service: null,
    is_available: true
  });
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    address: '',
    city: '',
    phone: '',
    email: '',
    website: '',
    star_rating: 5,
    facilities: [],
    latitude: '',
    longitude: '',
    images: [],
    videos: [],
    videos_360: [],
    is_active: true,
    is_draft: false,
    primary_image_index: 0
  });

  const facilities = {
    wifi: 'Wi-Fi',
    parking: 'Otopark',
    restaurant: 'Restoran',
    gym: 'Spor Salonu',
    pool: 'Yüzme Havuzu',
    spa: 'Spa',
    business_center: 'İş Merkezi',
    concierge: 'Konsiyerj',
    room_service: 'Oda Servisi',
    bar: 'Bar',
    conference_rooms: 'Toplantı Salonları',
    laundry: 'Çamaşırhane',
    airport_shuttle: 'Havaalanı Servisi',
    pet_friendly: 'Evcil Hayvan Dostu'
  };

  const serviceCategories = {
    transport: { label: 'Ulaşım & Transfer', emoji: '🚗' },
    catering: { label: 'Personel Hizmetleri', emoji: '👤' },
    refreshment: { label: 'Yiyecek & İçecek', emoji: '🍽️' },
    equipment: { label: 'Ekipman', emoji: '🎤' },
    service: { label: 'Diğer Hizmetler', emoji: '⭐' }
  };

  const serviceIcons = {
    airport_transfer: '✈️',
    city_transfer: '🚌',
    breakfast: '🍳',
    lunch: '🥗',
    dinner: '🍽️',
    coffee_break: '☕',
    professional_host: '👤',
    security: '🛡️',
    default: '⭐'
  };

  const fetchExtraServices = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/hotels/${hotelId}/extra-services`);
      setExtraServices(response.data);
    } catch (error) {
      console.error('Extra services fetch error:', error);
    }
  }, [hotelId]);

  const fetchHotelData = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/hotels/${hotelId}`);
      const hotelData = response.data;
      setHotel(hotelData);
      
      // Also fetch extra services
      fetchExtraServices();
      setFormData({
        name: hotelData.name || '',
        description: hotelData.description || '',
        address: hotelData.address || '',
        city: hotelData.city || '',
        phone: hotelData.phone || '',
        email: hotelData.email || '',
        website: hotelData.website || '',
        star_rating: hotelData.star_rating || 5,
        facilities: hotelData.facilities || [],
        latitude: hotelData.latitude || '',
        longitude: hotelData.longitude || '',
        images: hotelData.images || [],
        videos: hotelData.videos || [],
        videos_360: hotelData.videos_360 || [],
        is_active: hotelData.is_active !== undefined ? hotelData.is_active : true,
        is_draft: hotelData.is_draft || false,
        primary_image_index: hotelData.primary_image_index || 0
      });
    } catch (error) {
      console.error('Error fetching hotel:', error);
      toast.error('Otel bilgileri yüklenemedi');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  }, [hotelId, navigate]);

  useEffect(() => {
    if (hotelId) {
      fetchHotelData();
    }
  }, [hotelId, fetchHotelData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/hotels/${hotelId}`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      toast.success('Otel bilgileri başarıyla güncellendi!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Error updating hotel:', error);
      toast.error(error.response?.data?.detail || 'Otel güncellenirken hata oluştu');
    } finally {
      setSaving(false);
    }
  };

  const handleFacilityToggle = (facility) => {
    setFormData(prev => ({
      ...prev,
      facilities: prev.facilities.includes(facility)
        ? prev.facilities.filter(f => f !== facility)
        : [...prev.facilities, facility]
    }));
  };

  // Fotoğraf sırasını değiştir
  const moveImage = (fromIndex, toIndex) => {
    setFormData(prev => {
      const newImages = [...prev.images];
      const [removed] = newImages.splice(fromIndex, 1);
      newImages.splice(toIndex, 0, removed);
      
      // Eğer primary image etkilendiyse güncelle
      let newPrimaryIndex = prev.primary_image_index;
      if (fromIndex === prev.primary_image_index) {
        newPrimaryIndex = toIndex;
      } else if (fromIndex < prev.primary_image_index && toIndex >= prev.primary_image_index) {
        newPrimaryIndex--;
      } else if (fromIndex > prev.primary_image_index && toIndex <= prev.primary_image_index) {
        newPrimaryIndex++;
      }
      
      return {
        ...prev,
        images: newImages,
        primary_image_index: newPrimaryIndex
      };
    });
  };

  // Ana fotoğrafı seç
  const setPrimaryImage = (index) => {
    setFormData(prev => ({
      ...prev,
      primary_image_index: index
    }));
    toast.success('Ana fotoğraf belirlendi!');
  };

  const handlePlaceSelected = (place) => {
    if (place) {
      setFormData(prev => ({
        ...prev,
        address: place.formatted_address,
        city: place.city || prev.city,
        latitude: place.geometry.location.lat(),
        longitude: place.geometry.location.lng()
      }));
    }
  };

  const handleImageUploaded = (imageUrl) => {
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, imageUrl]
    }));
    setHotel(prev => ({
      ...prev,
      images: [...(prev.images || []), imageUrl]
    }));
  };

  const handleImageRemoved = async (imageUrl, index) => {
    if (!window.confirm('Bu fotoğrafı silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      // Extract just the filename from the full URL
      const imageFilename = imageUrl.split('/').pop();
      
      await axios.delete(`${API}/hotels/${hotelId}/images/${imageFilename}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Update both formData and hotel state
      setFormData(prev => ({
        ...prev,
        images: prev.images.filter((_, i) => i !== index)
      }));
      
      setHotel(prev => ({
        ...prev,
        images: (prev.images || []).filter((_, i) => i !== index)
      }));

      toast.success('Fotoğraf başarıyla silindi!');
    } catch (error) {
      console.error('Error deleting image:', error);
      toast.error(error.response?.data?.detail || 'Fotoğraf silinirken hata oluştu');
    }
  };

  const handleVideoUploaded = (videoUrl) => {
    setFormData(prev => ({
      ...prev,
      videos: [...prev.videos, videoUrl]
    }));
    setHotel(prev => ({
      ...prev,
      videos: [...(prev.videos || []), videoUrl]
    }));
  };

  const handleVideoRemoved = async (videoUrl) => {
    if (!window.confirm('Bu videoyu silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      // Extract just the filename from the full URL
      const videoFilename = videoUrl.split('/').pop();
      
      await axios.delete(`${API}/hotels/${hotelId}/videos/${videoFilename}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Update both formData and hotel state
      setFormData(prev => ({
        ...prev,
        videos: prev.videos.filter(v => v !== videoUrl)
      }));
      
      setHotel(prev => ({
        ...prev,
        videos: (prev.videos || []).filter(v => v !== videoUrl)
      }));

      toast.success('Video başarıyla silindi!');
    } catch (error) {
      console.error('Error deleting video:', error);
      toast.error(error.response?.data?.detail || 'Video silinirken hata oluştu');
    }
  };

  const handleVideo360Uploaded = (videoUrl) => {
    setFormData(prev => ({
      ...prev,
      videos_360: [...(prev.videos_360 || []), videoUrl]
    }));
    setHotel(prev => ({
      ...prev,
      videos_360: [...(prev.videos_360 || []), videoUrl]
    }));
  };

  const handleVideo360Removed = async (videoUrl) => {
    if (!window.confirm('Bu 360° videoyu silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const videoFilename = videoUrl.split('/').pop();
      
      await axios.delete(`${API}/hotels/${hotelId}/videos/${videoFilename}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setFormData(prev => ({
        ...prev,
        videos_360: (prev.videos_360 || []).filter(v => v !== videoUrl)
      }));
      
      setHotel(prev => ({
        ...prev,
        videos_360: (prev.videos_360 || []).filter(v => v !== videoUrl)
      }));

      toast.success('360° Video başarıyla silindi!');
    } catch (error) {
      console.error('Error deleting 360 video:', error);
      toast.error(error.response?.data?.detail || '360° Video silinirken hata oluştu');
    }
  };

  // Extra Services CRUD
  const handleAddService = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/hotels/${hotelId}/extra-services`, serviceForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Hizmet başarıyla eklendi!');
      setShowAddService(false);
      resetServiceForm();
      await fetchExtraServices();
    } catch (error) {
      console.error('Error adding service:', error);
      toast.error(error.response?.data?.detail || 'Hizmet eklenirken hata oluştu');
    }
  };

  const handleUpdateService = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/hotels/${hotelId}/extra-services/${editingService.id}`, serviceForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Hizmet başarıyla güncellendi!');
      setEditingService(null);
      resetServiceForm();
      await fetchExtraServices();
    } catch (error) {
      console.error('Error updating service:', error);
      toast.error(error.response?.data?.detail || 'Hizmet güncellenirken hata oluştu');
    }
  };

  const handleDeleteService = async (serviceId) => {
    if (!window.confirm('Bu hizmeti silmek istediğinizden emin misiniz?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API}/hotels/${hotelId}/extra-services/${serviceId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Hizmet başarıyla silindi!');
      await fetchExtraServices();
    } catch (error) {
      console.error('Error deleting service:', error);
      toast.error(error.response?.data?.detail || 'Hizmet silinirken hata oluştu');
    }
  };

  const startEditService = (service) => {
    setEditingService(service);
    setServiceForm({
      name: service.name,
      description: service.description || '',
      price: service.price,
      currency: service.currency,
      unit: service.unit,
      category: service.category,
      service_type: service.service_type || '',
      duration_minutes: service.duration_minutes,
      capacity_per_service: service.capacity_per_service,
      is_available: service.is_available
    });
    setShowAddService(true);
  };

  const resetServiceForm = () => {
    setServiceForm({
      name: '',
      description: '',
      price: 0,
      currency: 'EUR',
      unit: 'piece',
      category: 'catering',
      service_type: '',
      duration_minutes: null,
      capacity_per_service: null,
      is_available: true
    });
  };

  const getServiceIcon = (service) => {
    return serviceIcons[service.service_type] || serviceIcons.default;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate('/dashboard')}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Dashboard'a Dön
          </Button>
          <div className="flex items-center space-x-3">
            <Building2 className="h-8 w-8 text-indigo-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Otel Düzenle</h1>
              <p className="text-gray-500">{hotel?.name}</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6 border-b border-gray-200">
          <div className="flex space-x-8">
            <button
              type="button"
              onClick={() => setActiveTab('info')}
              className={`pb-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'info'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              🏨 Otel Bilgileri
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('services')}
              className={`pb-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'services'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ⭐ Ekstra Hizmetler
            </button>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'info' && (
          <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <Card>
            <CardHeader>
              <CardTitle>Temel Bilgiler</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Otel Adı *</Label>
                <Input
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Örn: Grand Hotel İstanbul"
                  required
                />
              </div>

              <div>
                <Label>Açıklama</Label>
                <Textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Otel hakkında detaylı bilgi..."
                  rows={4}
                />
              </div>

              <div>
                <Label>Yıldız Sayısı</Label>
                <Select
                  value={formData.star_rating?.toString()}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, star_rating: parseInt(value) }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5].map(star => (
                      <SelectItem key={star} value={star.toString()}>
                        {'⭐'.repeat(star)} ({star} Yıldız)
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Location */}
          <Card>
            <CardHeader>
              <CardTitle>Konum Bilgileri</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Adres Ara (Google Maps)</Label>
                <GooglePlacesAutocomplete
                  onPlaceSelected={handlePlaceSelected}
                  placeholder="Adres arayın..."
                />
              </div>

              <div>
                <Label>Adres *</Label>
                <Input
                  value={formData.address}
                  onChange={(e) => setFormData(prev => ({ ...prev, address: e.target.value }))}
                  placeholder="Tam adres"
                  required
                />
              </div>

              <div>
                <Label>Şehir *</Label>
                <Input
                  value={formData.city}
                  onChange={(e) => setFormData(prev => ({ ...prev, city: e.target.value }))}
                  placeholder="Örn: İstanbul"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Enlem (Latitude)</Label>
                  <Input
                    type="number"
                    step="any"
                    value={formData.latitude}
                    onChange={(e) => setFormData(prev => ({ ...prev, latitude: e.target.value }))}
                    placeholder="41.0082"
                  />
                </div>
                <div>
                  <Label>Boylam (Longitude)</Label>
                  <Input
                    type="number"
                    step="any"
                    value={formData.longitude}
                    onChange={(e) => setFormData(prev => ({ ...prev, longitude: e.target.value }))}
                    placeholder="28.9784"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Contact */}
          <Card>
            <CardHeader>
              <CardTitle>İletişim Bilgileri</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Telefon *</Label>
                <Input
                  value={formData.phone}
                  onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
                  placeholder="+90 212 XXX XX XX"
                  required
                />
              </div>

              <div>
                <Label>E-posta *</Label>
                <Input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  placeholder="info@hotel.com"
                  required
                />
              </div>

              <div>
                <Label>Website</Label>
                <Input
                  value={formData.website}
                  onChange={(e) => setFormData(prev => ({ ...prev, website: e.target.value }))}
                  placeholder="https://www.hotel.com"
                />
              </div>
            </CardContent>
          </Card>

          {/* Facilities */}
          <Card>
            <CardHeader>
              <CardTitle>Otel Olanakları</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {Object.entries(facilities).map(([key, label]) => (
                  <Label key={key} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.facilities.includes(key)}
                      onChange={() => handleFacilityToggle(key)}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm">{label}</span>
                  </Label>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Media Info */}
          <Card>
            <CardHeader>
              <CardTitle>Fotoğraf Yönetimi</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Current Images */}
              {formData.images && formData.images.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium mb-3">Mevcut Fotoğraflar ({formData.images.length})</h4>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {formData.images.map((img, idx) => (
                      <div key={idx} className="relative group">
                        <img src={img} alt={`Hotel ${idx + 1}`} className="w-full h-32 object-cover rounded-lg" />
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* New Image Upload */}
              <div>
                <h4 className="text-sm font-medium mb-3">Yeni Fotoğraf Ekle</h4>
                <ImageUploader
                  entityId={hotelId}
                  entityType="hotel"
                  onUploadSuccess={() => fetchHotelData()}
                  maxImages={10}
                />
              </div>
            </CardContent>
          </Card>

          {/* Video Management */}
          <Card>
            <CardHeader>
              <CardTitle>Video Yönetimi</CardTitle>
            </CardHeader>
            <CardContent>
              <VideoUpload
                entityId={hotelId}
                entityType="hotel"
                videos={formData.videos || []}
                onVideoUploaded={handleVideoUploaded}
                onVideoRemoved={handleVideoRemoved}
              />
            </CardContent>
          </Card>

          {/* 360 Video Management */}
          <Card>
            <CardHeader>
              <CardTitle>360° Video Yönetimi</CardTitle>
            </CardHeader>
            <CardContent>
              <Video360Upload
                entityId={hotelId}
                entityType="hotel"
                videos={formData.videos_360 || []}
                onVideoUploaded={handleVideo360Uploaded}
                onVideoRemoved={handleVideo360Removed}
              />
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex justify-end space-x-3 pb-8">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/dashboard')}
            >
              İptal
            </Button>
            <Button
              type="submit"
              disabled={saving}
              className="bg-indigo-600 hover:bg-indigo-700"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Kaydediliyor...
                </>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  Değişiklikleri Kaydet
                </>
              )}
            </Button>
          </div>
        </form>
        )}

        {/* Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6 pb-8">
            {/* Header */}
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">✨ Ekstra Hizmetler Yönetimi</h2>
                <p className="text-sm text-gray-600 mt-1">
                  Müşterilerinize sunacağınız ek hizmetleri tanımlayın ve fiyatlandırın
                </p>
              </div>
              <Button
                onClick={() => {
                  resetServiceForm();
                  setEditingService(null);
                  setShowAddService(true);
                }}
                className="bg-indigo-600 hover:bg-indigo-700"
              >
                + Yeni Hizmet Ekle
              </Button>
            </div>

            {/* Add/Edit Service Modal */}
            {showAddService && (
              <Card className="border-2 border-indigo-200 bg-indigo-50">
                <CardHeader>
                  <CardTitle className="flex justify-between items-center">
                    {editingService ? '✏️ Hizmet Düzenle' : '➕ Yeni Hizmet Ekle'}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setShowAddService(false);
                        setEditingService(null);
                        resetServiceForm();
                      }}
                    >
                      ✕
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Hizmet Adı *</Label>
                      <Input
                        value={serviceForm.name}
                        onChange={(e) => setServiceForm(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Örn: Havaalanı Transferi"
                      />
                    </div>
                    <div>
                      <Label>Kategori *</Label>
                      <Select
                        value={serviceForm.category}
                        onValueChange={(value) => setServiceForm(prev => ({ ...prev, category: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {Object.entries(serviceCategories).map(([key, val]) => (
                            <SelectItem key={key} value={key}>
                              {val.emoji} {val.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label>Açıklama</Label>
                    <Textarea
                      value={serviceForm.description}
                      onChange={(e) => setServiceForm(prev => ({ ...prev, description: e.target.value }))}
                      placeholder="Hizmet hakkında detaylı bilgi..."
                      rows={2}
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label>Fiyat *</Label>
                      <Input
                        type="number"
                        step="0.01"
                        min="0"
                        value={serviceForm.price}
                        onChange={(e) => setServiceForm(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))}
                        placeholder="0.00"
                      />
                    </div>
                    <div>
                      <Label>Para Birimi *</Label>
                      <Select
                        value={serviceForm.currency}
                        onValueChange={(value) => setServiceForm(prev => ({ ...prev, currency: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="EUR">€ EUR</SelectItem>
                          <SelectItem value="USD">$ USD</SelectItem>
                          <SelectItem value="TRY">₺ TRY</SelectItem>
                          <SelectItem value="GBP">£ GBP</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label>Birim</Label>
                      <Select
                        value={serviceForm.unit}
                        onValueChange={(value) => setServiceForm(prev => ({ ...prev, unit: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="piece">Adet</SelectItem>
                          <SelectItem value="hour">Saat</SelectItem>
                          <SelectItem value="day">Gün</SelectItem>
                          <SelectItem value="person">Kişi</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Hizmet Tipi</Label>
                      <Input
                        value={serviceForm.service_type}
                        onChange={(e) => setServiceForm(prev => ({ ...prev, service_type: e.target.value }))}
                        placeholder="Örn: airport_transfer"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        İkon için: airport_transfer, city_transfer, breakfast, lunch, dinner, coffee_break
                      </p>
                    </div>
                    <div>
                      <Label>Kapasite (Kişi)</Label>
                      <Input
                        type="number"
                        min="0"
                        value={serviceForm.capacity_per_service || ''}
                        onChange={(e) => setServiceForm(prev => ({ 
                          ...prev, 
                          capacity_per_service: e.target.value ? parseInt(e.target.value) : null 
                        }))}
                        placeholder="Örn: 4"
                      />
                    </div>
                  </div>

                  <div>
                    <Label>Süre (Dakika)</Label>
                    <Input
                      type="number"
                      min="0"
                      value={serviceForm.duration_minutes || ''}
                      onChange={(e) => setServiceForm(prev => ({ 
                        ...prev, 
                        duration_minutes: e.target.value ? parseInt(e.target.value) : null 
                      }))}
                      placeholder="Örn: 45"
                    />
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="is_available"
                      checked={serviceForm.is_available}
                      onChange={(e) => setServiceForm(prev => ({ ...prev, is_available: e.target.checked }))}
                      className="rounded border-gray-300"
                    />
                    <Label htmlFor="is_available" className="cursor-pointer">
                      Hizmet aktif (müşteriler görebilir)
                    </Label>
                  </div>

                  <div className="flex justify-end space-x-3 pt-4">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => {
                        setShowAddService(false);
                        setEditingService(null);
                        resetServiceForm();
                      }}
                    >
                      İptal
                    </Button>
                    <Button
                      type="button"
                      onClick={editingService ? handleUpdateService : handleAddService}
                      className="bg-indigo-600 hover:bg-indigo-700"
                    >
                      {editingService ? 'Güncelle' : 'Ekle'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Services List */}
            {extraServices.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <div className="text-6xl mb-4">📦</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Henüz ekstra hizmet eklenmemiş
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Müşterilerinize sunmak istediğiniz ek hizmetleri ekleyerek başlayın
                  </p>
                  <Button
                    onClick={() => {
                      resetServiceForm();
                      setEditingService(null);
                      setShowAddService(true);
                    }}
                    className="bg-indigo-600 hover:bg-indigo-700"
                  >
                    İlk Hizmeti Ekle
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Group services by category */}
                {Object.entries(serviceCategories).map(([categoryKey, categoryInfo]) => {
                  const categoryServices = extraServices.filter(s => s.category === categoryKey);
                  if (categoryServices.length === 0) return null;

                  return (
                    <div key={categoryKey} className="space-y-3">
                      <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                        <span className="text-2xl">{categoryInfo.emoji}</span>
                        {categoryInfo.label}
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {categoryServices.map((service) => (
                          <Card
                            key={service.id}
                            className={`border-2 transition-all hover:shadow-lg ${
                              service.is_available 
                                ? 'border-gray-200 bg-white' 
                                : 'border-gray-300 bg-gray-50 opacity-60'
                            }`}
                          >
                            <CardContent className="p-4">
                              <div className="flex items-start justify-between mb-3">
                                <div className="flex items-center gap-2">
                                  <span className="text-3xl">{getServiceIcon(service)}</span>
                                  <div>
                                    <h4 className="font-semibold text-gray-900">{service.name}</h4>
                                    {!service.is_available && (
                                      <span className="text-xs text-red-600 font-medium">
                                        🚫 Devre Dışı
                                      </span>
                                    )}
                                  </div>
                                </div>
                              </div>
                              
                              {service.description && (
                                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                                  {service.description}
                                </p>
                              )}

                              <div className="space-y-2 mb-4">
                                <div className="flex justify-between items-center">
                                  <span className="text-sm text-gray-600">Fiyat:</span>
                                  <span className="font-bold text-indigo-600">
                                    {service.price === 0 ? (
                                      <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-semibold">
                                        ✓ ÜCRETSİZ
                                      </span>
                                    ) : (
                                      `${service.price} ${service.currency}`
                                    )}
                                  </span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                  <span className="text-gray-600">Birim:</span>
                                  <span className="text-gray-900">{service.unit}</span>
                                </div>
                                {service.capacity_per_service && (
                                  <div className="flex justify-between items-center text-sm">
                                    <span className="text-gray-600">Kapasite:</span>
                                    <span className="text-gray-900">{service.capacity_per_service} kişi</span>
                                  </div>
                                )}
                                {service.duration_minutes && (
                                  <div className="flex justify-between items-center text-sm">
                                    <span className="text-gray-600">Süre:</span>
                                    <span className="text-gray-900">{service.duration_minutes} dk</span>
                                  </div>
                                )}
                              </div>

                              <div className="flex gap-2">
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="flex-1"
                                  onClick={() => startEditService(service)}
                                >
                                  ✏️ Düzenle
                                </Button>
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                  onClick={() => handleDeleteService(service.id)}
                                >
                                  🗑️
                                </Button>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HotelEditPage;
