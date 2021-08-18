import React, {useState, useEffect, useRef} from 'react';
import {Container, Button, Box, Typography} from '@material-ui/core'
import { AppBar, Toolbar, IconButton} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './App.css';
import { RepeatOneSharp } from '@material-ui/icons';

const useStyles = makeStyles((theme) => ({
  button: {
    margin: '0 0 1em 0',
    width: '40%',
    height:'40px',
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const videoRef = useRef()
  const photoRef = useRef()
  const classes = useStyles();

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
  }

  async function detect() {
    if (photoRef.current) {
      const formData = new FormData();
      formData.append('image', photoRef.current);
      const response = await fetch('/detect', {
        method: "POST",
        body: formData,
      })

      if (response.status === 200) {
        const text = await response.text();
        alert("done");
      } else {
        alert("somtthing wrong");
      }
    }
  }

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            Med Erkennung
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
      <Box bgcolor="lightblue">
        <div className="Live-Section" >
          <video className="streaming" ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
          <Button className={classes.button} variant="contained" color="primary" onClick={takePhoto}>Take Picture</Button>
          <Button className={classes.button} variant="contained" color="primary" onClick={detect}>Detect</Button>
          <canvas className="streaming" ref={photoRef} />
        </div>
      </Box>
    </div>
  );
}

export default App;
