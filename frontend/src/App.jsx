// frontend/src/App.jsx

import { useState } from "react";
import TextInput from "./components/TextInput";
import StrategySelector from "./components/StrategySelector";
import ResultView from "./components/ResultView";
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

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto" }}>
      <h1>Sentinel-PII</h1>
      <TextInput text={text} setText={setText} />
      <StrategySelector strategy={strategy} setStrategy={setStrategy} />
      <button onClick={handleSubmit} disabled={loading || !text}>
        {loading ? "Scanning..." : "Anonymize"}
      </button>
      <ResultView result={result} />
    </div>
  );
}