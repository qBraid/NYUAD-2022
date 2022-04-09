import styled from 'styled-components';
import map from './PersianGulfMap.png';
import './App.css';
import React from 'react';
import ReactDom from 'react-dom';
import { useState } from "react";

const useMousePosition = () => { //get mouse position in coordinates
  const [position, setPosition] = useState({ x: 0, y: 0 });

  React.useEffect(() => {
    const setFromEvent = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener("mousedown", setFromEvent);

    return () => {
      window.removeEventListener("mousedown", setFromEvent);
    };
  }, []);
  //console.log(position);
  return position;
};


const App = () => {
  const[counter, setCounter] = React.useState(18); //counter
  const interval = React.useRef(null);
  const position = useMousePosition();
  const [cursorX, setCursorX] = useState();
  const [cursorY, setCursorY] = useState();

  const stopMovement = (e) => { //tracking mouse movement
    setCursorX(e.pageX);
    setCursorY(e.pageY);
  };

  window.addEventListener('mousemove', stopMovement, false);

  React.useEffect(() => { 
    return () => stopCounter();
  }, []);

  const startCounter = () => { //increment counter
    if(interval.current) return;
    interval.current = setInterval(() => {
      setCounter((prevCounter) => prevCounter + 1);
    }, 100);
  };

  const stopCounter= () => { //stop enlarging size
    if(interval.current) {
      clearInterval(interval.current);
      interval.current = null
    }
    window.removeEventListener('mousemove', stopMovement, false);
  };

  const circleStyle = {
    margin: '5px',
    height: `${counter}px`,
    width: `${counter}px`,
    background: 'black',
    borderRadius: '50%',
    boxShadow: '10px 5px 5px #BEBEBE',
    position: 'fixed',
    left: cursorX - 0.5*counter + 'px',
    top: cursorY - 0.5*counter + 'px'
  };

  return (
    <div className="App">
      <div className="circle"
        onMouseDown={startCounter}
        onMouseUp={stopCounter}
        onMouseLeave={stopCounter} 
        style = {circleStyle}
      >
      </div>

      <button onClick={ //fetching data from backend
        fetch('http://127.0.0.1:5000/qubo?size=20&x=0&y=5', 
        {mode: 'cors'})
        .then(response => response.json()) //use data to move the ships .then(data => console.log(data)
        }></button> 
        
      <div> 
        <img className="App-map" src={map} alt="map of persian gulf" />
      </div>
    </div>
  );
}

export default App;
