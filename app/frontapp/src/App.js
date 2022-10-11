import logo from './logo.svg';
import  { PageHeader } from 'antd';
import './App.css';
import InflationList from './components/InflationList';


function App() {
  return (
    <div className="App">
        <PageHeader
        ghost={false}
      onBack={() => null}
      title="Inflacja"
      subTitle="Inflacja w Polsce wegług GUS"
  />
      <InflationList/>
    </div>
  );
}

export default App;
