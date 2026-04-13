import { useState } from 'react';

export default function ObjectionAccordion({ tactics }) {
  const [flippedIndex, setFlippedIndex] = useState(null);

  if (!tactics) return null;

  const { objection_handlers = [], battle_card_snippets = [], elevator_pitch = '' } = tactics;

  return (
    <div className="space-y-12 max-w-5xl mx-auto">
      
      {/* Elevator Pitch Header */}
      {elevator_pitch && elevator_pitch !== 'Not Found' && (
        <div className="card-container bg-indigo-50/50 border-indigo-100 border-l-4 border-l-indigo-500">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">⏱️</span>
            <h4 className="text-lg font-bold text-slate-900">30-Second Elevator Pitch</h4>
          </div>
          <p className="text-slate-700 text-lg font-medium leading-relaxed">{elevator_pitch}</p>
        </div>
      )}

      {/* Flashcards Section */}
      <div>
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-slate-900">Questions They Might Ask</h3>
          <p className="text-slate-500 mt-1">Interactive field tactics. Click to reveal the recommended response.</p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {objection_handlers.map((handler, i) => {
            const isFlipped = flippedIndex === i;
            
            return (
              <div 
                key={i} 
                className="flip-card-perspective h-[320px] cursor-pointer group"
                onClick={() => setFlippedIndex(isFlipped ? null : i)}
              >
                <div 
                  className="flip-card-inner shadow-sm rounded-xl"
                  style={{ transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)' }}
                >
                  {/* Front: The Question (Light grayish white) */}
                  <div className="flip-card-front card-container bg-white flex flex-col justify-center items-center text-center group-hover:border-blue-300 transition-colors">
                    <div className="absolute top-4 left-4">
                      <span className="px-2.5 py-1 bg-rose-100 text-rose-700 text-xs font-bold uppercase tracking-wider rounded-md">Expected Question</span>
                    </div>
                    <div className="absolute top-4 right-4 text-slate-200 text-4xl font-serif">"</div>
                    <h4 className="text-xl font-bold text-slate-800 px-6 leading-tight">
                      {handler.objection}
                    </h4>
                    <span className="absolute bottom-4 text-xs font-bold uppercase tracking-widest text-slate-400 animate-pulse flex items-center gap-1">
                      Click to flip <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" /></svg>
                    </span>
                  </div>

                  {/* Back: The Response (Soft Emerald/Mint) */}
                  <div className="flip-card-back card-container bg-gradient-to-br from-emerald-50 to-white border-emerald-200 overflow-y-auto flex flex-col">
                    <div className="mb-4">
                      <span className="px-2.5 py-1 bg-emerald-100 text-emerald-700 text-xs font-bold uppercase tracking-wider rounded-md">Tactical Response</span>
                    </div>
                    
                    <p className="text-slate-800 text-[15px] leading-relaxed mb-4">
                      {handler.response}
                    </p>
                    
                    {handler.supporting_data && (
                      <div className="mt-auto p-3 bg-white/60 border border-emerald-100 rounded-lg flex items-start gap-3">
                        <span className="text-lg">📊</span>
                        <div className="text-sm font-medium text-emerald-900 leading-snug">
                          {handler.supporting_data}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Snippets Grid */}
      {battle_card_snippets.length > 0 && (
        <div className="pt-8 border-t border-slate-200">
          <h3 className="text-xl font-bold text-slate-900 mb-6">Quick Talking Points</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {battle_card_snippets.map((snippet, i) => (
              <div key={i} className="card-container border-t-4 border-t-blue-500 hover:-translate-y-1 transition-transform">
                <div className="flex flex-col gap-3 mb-3">
                  <span className="self-start px-2 py-0.5 bg-blue-50 text-blue-700 text-[10px] font-bold uppercase tracking-widest rounded border border-blue-100">
                    {snippet.category}
                  </span>
                  <h4 className="text-[15px] font-bold text-slate-900 leading-snug">{snippet.title}</h4>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed">{snippet.snippet}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
