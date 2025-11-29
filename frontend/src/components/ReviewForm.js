import React, { useState } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import StarRating from './StarRating';
import { MessageSquare, ThumbsUp, ThumbsDown } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ReviewForm = ({ hotelId, onReviewSubmitted }) => {
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [pros, setPros] = useState('');
  const [cons, setCons] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (rating === 0) {
      toast.error('Lütfen yıldız vererek değerlendirin');
      return;
    }

    if (comment.trim().length < 10) {
      toast.error('Yorum en az 10 karakter olmalıdır');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API}/reviews`, {
        hotel_id: hotelId,
        rating: rating,
        comment: comment.trim(),
        pros: pros.trim() || null,
        cons: cons.trim() || null
      });

      toast.success('Yorumunuz başarıyla gönderildi!');
      
      // Reset form
      setRating(0);
      setComment('');
      setPros('');
      setCons('');

      // Callback to parent
      if (onReviewSubmitted) {
        onReviewSubmitted(response.data);
      }
    } catch (error) {
      console.error('Review submit error:', error);
      if (error.response?.status === 400 && error.response?.data?.detail?.includes('already reviewed')) {
        toast.error('Bu otel için zaten bir yorumunuz var');
      } else if (error.response?.status === 403) {
        toast.error('Yorum yapmak için giriş yapmalısınız');
      } else {
        toast.error('Yorum gönderilemedi. Lütfen tekrar deneyin');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <MessageSquare className="h-5 w-5 text-indigo-600" />
          <span>Değerlendirmenizi Paylaşın</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Rating */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Değerlendirme <span className="text-red-500">*</span>
            </label>
            <StarRating
              rating={rating}
              interactive={true}
              onChange={setRating}
              size="xl"
              showNumber={false}
            />
            {rating > 0 && (
              <p className="mt-2 text-sm text-gray-600">
                {rating === 5 && '🎉 Mükemmel!'}
                {rating === 4 && '👍 Çok İyi'}
                {rating === 3 && '😊 İyi'}
                {rating === 2 && '😐 Orta'}
                {rating === 1 && '😞 Kötü'}
              </p>
            )}
          </div>

          {/* Comment */}
          <div>
            <label htmlFor="comment" className="block text-sm font-medium text-gray-700 mb-2">
              Yorumunuz <span className="text-red-500">*</span>
            </label>
            <textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Deneyimlerinizi paylaşın... (En az 10 karakter)"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={4}
              minLength={10}
              maxLength={1000}
              required
            />
            <p className="mt-1 text-xs text-gray-500 text-right">
              {comment.length}/1000
            </p>
          </div>

          {/* Pros */}
          <div>
            <label htmlFor="pros" className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
              <ThumbsUp className="h-4 w-4 text-green-600" />
              <span>Olumlu Yönler (Opsiyonel)</span>
            </label>
            <textarea
              id="pros"
              value={pros}
              onChange={(e) => setPros(e.target.value)}
              placeholder="Beğendiğiniz özellikler..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={2}
              maxLength={300}
            />
          </div>

          {/* Cons */}
          <div>
            <label htmlFor="cons" className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
              <ThumbsDown className="h-4 w-4 text-red-600" />
              <span>Geliştirilmesi Gerekenler (Opsiyonel)</span>
            </label>
            <textarea
              id="cons"
              value={cons}
              onChange={(e) => setCons(e.target.value)}
              placeholder="İyileştirilebilecek noktalar..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={2}
              maxLength={300}
            />
          </div>

          <Button
            type="submit"
            disabled={loading || rating === 0 || comment.trim().length < 10}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            {loading ? 'Gönderiliyor...' : 'Yorumu Gönder'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ReviewForm;
