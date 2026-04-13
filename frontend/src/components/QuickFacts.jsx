export default function QuickFacts({ companyData, productData, inputs }) {
  if (!companyData) return null;

  const facts = [
    { label: 'Headquarters', value: companyData.headquarters, icon: '📍' },
    { label: 'Employees', value: companyData.employee_count, icon: '👥' },
    { label: 'Founded', value: companyData.year_founded, icon: '📅' },
    { label: 'Total Funding', value: companyData.total_funding, icon: '💰' },
    { label: 'Products', value: companyData.all_products?.length ? `${companyData.all_products.length} products` : 'Not Found', icon: '📦' },
    { label: 'Free Tier', value: productData?.has_free_tier ? '✅ Yes' : '❌ No', icon: '🆓' },
    { label: 'Trial', value: productData?.free_trial_duration || 'Not Found', icon: '⏱️' },
  ];

  return (
    <div className="card-container flex flex-col h-full border-t-4 border-t-slate-800">
      <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
        <span className="w-2.5 h-2.5 rounded-full bg-slate-800 shrink-0" />
        Quick Facts
      </h3>

      <div className="grid grid-cols-2 gap-4 mb-8">
        {facts.map((fact, i) => (
          <div key={i} className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors">
            <span className="text-xl shrink-0 leading-none">{fact.icon}</span>
            <div className="flex flex-col">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">{fact.label}</span>
              <span className="text-sm font-semibold text-slate-800 leading-tight">{fact.value || 'Not Found'}</span>
            </div>
          </div>
        ))}
      </div>

      {companyData.funding_rounds?.length > 0 && (
        <div className="mb-8">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 border-b border-slate-100 pb-2">Recent Funding</h4>
          <div className="space-y-3">
            {companyData.funding_rounds.map((round, i) => (
              <div key={i} className="flex flex-col p-3 bg-indigo-50 border border-indigo-100/50 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 text-xs font-bold rounded uppercase tracking-wider">
                    {round.round_name}
                  </span>
                  <span className="text-sm font-bold text-slate-800">{round.amount}</span>
                </div>
                {round.lead_investors?.length > 0 && (
                  <span className="text-xs text-slate-500">
                    <strong className="text-slate-600">Lead:</strong> {round.lead_investors.join(', ')}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {companyData.all_products?.length > 0 && (
        <div className="mt-auto">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 border-b border-slate-100 pb-2">Product Ecosystem</h4>
          <div className="flex flex-wrap gap-2">
            {companyData.all_products.map((product, i) => (
              <span key={i} className="px-2.5 py-1 bg-slate-100 border border-slate-200 text-slate-700 text-xs font-medium rounded-md">
                {product}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
