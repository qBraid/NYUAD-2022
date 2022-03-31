import logo from './logo.svg';
import map from './PersianGulfMap.png';
import './App.css';
import React from 'react';
import ReactDom from 'react-dom';
import { useState } from "react";
import styled from 'styled-components'


const useMousePosition = () => {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  React.useEffect(() => {
    const setFromEvent = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener("mousemove", setFromEvent);

    return () => {
      window.removeEventListener("mousemove", setFromEvent);
    };
  }, []);

  return position;
};

export const Ball = () =>
{
  let offsetX,offsetY
  const move=e=>
  {
    const el=e.target
    el.style.left = `${e.pageX-offsetX}px`
    el.style.top = `${e.pageY-offsetY}px`
  }
  const add=e=>
  {
    const el=e.target
    offsetX=e.clientX-el.getBoundingClientRect().left
    offsetY=e.clientY-el.getBoundingClientRect().top
    el.addEventListener('mousemove',move)
  }
  const remove=e=>{
    const el=e.target
    el.removeEventListener('mousemove',move)
  }
  const Wrapper=styled.div`
  width: 50px;
  height: 50px;
  border-radius: 29px;
  box-shadow: 0 0 6px;
  position: absolute;
  top: 40px;
  left: 227px;
  background-color: rgb(0,0,0,0.5);
  cursor:pointer;
  `
  return (
    <Wrapper onMouseDown={add} onMouseUp={remove}/>
  )
}

const App = () => {
  const[counter, setCounter] = React.useState(50); //counter
  const interval = React.useRef(null);
  //const [circles, setCircles] = useState([]);
  const position = useMousePosition();
  const [cursorX, setCursorX] = useState();
  const [cursorY, setCursorY] = useState();

  window.addEventListener('mousemove', (e) => {
    setCursorX(e.pageX);
    setCursorY(e.pageY);
  })

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
    boxShadow: '10px 5px 5px #BEBEBE',
    position: 'fixed',
    left: cursorX - 0.5*counter + 'px',
    top: cursorY - 0.5*counter + 'px'
  };

  // const getCoords = (event) => { //doesnt work yet
  //   var e = event.target;
  //   var dim = e.getBoundingClientRect();
  //   var x = event.clientX - dim.left;
  //   var y = event.clientY - dim.top;
  //   return [x, y];
  // };

  // const creatObj = (event) => { //doesnt work yet
  //   let [x, y] = getCoords(event);
  //   console.log(x);
  //   console.log(y);
  //   let newCircle = ( 
  //     <cicle 
  //       key={circles.length + 1} 
  //       cx={x} 
  //       cy={y}
  //       r="10"
  //       stroke="black"
  //       strokeWidth="1"
  //       fill="blue"
  //       />
  //     );
  //     let allCircles = [...circles, newCircle];
  //     setCircles(allCircles);
  // }

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

  const cursorStyle = {
    width: `${counter}px`,
    height: `${counter}px`,
    color: 'black',
    boxShadow: '10px' 
  };

  return (
    <div className="App">
      <div
        onMouseDown={startCounter}
        onMouseUp={stopCounter}
        onMouseLeave={stopCounter} 
        style = {elementStyle}
      >
      </div>

      {/*<div className="cursor"
        style = {{
          left: cursorX + 'px',
          top: cursorY + 'px'
        }}
        > 
      </div>*/
      }
      <div>
        <img className="App-map" src={map} alt="map of persian gulf" />
      </div>

      {/* <div 
          onMouseDown={startCounter}
          onMouseUp={stopCounter}
          onMouseLeave={stopCounter}
          onMouseMove={useMousePosition}
          // style={elementStyle}
          style={ elementStyle }
          // position={position}
      /> */}

      {/* <button onClick={sayHello}>Default</button>; */}
    </div>
  );
}

export default App;
