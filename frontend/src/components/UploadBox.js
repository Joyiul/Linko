export default function UploadBox({ setFile }) {
  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
    </div>
  );
}
