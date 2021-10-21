import React, {useState, useEffect, useRef} from 'react';
import {Container, Button, Box, Typography} from '@material-ui/core'
import { AppBar, Toolbar, IconButton, Grid, Paper} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './Home.css';

const med_list_name = [
  "weichkapsel_transparent",
  "weichkapsel_braun",
  "kapsel_weiss_gelb_orange",
  "kapsel_weiss_gelb",
  "kapsel_weiss",
  "dragee_blau",
  "dragee_pink",
  "tablette_beige_oval",
  "tablette_weiss_oval",
  "tablette_braun_rund",
  "tablette_blau_rund",
  "tablette_weiss_zink",
  "tablette_weiss_10mm",
  "tablette_weiss_8mm",
  "tablette_weiss_7mm"
]

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
  paper: (props) => ({
    height: 140,
    width: '80%',
    border: `5px solid ${props.color}`,
    marginBottom: 10
  }),
  gPaper: {
    height: 140,
    width: '80%',
    border: '5px solid green',
    marginBottom: 10
  },
  title: {
    flexGrow: 1,
  },
}));

function Home() {
  const videoRef = useRef();
  const photoRef = useRef();
  const imageRef = useRef();
  const [gTruth, setGTruth] = useState([]);
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

  async function detectMed() {
    // if (imageRef.current) {
    //   const formData = new FormData();
    //   formData.append('image', imageRef.current);
    //   const response = await fetch('/detectMed', {
    //     method: "POST",
    //     body: formData,
    //   })
      
    //   if (response.status === 200) {
    //     const text = await response.json()
    //     // const qrCodeID = Object.keys(text)[0]
    //     // setqrCode(qrCodeID)
    //     // setResult(text[qrCodeID])
    //     console.log(text)
    //   } else {
    //     alert("somtething wrong");
    //   }

    //   //console.log(result)
    // }

    const response = await fetch('/detectMed', {
      method: "GET"
      //body: formData,
    })

    if (response.status === 200) {
      setGTruth([])
      setResult([])
      const text = await response.json()
      // const qrCodeID = Object.keys(text)[0]
      // setqrCode(qrCodeID)
      setGTruth(text.groundtruth)
      setResult(text.prediction)
      console.log(text.prediction)
      console.log(text.result)
    } else {
      alert("somtething wrong");
    }
  }
  
  console.log("result is", result)
  const props = {
    color: 'red'
  }
  const classes = useStyles(props);

  return (
    <div className="App">
      <Box bgcolor="lightblue" display="flex" flexDirection="row">
        <div className="Live-Section" >
          <video className="streaming" ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
          <Button className={classes.button} variant="contained" color="primary" onClick={takePhoto}>Take Picture</Button>
          <Button className={classes.button} variant="contained" color="primary" onClick={detectMed}>Detect</Button>
          <canvas className="streaming" ref={photoRef} />
        </div>
        <div className="Result" >
          <div className="GroundTruth">
            <Typography variant="h6" className={classes.title}>
              {qrCode}
            </Typography>
            <Grid container direction="column" >
              {gTruth.map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.gPaper} >
                    <ul>
                      {value.map(name => <li key={name.id}> {med_list_name[name.id]} </li>)}
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
                  <Paper className={classes.paper} style={ value.result ? { border: '5px solid green' } : { border: '5px solid red' }}>
                    <ul>
                      {value.detectedMed.map(name => <li key={name.id}> {med_list_name[name.id]} </li>)}
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