import React, {useState, useEffect, useRef} from 'react';
import {Container, Button, Box, Typography} from '@material-ui/core'
import { AppBar, Toolbar, IconButton, Grid, Paper} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './App.css';

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

function Home() {
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
      <Box bgcolor="lightblue" display="flex" flexDirection="row">
        <div className="Live-Section" >
          <video className="streaming" ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
          <Button className={classes.button} variant="contained" color="primary" onClick={takePhoto}>Take Picture</Button>
          <Button className={classes.button} variant="contained" color="primary" onClick={detect}>Detect</Button>
          <canvas className="streaming" ref={photoRef} />
        </div>
        <div className="Result" >
          <div className="GroundTruth">
            <Typography variant="h6" className={classes.title}>
              {qrCode}
            </Typography>
            <Grid container direction="column" >
              {result.map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.paper}>
                    <ul>
                      {value.map(name => <li key={name}> {name} </li>)}
                    </ul>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </div>
          <div className="Prediction">
            <Typography variant="h6" className={classes.title}>
              Prediction
            </Typography>
            <Grid container direction="column" >
              {result.map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.paper}>
                    <ul>
                      <li> prediction </li>
                    </ul>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </div>
        </div>
      </Box>
    </div>
  );
}

export default Home;