/**
 * client.js — API client for the Sales Intelligence Pipeline backend.
 */

const API_BASE = 'http://localhost:8000';

/**
 * Run the full pipeline with the given inputs.
 * @param {Object} inputs - Pipeline inputs
 * @returns {Promise<Object>} Pipeline response with battle_card
 */
export async function runPipeline(inputs) {
  const response = await fetch(`${API_BASE}/run-pipeline`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(inputs),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Upload product documentation for RAG.
 * @param {string} text - Document text
 * @param {string} source - Source label
 * @returns {Promise<Object>}
 */
export async function uploadDocs(text, source = 'manual_upload') {
  const response = await fetch(`${API_BASE}/upload-docs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, source }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Load mock product docs into ChromaDB.
 * @returns {Promise<Object>}
 */
export async function loadMockDocs() {
  const response = await fetch(`${API_BASE}/load-mock-docs`, {
    method: 'POST',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Health check.
 * @returns {Promise<Object>}
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}
