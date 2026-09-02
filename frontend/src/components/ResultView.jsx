// frontend/src/components/ResultView.jsx

export default function ResultView({ result }) {
  if (!result) return null;

  return (
    <div>
      <h3>Anonymized Output</h3>
      <p>{result.anonymized_text}</p>
      <small>{result.entities_found} entities detected</small>
    </div>
  );
}