import { useEffect, useState } from 'react';

const PIPELINE_STEPS = [
  { label: 'Classifying category & sources', icon: '🏷️', delay: 0 },
  { label: 'Profiling company intelligence', icon: '🏢', delay: 8 },
  { label: 'Analyzing product deep-dive', icon: '🔍', delay: 20 },
  { label: 'Scraping reviews & sentiment', icon: '📝', delay: 35 },
  { label: 'Running RAG comparison', icon: '⚔️', delay: 50 },
  { label: 'Compiling Intelligence Report', icon: '📋', delay: 65 },
];

export default function LoadingOverlay({ isVisible }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!isVisible) {
      setCurrentStep(0);
      setElapsed(0);
      return;
    }

    const timer = setInterval(() => {
      setElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [isVisible]);

  useEffect(() => {
    if (!isVisible) return;

    // Advance steps based on elapsed time
    const nextStep = PIPELINE_STEPS.findIndex(
      (step) => step.delay > elapsed
    );
    if (nextStep === -1) {
      setCurrentStep(PIPELINE_STEPS.length - 1);
    } else if (nextStep > 0) {
      setCurrentStep(nextStep - 1);
    }
  }, [elapsed, isVisible]);

  if (!isVisible) return null;

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return m > 0 ? `${m}m ${sec}s` : `${sec}s`;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
      <div className="bg-white border border-slate-200 rounded-2xl shadow-xl w-full max-w-md p-8 flex flex-col items-center">
        
        {/* Spinner */}
        <div className="relative w-24 h-24 flex items-center justify-center mb-6">
          <div className="absolute inset-0 rounded-full border-4 border-slate-100 border-t-blue-600 animate-spin" />
          <span className="text-3xl relative z-10">
            {PIPELINE_STEPS[currentStep]?.icon}
          </span>
        </div>

        <h2 className="text-xl font-bold text-slate-900 mb-1">Generating Intelligence Report</h2>
        <p className="text-sm font-medium text-slate-500 mb-8">
          This typically takes 60–120 seconds
        </p>

        {/* Steps List */}
        <div className="w-full space-y-3">
          {PIPELINE_STEPS.map((step, i) => {
            const isDone = i < currentStep;
            const isActive = i === currentStep;
            const isPending = i > currentStep;

            return (
              <div
                key={i}
                className={`flex items-center gap-4 p-2 rounded-lg transition-colors ${
                  isActive ? 'bg-blue-50' : ''
                }`}
              >
                <div className="w-6 flex justify-center items-center shrink-0">
                  {isDone ? (
                    <svg className="w-5 h-5 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : isActive ? (
                    <div className="w-2.5 h-2.5 bg-blue-600 rounded-full animate-ping" />
                  ) : (
                    <div className="w-1.5 h-1.5 bg-slate-200 rounded-full" />
                  )}
                </div>
                <span className={`text-sm font-medium ${
                  isDone ? 'text-slate-500 line-through' :
                  isActive ? 'text-blue-700 font-bold' :
                  'text-slate-400'
                }`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>

        {/* Timer */}
        <div className="mt-8 px-4 py-2 bg-slate-50 border border-slate-100 rounded-full flex items-center gap-2">
          <span className="text-lg">⏱</span>
          <span className="text-sm font-bold text-slate-700 tracking-wider">
            {formatTime(elapsed)}
          </span>
        </div>
      </div>
    </div>
  );
}
