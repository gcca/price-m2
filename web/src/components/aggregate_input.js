export default function AggregateInput({ UpdateAggregate }) {
  function NotifyChange(evt) {
    UpdateAggregate(evt.target.value);
  }

  return (
    <form>
      <span>
        <input type="radio" name="aggregate" value="avg" onChange={NotifyChange} />
        <label>Avg</label>
      </span>
      <span>
        <input type="radio" name="aggregate" value="max" onChange={NotifyChange} />
        <label>Máx</label>
      </span>
      <span>
        <input type="radio" name="aggregate" value="min" onChange={NotifyChange} />
        <label>Mín</label>
      </span>
    </form>
  );
}
