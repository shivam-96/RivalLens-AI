import { useState } from 'react';
import QuickFacts from './QuickFacts';
import SentimentMeter from './SentimentMeter';
import ComparisonTable from './ComparisonTable';
import ObjectionAccordion from './ObjectionAccordion';
import ReviewsPanel from './ReviewsPanel';

const TABS = [
  { id: 'summary', name: 'Executive Summary', icon: '📊' },
  { id: 'comparison', name: 'Head-to-Head', icon: '⚔️' },
  { id: 'reviews', name: 'Voice of Customer', icon: '🗣️' },
  { id: 'tactics', name: 'Field Strategy', icon: '🧠' },
];

export default function BattleCard({ data }) {
  const [activeTab, setActiveTab] = useState('summary');

  if (!data) return null;

  const {
    inputs,
    company_data,
    product_data,
    reviews,
    comparison,
    tactics,
    generated_at,
    classifier,
  } = data;

  const renderTabContent = () => {
    switch (activeTab) {
      case 'summary':
        return (
          <div className="space-y-8 animate-fade-in pb-16">
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <QuickFacts companyData={company_data} productData={product_data} inputs={inputs} />
              <SentimentMeter reviews={reviews} />
            </div>

            {/* Pricing Tiers Bar */}
            {product_data?.pricing_tiers?.length > 0 && (
              <div className="card-container border-t-4 border-t-emerald-500">
                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                  <span>💳</span> Pricing Tiers
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                  {product_data.pricing_tiers.map((tier, i) => (
                    <div key={i} className="p-6 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-300 transition-colors">
                      <span className="block text-lg font-bold text-slate-900 mb-1">{tier.tier_name}</span>
                      <span className="block text-3xl font-extrabold text-emerald-600 mb-1">{tier.price}</span>
                      <span className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">{tier.billing_model}</span>
                      
                      {tier.key_features?.length > 0 && (
                        <ul className="space-y-2 pt-4 border-t border-slate-200">
                          {tier.key_features.slice(0, 4).map((f, j) => (
                            <li key={j} className="text-sm text-slate-600 flex items-start gap-2">
                              <span className="text-emerald-500 font-bold shrink-0">✓</span>
                              <span>{f}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Hidden Frictions */}
            {product_data?.hidden_frictions?.length > 0 && (
              <div className="card-container border-t-4 border-t-rose-500">
                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                  <span>⚠️</span> Hidden Frictions
                </h3>
                <div className="space-y-4">
                  {product_data.hidden_frictions.map((f, i) => (
                    <div key={i} className="flex flex-col sm:flex-row sm:items-start gap-4 p-5 bg-rose-50 border border-rose-100 rounded-xl">
                      <span className="text-xl shrink-0 mt-0.5">🔴</span>
                      <div>
                        <p className="text-base font-medium text-rose-900 mb-2">{f.friction}</p>
                        <span className="text-xs font-semibold text-rose-500 uppercase tracking-widest">Source: {f.source}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      case 'comparison':
        return (
          <div className="animate-fade-in pb-16">
            <ComparisonTable comparison={comparison} />
          </div>
        );
      case 'reviews':
        return (
          <div className="animate-fade-in pb-16">
            <ReviewsPanel reviews={reviews} />
          </div>
        );
      case 'tactics':
        return (
          <div className="animate-fade-in pb-16">
            <ObjectionAccordion tactics={tactics} />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="w-full">
      {/* Competitor Header */}
      <div className="bg-white border-b border-slate-200 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold rounded-full mb-3 uppercase tracking-wider border border-blue-100">
                {classifier?.category_label}
              </span>
              <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
                {inputs?.name}
                <span className="text-blue-600 font-medium"> — {inputs?.target_product}</span>
              </h1>
              {company_data?.website_description && company_data.website_description !== 'Not Found' && (
                <p className="mt-3 text-slate-600 max-w-3xl leading-relaxed">
                  {company_data.website_description}
                </p>
              )}
            </div>
            
            <div className="text-left md:text-right flex flex-col shrink-0">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Generated</span>
              <span className="text-sm font-medium text-slate-700 bg-slate-100 px-3 py-1 rounded-md">
                {generated_at ? new Date(generated_at).toLocaleString() : 'N/A'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Sticky Top Navbar */}
      <div className="bg-white border-b border-slate-200 sticky top-[73px] z-40 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1 overflow-x-auto py-2 scrollbar-none">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-5 py-3 rounded-lg text-sm font-bold whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-50 text-blue-700 shadow-sm border border-blue-100'
                    : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <span className="text-lg">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderTabContent()}
      </div>

    </div>
  );
}
