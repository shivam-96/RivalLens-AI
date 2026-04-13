import { useState } from 'react';

const TABS = [
  { key: 'positive', label: 'Positive Resonance', icon: '👍' },
  { key: 'negative', label: 'Critical Pain Points', icon: '👎' },
  { key: 'youtube', label: 'Video Analysis', icon: '🎬' },
];

export default function ReviewsPanel({ reviews }) {
  const [activeTab, setActiveTab] = useState('positive');

  if (!reviews) return null;

  const {
    top_positive_reviews: positive = [],
    top_negative_reviews: negative = [],
    youtube_summaries: youtube = [],
    overall_sentiment,
    sentiment_label
  } = reviews;

  // We use Tailwind's CSS Columns for masonry layout.
  // Tailwind handles this beautifully with "columns-1 md:columns-2"
  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      
      {/* Sentiment Header */}
      <div className="card-container bg-indigo-50/30 border-indigo-100 flex flex-col sm:flex-row justify-between items-center gap-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-900 mb-1">Voice of Customer</h3>
          <p className="text-slate-600">
            Overall Sentiment: <span className="font-bold text-indigo-900">{sentiment_label}</span>
          </p>
        </div>
        <div className="bg-white px-6 py-4 rounded-xl shadow-sm border border-indigo-100 flex items-center justify-center">
           <span className={`text-4xl font-extrabold ${overall_sentiment > 0.1 ? 'text-emerald-500' : overall_sentiment < -0.1 ? 'text-rose-500' : 'text-amber-500'}`}>
             {overall_sentiment > 0 ? '+' : ''}{overall_sentiment?.toFixed(2)}
           </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-3">
        {TABS.map((tab) => {
          const count =
            tab.key === 'positive'
              ? positive.length
              : tab.key === 'negative'
              ? negative.length
              : youtube.length;

          const isActive = activeTab === tab.key;

          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold transition-all ${
                isActive 
                  ? 'bg-slate-900 text-white shadow-md' 
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300'
              }`}
            >
              <span className="text-lg">{tab.icon}</span>
              {tab.label}
              <span className={`px-2 py-0.5 rounded-full text-xs font-bold ml-1 ${
                isActive ? 'bg-slate-700 text-white' : 'bg-slate-100 text-slate-500'
              }`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Masonry Content Area */}
      <div className="animate-tab-enter" key={activeTab}>
        {activeTab === 'positive' && (
          <div className="columns-1 md:columns-2 gap-6 w-full">
            {positive.length === 0 ? (
              <p className="p-8 text-center text-slate-500 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 break-inside-avoid">No positive reviews found</p>
            ) : (
              positive.map((review, i) => <ReviewCard key={i} review={review} type="positive" index={i} />)
            )}
          </div>
        )}

        {activeTab === 'negative' && (
          <div className="columns-1 md:columns-2 gap-6 w-full">
            {negative.length === 0 ? (
              <p className="p-8 text-center text-slate-500 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 break-inside-avoid">No critical reviews found</p>
            ) : (
              negative.map((review, i) => <ReviewCard key={i} review={review} type="negative" index={i} />)
            )}
          </div>
        )}

        {activeTab === 'youtube' && (
          <div className="columns-1 md:columns-2 gap-6 w-full">
            {youtube.length === 0 ? (
              <p className="p-8 text-center text-slate-500 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 break-inside-avoid">No YouTube reviews found</p>
            ) : (
              youtube.map((video, i) => <YouTubeCard key={i} video={video} index={i} />)
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function ReviewCard({ review, type, index }) {
  const isPositive = type === 'positive';
  
  return (
    <div 
      className={`card-container break-inside-avoid mb-6 flex flex-col gap-4 relative overflow-hidden animate-fade-in border-t-4 ${isPositive ? 'border-t-emerald-400' : 'border-t-rose-400'}`}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="absolute top-[-20px] right-2 text-9xl font-serif text-slate-50 opacity-50 select-none">"</div>
      
      <div className="flex justify-between items-start relative z-10">
        <span className="px-2.5 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold uppercase tracking-widest rounded border border-slate-200">
          {review.source}
        </span>
        <span className={`text-lg font-bold ${review.sentiment_score > 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
          {review.sentiment_score > 0 ? '+' : ''}{review.sentiment_score?.toFixed(1)}
        </span>
      </div>
      
      <blockquote className="text-[15px] leading-relaxed text-slate-800 italic relative z-10 mb-2">
        "{review.verbatim_quote}"
      </blockquote>
      
      <div className="mt-auto pt-4 border-t border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs uppercase">
            {(review.author || 'A').charAt(0)}
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-bold text-slate-900">{review.author || 'Anonymous'}</span>
            {review.date && review.date !== 'Not Found' && (
              <span className="text-[11px] text-slate-500">{review.date}</span>
            )}
          </div>
        </div>
        {review.key_theme && (
          <span className="px-2.5 py-1 bg-violet-50 text-violet-700 text-[10px] font-bold uppercase tracking-widest rounded border border-violet-100">
            {review.key_theme}
          </span>
        )}
      </div>
    </div>
  );
}

function YouTubeCard({ video, index }) {
  return (
    <div 
      className="card-container break-inside-avoid mb-6 border-t-4 border-t-red-500 animate-fade-in"
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="flex justify-between items-center mb-4">
        <span className="px-2.5 py-1 bg-red-50 text-red-700 text-xs font-bold uppercase tracking-wider rounded border border-red-100 flex items-center gap-1">
          🎬 YouTube
        </span>
        <span className="text-xs font-bold text-slate-500 bg-slate-100 px-2 py-1 rounded">{video.channel_name}</span>
      </div>
      
      <h4 className="text-lg font-bold text-slate-900 leading-snug mb-4">{video.video_title}</h4>
      
      {video.key_points?.length > 0 && (
        <ul className="space-y-2 mb-6">
          {video.key_points.map((point, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
              <span className="text-red-400 mt-1 shrink-0">•</span>
              <span className="leading-relaxed">{point}</span>
            </li>
          ))}
        </ul>
      )}
      
      {video.overall_verdict && video.overall_verdict !== 'Not Found' && (
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 mb-4 border-l-4 border-l-slate-400">
          <strong className="text-slate-900 uppercase text-xs tracking-wider block mb-1">Verdict</strong> 
          {video.overall_verdict}
        </div>
      )}
      
      {video.video_url && (
        <a
          href={video.video_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center justify-center gap-2 w-full py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-sm rounded-lg transition-colors"
        >
          Watch Video <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
        </a>
      )}
    </div>
  );
}
