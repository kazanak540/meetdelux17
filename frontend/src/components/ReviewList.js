import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import StarRating from './StarRating';
import { MessageSquare, ThumbsUp, CheckCircle, Calendar, Reply } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ReviewList = ({ hotelId, refreshTrigger }) => {
  const { user } = useContext(AuthContext);
  const [reviews, setReviews] = useState([]);
  const [ratingDistribution, setRatingDistribution] = useState({});
  const [averageRating, setAverageRating] = useState(0);
  const [totalReviews, setTotalReviews] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('created_at');
  const [replyingTo, setReplyingTo] = useState(null);
  const [replyText, setReplyText] = useState('');

  useEffect(() => {
    fetchReviews();
  }, [hotelId, sortBy, refreshTrigger]);

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`${API}/reviews/hotel/${hotelId}?sort_by=${sortBy}`);
      setReviews(response.data.reviews);
      setRatingDistribution(response.data.rating_distribution);
      setAverageRating(response.data.average_rating);
      setTotalReviews(response.data.total_count);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      toast.error('Yorumlar yüklenemedi');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkHelpful = async (reviewId) => {
    try {
      await axios.post(`${API}/reviews/${reviewId}/helpful`);
      toast.success('Teşekkürler!');
      fetchReviews();
    } catch (error) {
      console.error('Error marking helpful:', error);
      toast.error('İşlem başarısız');
    }
  };

  const handleSubmitReply = async (reviewId) => {
    if (!replyText.trim() || replyText.length < 10) {
      toast.error('Yanıt en az 10 karakter olmalıdır');
      return;
    }

    try {
      await axios.put(`${API}/reviews/${reviewId}/response`, {
        response_text: replyText.trim()
      });
      toast.success('Yanıtınız gönderildi');
      setReplyingTo(null);
      setReplyText('');
      fetchReviews();
    } catch (error) {
      console.error('Error submitting reply:', error);
      toast.error('Yanıt gönderilemedi');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        {[...Array(3)].map((_, i) => (
          <Card key={i}>
            <CardContent className="p-6">
              <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
              <div className="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <Card>
        <CardContent className="p-12 text-center">
          <MessageSquare className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Henüz yorum yok
          </h3>
          <p className="text-gray-500">
            Bu otel için ilk yorumu siz yapın!
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Section */}
      <Card>
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Average Rating */}
            <div className="text-center md:text-left">
              <div className="flex flex-col md:flex-row items-center space-x-0 md:space-x-4">
                <div className="text-5xl font-bold text-indigo-600 mb-2 md:mb-0">
                  {averageRating.toFixed(1)}
                </div>
                <div>
                  <StarRating rating={averageRating} size="lg" showNumber={false} />
                  <p className="text-sm text-gray-600 mt-1">
                    {totalReviews} değerlendirme
                  </p>
                </div>
              </div>
            </div>

            {/* Rating Distribution */}
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map((star) => {
                const count = ratingDistribution[star] || 0;
                const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;
                
                return (
                  <div key={star} className="flex items-center space-x-2">
                    <span className="text-sm font-medium w-8">{star} ⭐</span>
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-yellow-400 rounded-full transition-all duration-300"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-8 text-right">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sort Options */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Tüm Yorumlar ({totalReviews})
        </h3>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
          <option value="created_at">En Yeni</option>
          <option value="rating">En Yüksek Puan</option>
          <option value="helpful_count">En Yararlı</option>
        </select>
      </div>

      {/* Reviews List */}
      <div className="space-y-4">
        {reviews.map((review) => (
          <Card key={review.id} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              {/* Review Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-start space-x-3">
                  <div className="h-12 w-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg">
                    {review.user_name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-semibold text-gray-900">{review.user_name}</h4>
                      {review.is_verified && (
                        <CheckCircle className="h-4 w-4 text-green-500" title="Doğrulanmış Rezervasyon" />
                      )}
                    </div>
                    <div className="flex items-center space-x-2 mt-1">
                      <StarRating rating={review.rating} size="sm" showNumber={false} />
                      <span className="text-xs text-gray-500 flex items-center">
                        <Calendar className="h-3 w-3 mr-1" />
                        {formatDate(review.created_at)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Review Content */}
              <div className="space-y-3">
                <p className="text-gray-700 leading-relaxed">{review.comment}</p>

                {review.pros && (
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <p className="text-sm text-green-800">
                      <strong>➕ Olumlu:</strong> {review.pros}
                    </p>
                  </div>
                )}

                {review.cons && (
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <p className="text-sm text-red-800">
                      <strong>➖ Geliştirilmeli:</strong> {review.cons}
                    </p>
                  </div>
                )}
              </div>

              {/* Hotel Response */}
              {review.hotel_response && (
                <div className="mt-4 ml-4 pl-4 border-l-2 border-indigo-300 bg-indigo-50 p-4 rounded">
                  <div className="flex items-center space-x-2 mb-2">
                    <Reply className="h-4 w-4 text-indigo-600" />
                    <span className="font-semibold text-indigo-900">Otelden Yanıt</span>
                    <span className="text-xs text-indigo-600">
                      {formatDate(review.hotel_response_date)}
                    </span>
                  </div>
                  <p className="text-sm text-indigo-800">{review.hotel_response}</p>
                </div>
              )}

              {/* Reply Form for Hotel Manager */}
              {user && (user.role === 'hotel_manager' || user.role === 'admin') && !review.hotel_response && (
                <div className="mt-4">
                  {replyingTo === review.id ? (
                    <div className="space-y-2">
                      <textarea
                        value={replyText}
                        onChange={(e) => setReplyText(e.target.value)}
                        placeholder="Yoruma yanıt verin..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none"
                        rows={3}
                        minLength={10}
                        maxLength={500}
                      />
                      <div className="flex space-x-2">
                        <Button
                          onClick={() => handleSubmitReply(review.id)}
                          size="sm"
                          className="bg-indigo-600 hover:bg-indigo-700"
                        >
                          Gönder
                        </Button>
                        <Button
                          onClick={() => {
                            setReplyingTo(null);
                            setReplyText('');
                          }}
                          variant="outline"
                          size="sm"
                        >
                          İptal
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <Button
                      onClick={() => setReplyingTo(review.id)}
                      variant="outline"
                      size="sm"
                      className="mt-2"
                    >
                      <Reply className="h-4 w-4 mr-2" />
                      Yanıtla
                    </Button>
                  )}
                </div>
              )}

              {/* Helpful Button */}
              <div className="mt-4 pt-4 border-t border-gray-200 flex items-center justify-between">
                <button
                  onClick={() => handleMarkHelpful(review.id)}
                  className="flex items-center space-x-2 text-sm text-gray-600 hover:text-indigo-600 transition-colors"
                >
                  <ThumbsUp className="h-4 w-4" />
                  <span>Yararlı ({review.helpful_count})</span>
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ReviewList;
