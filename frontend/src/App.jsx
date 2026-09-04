import { useState } from "react";
import "./App.css";
import { anonymizeText } from "./api";

export default function App() {
  const [text, setText] = useState("");
  const [strategy, setStrategy] = useState("replace");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    try {
      const data = await anonymizeText(text, strategy);
      setResult(data);
    } catch (error) {
      console.error("Anonymization failed:", error);
      alert("Something went wrong — check the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  // Renders <REDACTED> tokens as solid black bars instead of plain text
  function renderRedacted(anonymizedText) {
    const parts = anonymizedText.split(/(<REDACTED>)/g);
    return parts.map((part, i) =>
      part === "<REDACTED>" ? (
        <span key={i} className="result__redacted">
          REDACTED
        </span>
      ) : (
        <span key={i}>{part}</span>
      )
    );
  }

  return (
    <div className="case-file">
      <div className="case-file__header">
        <h1 className="case-file__title">Sentinel-PII</h1>
        <div className="case-file__subtitle">CASE FILE // PII DETECTION &amp; REDACTION</div>
      </div>

      <div className="case-file__card">
        <label className="field-label" htmlFor="scan-text">
          Text to scan
        </label>
        <textarea
          id="scan-text"
          className="case-file__textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste text containing names, phone numbers, CNIC, etc."
        />

        <div className="case-file__row">
          <select
            className="case-file__select"
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
          >
            <option value="replace">Replace with label</option>
            <option value="mask">Mask with asterisks</option>
            <option value="hash">Hash</option>
          </select>

          <button
            className="case-file__button"
            onClick={handleSubmit}
            disabled={loading || !text}
          >
            {loading ? "Scanning..." : "Anonymize"}
          </button>
        </div>

        {result && (
          <div className="result">
            <div className="result__label">REDACTED OUTPUT</div>
            <div className="result__text">
              {renderRedacted(result.anonymized_text)}
            </div>
            <div className="result__count">
              {result.entities_found} entities detected
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
