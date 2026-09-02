// frontend/src/components/TextInput.jsx

export default function TextInput({ text, setText }) {
  return (
    <div>
      <label>Enter text to scan:</label>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
        placeholder="Paste text containing names, phone numbers, CNIC, etc."
        style={{ width: "100%" }}
      />
    </div>
  );
}