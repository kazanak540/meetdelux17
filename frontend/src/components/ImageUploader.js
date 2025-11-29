import React, { useState } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Upload, X, Image as ImageIcon } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ImageUploader = ({ entityId, entityType, onUploadSuccess, maxImages = 10 }) => {
  const [uploading, setUploading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (validFiles.length !== files.length) {
      toast.error('Sadece resim dosyaları yükleyebilirsiniz');
    }
    
    setSelectedFiles(prev => [...prev, ...validFiles].slice(0, maxImages));
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const uploadImages = async () => {
    if (selectedFiles.length === 0) {
      toast.error('Lütfen en az bir resim seçin');
      return;
    }

    setUploading(true);
    const endpoint = entityType === 'hotel' 
      ? `${API}/hotels/${entityId}/upload-image`
      : `${API}/rooms/${entityId}/upload-image`;

    try {
      const uploadPromises = selectedFiles.map(async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return axios.post(endpoint, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      });

      await Promise.all(uploadPromises);
      toast.success(`${selectedFiles.length} fotoğraf yüklendi!`);
      setSelectedFiles([]);
      
      if (onUploadSuccess) onUploadSuccess();
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Fotoğraf yükleme başarısız');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-500 transition-colors">
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
          id="image-upload"
          disabled={uploading}
        />
        <label htmlFor="image-upload" className="cursor-pointer">
          <Upload className="h-12 w-12 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-600">
            Fotoğraf yüklemek için tıklayın
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Maksimum {maxImages} fotoğraf
          </p>
        </label>
      </div>

      {selectedFiles.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {selectedFiles.map((file, index) => (
            <div key={index} className="relative group">
              <img
                src={URL.createObjectURL(file)}
                alt={`Preview ${index + 1}`}
                className="w-full h-32 object-cover rounded-lg"
              />
              <button
                onClick={() => removeFile(index)}
                className="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {selectedFiles.length > 0 && (
        <Button
          onClick={uploadImages}
          disabled={uploading}
          className="w-full bg-indigo-600 hover:bg-indigo-700"
        >
          {uploading ? 'Yükleniyor...' : `${selectedFiles.length} Fotoğraf Yükle`}
        </Button>
      )}
    </div>
  );
};

export default ImageUploader;
