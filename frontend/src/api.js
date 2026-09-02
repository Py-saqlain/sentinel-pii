// frontend/src/api.js

import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function anonymizeText(text, strategy) {
  const response = await axios.post(`${API_BASE_URL}/anonymize`, {
    text: text,
    strategy: strategy,
  });
  return response.data;
}