export default function HighlightedText({ text }) {
  const highlights = ["whatever", "really", "like", "dude", "bro"];
  const parts = text.split(new RegExp(`(${highlights.join("|")})`, "gi"));

  return (
    <p>
      {parts.map((part, i) =>
        highlights.includes(part.toLowerCase()) ? (
          <span key={i} style={{ backgroundColor: "yellow" }}>{part}</span>
        ) : (
          part
        )
      )}
    </p>
  );
}
