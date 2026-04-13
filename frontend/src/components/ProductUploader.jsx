import { useState, useRef } from 'react';
import { uploadDocs } from '../api/client';

const TEMPLATE_CONTENT = `[Product Name] Overview:
(Describe your product here...)

Target Audience:
(Who is this product for?)

Pricing Tiers:
- Starter: (Price) - (Features)
- Pro: (Price) - (Features)
- Custom/Enterprise: (Details)

Key Features:
- (Feature 1)
- (Feature 2)
- (Feature 3)

Limitations or Weaknesses (Be honest):
- (Limitation 1)
- (Limitation 2)

Customer Support SLAs:
(E.g., 24/7 support, 4-hour response time...)
`;

export default function ProductUploader() {
  const [status, setStatus] = useState('idle');
  const [message, setMessage] = useState('');
  const fileInputRef = useRef(null);

  const handleDownloadTemplate = () => {
    const blob = new Blob([TEMPLATE_CONTENT], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'our_product_template.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setStatus('uploading');
    setMessage('Reading file...');

    try {
      const text = await file.text();
      setMessage('Ingesting data into knowledge base...');
      
      const response = await uploadDocs(text, 'user_template_upload');
      
      setStatus('success');
      setMessage(`Successfully loaded ${response.total_documents} chunks into the database.`);
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Failed to upload document.');
    } finally {
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="card-container">
      <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-slate-100">
        <div className="h-10 w-10 flex items-center justify-center rounded-lg bg-emerald-50 text-emerald-600">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
          </svg>
        </div>
        <div>
          <h2 className="text-lg font-bold text-slate-900">Our Product Configuration</h2>
          <p className="text-sm text-slate-500">Upload your product specs for comparison</p>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center gap-4">
        <button 
          className="flex-1 sm:flex-none inline-flex justify-center items-center gap-2 px-6 py-2.5 bg-white border border-slate-300 hover:bg-slate-50 hover:border-slate-400 text-slate-700 font-medium rounded-lg transition-colors focus:ring-2 focus:ring-emerald-500 focus:outline-none disabled:opacity-50"
          onClick={handleDownloadTemplate}
          disabled={status === 'uploading'}
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download Template
        </button>

        <input 
          type="file" 
          accept=".txt,.md"
          onChange={handleFileChange}
          ref={fileInputRef}
          disabled={status === 'uploading'}
          className="hidden"
        />
        
        <button 
          className="flex-1 sm:flex-none inline-flex justify-center items-center gap-2 px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-lg transition-colors focus:ring-2 focus:ring-emerald-500 focus:outline-none disabled:opacity-50"
          onClick={() => fileInputRef.current?.click()}
          disabled={status === 'uploading'}
        >
          {status === 'uploading' ? (
             <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          )}
          Upload Completed File
        </button>
      </div>

      {message && (
        <div className={`mt-4 p-3 rounded-lg text-sm font-medium border ${
          status === 'success' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 
          status === 'error' ? 'bg-red-50 text-red-700 border-red-200' : 
          'bg-slate-50 text-slate-600 border-slate-200'
        }`}>
          {message}
        </div>
      )}
    </div>
  );
}
