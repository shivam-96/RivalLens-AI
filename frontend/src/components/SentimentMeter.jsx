export default function SentimentMeter({ reviews }) {
  if (!reviews) return null;

  const { overall_sentiment = 0, sentiment_label = 'Neutral', total_reviews_analyzed = 0 } = reviews;

  // normalize -1 to 1 into 0 to 100 for visual gauge
  const percentage = ((overall_sentiment + 1) / 2) * 100;
  
  // Decide color scale
  const isPositive = overall_sentiment > 0.1;
  const isNegative = overall_sentiment < -0.1;
  const colorClass = isPositive ? 'text-emerald-600' : isNegative ? 'text-rose-600' : 'text-amber-500';
  const bgClass = isPositive ? 'bg-emerald-50 border-emerald-200' : isNegative ? 'bg-rose-50 border-rose-200' : 'bg-amber-50 border-amber-200';

  return (
    <div className="card-container flex flex-col h-full border-t-4 border-t-blue-500">
      <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
        <span className="w-2.5 h-2.5 rounded-full bg-blue-500 shrink-0" />
        Brand Sentiment
      </h3>

      <div className={`mt-4 mb-10 flex flex-col items-center justify-center py-8 rounded-2xl border ${bgClass}`}>
        <div className={`text-6xl font-extrabold tracking-tighter mb-2 ${colorClass}`}>
          {overall_sentiment > 0 ? '+' : ''}{overall_sentiment.toFixed(2)}
        </div>
        <div className={`text-sm font-bold uppercase tracking-widest ${colorClass} opacity-80`}>
          {sentiment_label}
        </div>
      </div>

      <div className="w-full mb-8 px-4">
        <div className="relative h-3 w-full bg-slate-200 rounded-full overflow-hidden flex">
          <div className="h-full bg-rose-500 w-1/3" />
          <div className="h-full bg-amber-400 w-1/3" />
          <div className="h-full bg-emerald-500 w-1/3" />
          
          {/* Market indicator */}
          <div 
            className="absolute top-0 bottom-0 w-2 bg-slate-900 rounded-full border-2 border-white shadow-sm transition-all duration-1000 ease-out"
            style={{ left: `calc(${percentage}% - 4px)` }}
          />
        </div>
        <div className="flex justify-between mt-2 text-xs font-bold text-slate-400 uppercase">
          <span>Negative</span>
          <span>Neutral</span>
          <span>Positive</span>
        </div>
      </div>

      <div className="mt-auto px-4 py-3 bg-slate-50 rounded-lg flex items-center justify-between border border-slate-100">
        <span className="text-sm font-medium text-slate-600">Sample Size Analyzed</span>
        <span className="text-black font-bold badge bg-white border border-slate-200 px-3 py-1 rounded-md shadow-sm">
          {total_reviews_analyzed} sources
        </span>
      </div>
    </div>
  );
}
