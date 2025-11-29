import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Filter, X } from 'lucide-react';

const FilterSidebar = ({ onFilterChange, onClear }) => {
  const [filters, setFilters] = useState({
    city: '',
    minCapacity: '',
    maxCapacity: '',
    minPrice: '',
    maxPrice: '',
    features: [],
    sortBy: 'created_at'
  });

  const availableFeatures = [
    'Projeksiyon', 'Ses Sistemi', 'Sahne', 'LED Ekran',
    'Klima', 'WiFi', 'Whiteboard', 'Video Konferans',
    'Catering Area', 'Backstage'
  ];

  const cities = [
    'İstanbul', 'Ankara', 'İzmir', 'Antalya', 'Bursa',
    'Adana', 'Gaziantep', 'Konya', 'Trabzon', 'Denizli'
  ];

  const handleChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleFeatureToggle = (feature) => {
    const newFeatures = filters.features.includes(feature)
      ? filters.features.filter(f => f !== feature)
      : [...filters.features, feature];
    handleChange('features', newFeatures);
  };

  const handleClear = () => {
    const clearedFilters = {
      city: '',
      minCapacity: '',
      maxCapacity: '',
      minPrice: '',
      maxPrice: '',
      features: [],
      sortBy: 'created_at'
    };
    setFilters(clearedFilters);
    onClear();
  };

  return (
    <Card className="sticky top-24">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>Filtreler</span>
          </CardTitle>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClear}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="h-4 w-4 mr-1" />
            Temizle
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* City */}
        <div>
          <Label className="text-sm font-medium mb-2">Şehir</Label>
          <select
            value={filters.city}
            onChange={(e) => handleChange('city', e.target.value)}
            className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Tüm Şehirler</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        {/* Capacity */}
        <div>
          <Label className="text-sm font-medium mb-2">Kapasite</Label>
          <div className="grid grid-cols-2 gap-2">
            <Input
              type="number"
              placeholder="Min"
              value={filters.minCapacity}
              onChange={(e) => handleChange('minCapacity', e.target.value)}
              className="text-sm"
            />
            <Input
              type="number"
              placeholder="Max"
              value={filters.maxCapacity}
              onChange={(e) => handleChange('maxCapacity', e.target.value)}
              className="text-sm"
            />
          </div>
        </div>

        {/* Price */}
        <div>
          <Label className="text-sm font-medium mb-2">Günlük Fiyat (€)</Label>
          <div className="grid grid-cols-2 gap-2">
            <Input
              type="number"
              placeholder="Min"
              value={filters.minPrice}
              onChange={(e) => handleChange('minPrice', e.target.value)}
              className="text-sm"
            />
            <Input
              type="number"
              placeholder="Max"
              value={filters.maxPrice}
              onChange={(e) => handleChange('maxPrice', e.target.value)}
              className="text-sm"
            />
          </div>
        </div>

        {/* Features */}
        <div>
          <Label className="text-sm font-medium mb-2">Özellikler</Label>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {availableFeatures.map(feature => (
              <label key={feature} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.features.includes(feature)}
                  onChange={() => handleFeatureToggle(feature)}
                  className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <span className="text-sm text-gray-700">{feature}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Sort */}
        <div>
          <Label className="text-sm font-medium mb-2">Sıralama</Label>
          <select
            value={filters.sortBy}
            onChange={(e) => handleChange('sortBy', e.target.value)}
            className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
          >
            <option value="created_at">En Yeni</option>
            <option value="price_asc">Fiyat: Düşük → Yüksek</option>
            <option value="price_desc">Fiyat: Yüksek → Düşük</option>
            <option value="capacity">Kapasite: Büyük → Küçük</option>
          </select>
        </div>
      </CardContent>
    </Card>
  );
};

export default FilterSidebar;
