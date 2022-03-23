import React, {useState, useEffect, useRef} from 'react';
//import {Container, Button, Box, Typography} from '@material-ui/core'
//import { AppBar, Toolbar, IconButton, Grid, Paper} from '@material-ui/core';
//import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './App.css';
import SimpleTabs from './Tabs';
import Home from './views/Home/Home';
import GroundTruth from './views/GroundTruth/GroundTruth';
import NavBar from './components/NavBar/NavBar';
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Switch, Redirect } from 'react-router-dom';


const useStyles = makeStyles((theme) => ({
  button: {
    margin: '0 0 1em 0',
    width: '50%',
    height:'40px',
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  forGrid: {
    margin: '0.5em 0 0 0',
  },
  gridItem: {
    margin: '0.5em 0 0 0',
    width: '500px',
    height: 300,
  },
  paper: {
    height: 140,
    width: '80%',
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const videoRef = useRef();
  const photoRef = useRef();
  const classes = useStyles();
  const imageRef = useRef();
  const [result, setResult] = useState([]);
  const [qrCode, setqrCode] = useState('Ground Truth');

  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);

  useEffect(() => {
    async function getCameraStream() {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: true,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    };

    getCameraStream();
  }, []);

  const playCameraStream = () => {
    if (videoRef.current) {
      videoRef.current.play();
    }
  };

  const takePhoto = () => {
    const context = photoRef.current.getContext('2d');
    const {videoWidth, videoHeight} = videoRef.current;

    photoRef.current.width = videoWidth;
    photoRef.current.height = videoHeight;
    
    context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);
    
    photoRef.current.toBlob((blob) => {
      imageRef.current = blob;
    })
  }

  async function detect() {
    if (imageRef.current) {
      const formData = new FormData();
      formData.append('image', imageRef.current);
      const response = await fetch('/detect', {
        method: "POST",
        body: formData,
      })
      
      if (response.status === 200) {
        const text = await response.json()
        const qrCodeID = Object.keys(text)[0]
        setqrCode(qrCodeID)
        setResult(text[qrCodeID])
        //console.log(qrCodeID)
      } else {
        alert("somtething wrong");
      }

      //console.log(result)
    }
  }

  console.log(result)

  return (
    <div className="App">
      {/* <Router>
        <NavBar />
        <Switch>
          <Route exact path="/Home" component={Home} />
          <Route exact path="/">
            <Redirect to="/Home" />
          </Route>
          <Route exact path="/About" component={GroundTruth} />
        </Switch>
      </Router> */}
      <SimpleTabs/>
    </div>
  );
}

export default App;
