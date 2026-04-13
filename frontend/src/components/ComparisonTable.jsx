export default function ComparisonTable({ comparison }) {
  if (!comparison) return null;

  const { wins = [], losses = [], neutral = [], win_rate = 0 } = comparison;
  const ragAvailable = comparison.rag_context_available;
  const winPercent = Math.round(win_rate * 100);

  const renderScorecardRow = (item, type) => {
    const isWin = type === 'win';
    
    // Impact styles
    const impactColors = {
      High: isWin ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-rose-100 text-rose-800 border-rose-200',
      Medium: 'bg-amber-100 text-amber-800 border-amber-200',
      Low: 'bg-slate-100 text-slate-800 border-slate-200'
    };
    const impactClass = impactColors[item.impact] || impactColors.Low;

    return (
      <div key={item.area + type} className="flex flex-col bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow mb-6">
        
        {/* Header Block (Area & Impact) */}
        <div className={`px-5 py-3 border-b flex justify-between items-center ${isWin ? 'bg-emerald-50/50 border-emerald-100' : 'bg-rose-50/50 border-rose-100'}`}>
          <h4 className="font-bold text-slate-900 text-lg flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isWin ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
            {item.area}
          </h4>
          <span className={`px-2.5 py-1 text-xs font-bold uppercase tracking-wider rounded-md border ${impactClass}`}>
            {item.impact} Impact
          </span>
        </div>

        {/* Head-to-Head Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-100">
          
          {/* OUR PRODUCT */}
          <div className={`p-6 flex flex-col relative ${isWin ? 'bg-white' : 'bg-slate-50 opacity-80'}`}>
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Our Product</span>
              {isWin && <span className="text-2xl" title="Winner">👑</span>}
            </div>
            <p className="text-slate-800 text-[15px] leading-relaxed flex-1">{item.our_position}</p>
          </div>

          {/* THEIR PRODUCT */}
          <div className={`p-6 flex flex-col relative ${!isWin ? 'bg-white' : 'bg-slate-50 opacity-80'}`}>
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Competitor</span>
              {!isWin && <span className="text-2xl" title="Winner">👑</span>}
            </div>
            <p className="text-slate-800 text-[15px] leading-relaxed flex-1">{item.competitor_position}</p>
          </div>
        </div>

        {/* Evidence Footer */}
        {item.evidence && (
          <div className="bg-slate-50 border-t border-slate-100 px-6 py-3 flex gap-3 text-sm text-slate-600">
            <span className="shrink-0">📎</span>
            <span className="italic">{item.evidence}</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-12 max-w-4xl mx-auto">
      
      {/* Overview Dashboard */}
      <div className="card-container flex flex-col sm:flex-row justify-between items-center gap-6 bg-gradient-to-br from-white to-slate-50">
        <div>
          <h3 className="text-2xl font-bold text-slate-900 mb-2">Head-to-Head Scorecard</h3>
          {!ragAvailable ? (
            <p className="text-amber-600 text-sm font-medium flex items-center gap-2">
              <span>⚠️</span> No internal product specs provided. Comparison is generated using market assumptions.
            </p>
          ) : (
            <p className="text-emerald-600 text-sm font-medium flex items-center gap-2">
              <span>✅</span> Powered by RAG against your internal documentation.
            </p>
          )}
        </div>
        
        <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-slate-100">
          <div className="text-right">
            <div className={`text-4xl font-extrabold ${winPercent >= 50 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {winPercent}%
            </div>
            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Win Rate</div>
          </div>
        </div>
      </div>

      {/* Wins Block */}
      <div>
        <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b border-slate-200 pb-3">
          <span className="text-emerald-500">🛡️</span> Where We Win
        </h3>
        {wins.length === 0 ? (
          <div className="p-8 text-center text-slate-500 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50">
            No conclusive wins identified in this analysis.
          </div>
        ) : (
          <div>{wins.map(item => renderScorecardRow(item, 'win'))}</div>
        )}
      </div>

      {/* Losses Block */}
      <div>
        <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b border-slate-200 pb-3 mt-12">
          <span className="text-rose-500">🎯</span> Where They Outperform
        </h3>
        {losses.length === 0 ? (
          <div className="p-8 text-center text-slate-500 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50">
            No conclusive disadvantages identified.
          </div>
        ) : (
          <div>{losses.map(item => renderScorecardRow(item, 'loss'))}</div>
        )}
      </div>

    </div>
  );
}
