export default function ZipCodeInput({ UpdateZipCode }) {
  function NotifyChange(evt) {
    UpdateZipCode(evt.target.value);
  }

  return (
    <div>
      <input onChange={NotifyChange} placeholder="Código postal" />
    </div>
  );
}
