import React from 'react';
import { Star } from 'lucide-react';

const StarRating = ({ 
  rating, 
  maxRating = 5, 
  size = 'md', 
  interactive = false, 
  onChange = null,
  showNumber = true 
}) => {
  const sizeClasses = {
    sm: 'h-3 w-3',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
    xl: 'h-8 w-8'
  };

  const handleClick = (value) => {
    if (interactive && onChange) {
      onChange(value);
    }
  };

  return (
    <div className="flex items-center space-x-1">
      {[...Array(maxRating)].map((_, index) => {
        const starValue = index + 1;
        const isFilled = starValue <= rating;
        const isHalfFilled = starValue - 0.5 === rating;

        return (
          <button
            key={index}
            type="button"
            onClick={() => handleClick(starValue)}
            disabled={!interactive}
            className={`${interactive ? 'cursor-pointer hover:scale-110 transition-transform' : 'cursor-default'} focus:outline-none`}
          >
            <Star
              className={`${sizeClasses[size]} ${
                isFilled
                  ? 'fill-yellow-400 text-yellow-400'
                  : isHalfFilled
                  ? 'fill-yellow-400 text-yellow-400'
                  : 'fill-gray-200 text-gray-300'
              }`}
            />
          </button>
        );
      })}
      {showNumber && (
        <span className="ml-2 text-sm font-medium text-gray-700">
          {rating > 0 ? rating.toFixed(1) : 'Henüz değerlendirilmedi'}
        </span>
      )}
    </div>
  );
};

export default StarRating;
