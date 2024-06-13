import './App.css';
import {useState} from 'react';
import AggregateInput from './components/aggregate_input';
import ConstructionTypeSelector from './components/construction_type_selector';
import ZipCodeInput from './components/zip_code';

export default function App() {
  const [zipCode, setZipCode] = useState('');
  const [aggregate, setAggregate] = useState('avg');
  const [constructionType, setConstructionType] = useState(1);
  const [result, setResult] = useState('');
  const [errors, setErrors] = useState('');

  function UpdateAggregate(aggregate) {
    setAggregate(aggregate);
    UpdateResult();
  }

  function UpdateZipCode(zipCode) {
    setZipCode(zipCode);
    UpdateResult();
  }

  function UpdateConstructionType(constructionType) {
    setConstructionType(constructionType);
    UpdateResult();
  }

  function UpdateResult() {
    (async function() {
      try{
        const resp = await fetch(`/price-m2/zip-codes/${zipCode}/aggregate/${aggregate}?construction_type=${constructionType}`);
        const data = await resp.json();
        if (resp.status == 200) {
          setResult(JSON.stringify(data.payload));
          setErrors('');
        } else {
          setResult('-');
          setErrors(JSON.stringify(data.errors));
        }
      } catch(_) {
        setResult('-');
        setErrors('');
      }
    })();
  }

  return (
    <div className="App">
      <div>
        <AggregateInput UpdateAggregate={UpdateAggregate}></AggregateInput>
      </div>
      <div>
        <ConstructionTypeSelector UpdateConstructionType={UpdateConstructionType}></ConstructionTypeSelector>
      </div>
      <div>
        <ZipCodeInput UpdateZipCode={UpdateZipCode}></ZipCodeInput>
      </div>
      <div>
        <table>
        <tbody>
          <tr>
            <td>f(</td>
            <td>{aggregate},</td>
            <td>{zipCode},</td>
            <td>{constructionType}</td>
            <td>)</td>
            <td>=</td>
            <td>{result}</td>
          </tr>
        </tbody>
        </table>
      </div>
      <div>
        {errors}
      </div>
    </div>
  );
}
