import logo from './logo.svg';
import map from './PersianGulfMap.png';
import './App.css';
import React from 'react';
import ReactDom from 'react-dom';
import { useState } from "react";

const App = () => {
  const[counter, setCounter] = React.useState(10); //counter
  const interval = React.useRef(null);
  const [circles, setCircles] = useState([]);

  React.useEffect(() => {
    return () => stopCounter();
  }, []);

  const containerStyle = {
    height: '100px', 
    width: '100px',
  };

  const elementStyle = {
    margin: '5px',
    height: `${counter}px`,
    width: `${counter}px`,
    background: 'radial-gradient(at 25% 25%, #2b86c5, #562b7c, #ff3cac)',
    borderRadius: '50%',
    boxShadow: '10px 5px 5px #BEBEBE'
  };

  const ClickableSVG = { //can ignore this
    width: '100px',
    hegith: '100px',
  };

  const getCoords = (event) => { //doesnt work yet
    var e = event.target;
    var dim = e.getBoundingClientRect();
    var x = event.clientX - dim.left;
    var y = event.clientY - dim.top;
    return [x, y];
  };

  const creatObj = (event) => { //doesnt work yet
    let [x, y] = getCoords(event);
    let newCircle = ( 
      <cicle 
        key={circles.length + 1} 
        cx={x} 
        cy={y}
        r="10"
        stroke="black"
        strokeWidth="1"
        fill="blue"
        />
      );
      let allCircles = [...circles, newCircle];
      setCircles(allCircles);
  }

  const startCounter = () => { //increment counter
    if(interval.current) return;
    interval.current = setInterval(() => {
      setCounter((prevCounter) => prevCounter + 1);
    }, 20);
  };

  const stopCounter= () => {
    if(interval.current) {
      clearInterval(interval.current);
      interval.current = null
    }
  };

  return (
    <div className="App">
      <div>
        <img className="App-map" src={map} alt="map of persian gulf" />
      </div>
      <div style={containerStyle}>
        <div 
          onMouseDown={startCounter}
          onMouseUp={stopCounter}
          onMouseLeave={stopCounter}
          style={elementStyle}
        />
      </div>
    </div>
  );
}


export default App;
