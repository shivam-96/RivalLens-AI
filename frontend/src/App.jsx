import { useState } from 'react';
import InputForm from './components/InputForm';
import ProductUploader from './components/ProductUploader';
import BattleCard from './components/BattleCard';
import LoadingOverlay from './components/LoadingOverlay';
import { runPipeline } from './api/client';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [battleCard, setBattleCard] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (inputs) => {
    setIsLoading(true);
    setError(null);
    setBattleCard(null);

    try {
      const result = await runPipeline(inputs);
      if (result.status === 'success' && result.battle_card) {
        setBattleCard(result.battle_card);
      } else {
        setError('Pipeline returned an unexpected response.');
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to the backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setBattleCard(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 relative">
      <LoadingOverlay isVisible={isLoading} />

      {/* Hero Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">⚔️</span>
            <div>
              <h1 className="text-xl font-bold text-slate-900 leading-tight">Competitive Intelligence Platform</h1>
              <p className="text-sm text-slate-500">Zero-research competitor analysis</p>
            </div>
          </div>
          {battleCard && (
            <button 
              onClick={handleReset}
              className="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors flex items-center gap-2"
            >
              <span>←</span> Start New Analysis
            </button>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Error Alert */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-3">
            <span className="text-red-500">❌</span>
            <p className="text-red-700 text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Conditional Rendering: Show Builder OR Results */}
        {!battleCard ? (
          <div className="max-w-3xl mx-auto space-y-8 animate-fade-in my-8">
            <div className="text-center space-y-3 mb-10">
              <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Generate an Intelligence Report</h2>
              <p className="text-lg text-slate-600">Enter a competitor and get a complete tactical breakdown in seconds.</p>
            </div>
            <ProductUploader />
            <InputForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
        ) : (
          <div className="animate-fade-in">
            <BattleCard data={battleCard} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
