import { useState } from 'react';

const CATEGORIES = [
  { value: 'Software', label: '💻 Software' },
  { value: 'Physical', label: '📦 Physical Product' },
  { value: 'Course', label: '🎓 Course / Education' },
  { value: 'Entertainment', label: '🎮 Entertainment' },
];

export default function InputForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    name: '',
    url: '',
    target_product: '',
    category: 'Software',
    focus_area: '',
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.url || !formData.target_product) return;
    onSubmit(formData);
  };

  const isValid = formData.name && formData.url && formData.target_product;

  return (
    <form className="card-container" onSubmit={handleSubmit}>
      <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-slate-100">
        <div className="h-10 w-10 flex items-center justify-center rounded-lg bg-blue-50 text-blue-600">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <div>
          <h2 className="text-lg font-bold text-slate-900">Competitor Research</h2>
          <p className="text-sm text-slate-500">Run the intelligence pipeline</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Competitor Name *</label>
          <input
            name="name"
            type="text"
            className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow outline-none text-slate-900"
            placeholder="e.g., Slack"
            value={formData.name}
            onChange={handleChange}
            required
            disabled={isLoading}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Target Product *</label>
          <input
            name="target_product"
            type="text"
            className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow outline-none text-slate-900"
            placeholder="e.g., Slack Pro"
            value={formData.target_product}
            onChange={handleChange}
            required
            disabled={isLoading}
          />
        </div>

        <div className="space-y-2 md:col-span-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Product URL *</label>
          <input
            name="url"
            type="url"
            className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow outline-none text-slate-900"
            placeholder="https://competitor.com/product"
            value={formData.url}
            onChange={handleChange}
            required
            disabled={isLoading}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Category *</label>
          <select
            name="category"
            className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow outline-none bg-white text-slate-900"
            value={formData.category}
            onChange={handleChange}
            disabled={isLoading}
          >
            {CATEGORIES.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Focus Area</label>
          <input
            name="focus_area"
            type="text"
            className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow outline-none text-slate-900"
            placeholder="e.g., enterprise security"
            value={formData.focus_area}
            onChange={handleChange}
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="mt-8">
        <button
          type="submit"
          className="w-full h-12 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2 shadow-sm"
          disabled={!isValid || isLoading}
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              Generate Report
              <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </>
          )}
        </button>
      </div>
    </form>
  );
}
