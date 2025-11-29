import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent } from './ui/card';
import { MapPin, Star } from 'lucide-react';
import useCurrency from '../hooks/useCurrency';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SimilarHotels = ({ currentHotelId, city, starRating }) => {
  const navigate = useNavigate();
  const { formatPrice } = useCurrency();
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSimilarHotels();
  }, [currentHotelId, city]);

  const fetchSimilarHotels = async () => {
    try {
      const response = await axios.get(`${API}/hotels`);
      
      // Filter: same city, exclude current hotel, limit to 3
      const similar = response.data
        .filter(h => h.id !== currentHotelId && h.city === city)
        .slice(0, 3);

      setHotels(similar);
    } catch (error) {
      console.error('Error fetching similar hotels:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold text-gray-900">Benzer Oteller</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-64 bg-gray-200 animate-pulse rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  if (hotels.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-gray-900">Benzer Oteller</h2>
      <p className="text-gray-600 text-sm">
        {city} bölgesindeki diğer otellerimizi keşfedin
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {hotels.map(hotel => (
          <Card 
            key={hotel.id}
            className="cursor-pointer hover:shadow-lg transition-all duration-300 overflow-hidden group"
            onClick={() => navigate(`/hotels/${hotel.id}`)}
          >
            {/* Image */}
            <div className="relative h-48 overflow-hidden">
              <img
                src={hotel.images?.[0] || '/placeholder-hotel.jpg'}
                alt={hotel.name}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
              <div className="absolute top-3 right-3 bg-white px-2 py-1 rounded-full shadow-md">
                <div className="flex items-center space-x-1">
                  <Star className="w-4 h-4 text-yellow-400 fill-current" />
                  <span className="text-sm font-medium">{hotel.average_rating?.toFixed(1) || '5.0'}</span>
                </div>
              </div>
            </div>

            <CardContent className="p-4">
              <h3 className="font-semibold text-gray-900 mb-2 line-clamp-1">
                {hotel.name}
              </h3>
              
              <div className="flex items-center text-gray-600 text-sm mb-3">
                <MapPin className="w-4 h-4 mr-1" />
                <span className="line-clamp-1">{hotel.city}</span>
              </div>

              {/* Star Rating */}
              <div className="flex items-center mb-3">
                {[...Array(hotel.star_rating || 5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                ))}
              </div>

              {/* CTA */}
              <button 
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium"
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/hotels/${hotel.id}`);
                }}
              >
                Detayları Gör
              </button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SimilarHotels;
