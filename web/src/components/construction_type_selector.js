import {useEffect, useState} from "react";

export default function ConstructionTypeSelector({ UpdateConstructionType }) {
  const [ctypes, setCTypes] = useState([]);

  useEffect(function() {
    (async function() {
      const resp = await fetch("/price-m2/completion/uso_construccion/");
      const data = await resp.json();
      setCTypes(data);
    })();
  }, []);

  function NotifyChange(evt) {
    UpdateConstructionType(evt.target.value);
  }

  return (
    <select onChange={NotifyChange}>
      {ctypes.map(opt =>
        <option key={opt.id} value={opt.id}>{opt.name}</option>
      )}
    </select>
  );
}
