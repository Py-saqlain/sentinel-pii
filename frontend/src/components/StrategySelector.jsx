// frontend/src/components/StrategySelector.jsx

export default function StrategySelector({ strategy, setStrategy }) {
  return (
    <div>
      <label>Anonymization strategy:</label>
      <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
        <option value="replace">Replace with label</option>
        <option value="mask">Mask with asterisks</option>
        <option value="hash">Hash</option>
      </select>
    </div>
  );
}