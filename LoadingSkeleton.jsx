const LoadingSkeleton = () => {
  return (
    <div className="crypto-card">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full loading-shimmer"></div>
          <div>
            <div className="h-5 w-16 loading-shimmer rounded mb-2"></div>
            <div className="h-4 w-24 loading-shimmer rounded"></div>
          </div>
        </div>
        <div className="flex gap-1">
          <div className="w-6 h-6 rounded-full loading-shimmer"></div>
          <div className="w-6 h-6 rounded-full loading-shimmer"></div>
        </div>
      </div>

      <div className="flex items-end justify-between">
        <div className="flex-1">
          <div className="h-8 w-32 loading-shimmer rounded mb-2"></div>
          <div className="flex items-center gap-2 mb-1">
            <div className="h-5 w-20 loading-shimmer rounded"></div>
            <div className="h-4 w-16 loading-shimmer rounded"></div>
          </div>
          <div className="h-3 w-12 loading-shimmer rounded"></div>
        </div>
        
        <div className="ml-4">
          <div className="w-20 h-10 loading-shimmer rounded"></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSkeleton;

