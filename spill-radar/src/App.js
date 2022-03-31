import logo from './logo.svg';
import map from './PersianGulfMap.png';
import './App.css';
import React from 'react';

class App extends React.Component{
  render(){
    //return (<h1>Hello world</h1>);

    return (
      <div className="App">
        <img className="App-map" src={map} alt="map of persian gulf" />
      </div>
    );
  }
}

export default App;
