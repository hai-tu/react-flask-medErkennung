import React, {useState, useEffect, useRef} from 'react';
import { Button, Box, Typography, Grid, Paper} from '@material-ui/core'
// import { Container, AppBar, Toolbar, IconButton} from '@material-ui/core';
// import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './Home.css';
import EnhancedTable from './MedTable';
import Notification from './Notification';

const med_list_name = [
  "Dragee_blau",
  "Dragee_pink",
  "Kapsel_weiss",
  "kapsel_weiss_gelb",
  "Kapsel_weiss_gelb_orange",
  "Tablette_beige_oval",
  "Tablette_blau_rund",
  "Tablette_braun_rund",
  "Tablette_weiss_10mm",
  "Tablette_weiss_8mm",
  "Tablette_weiss_7mm",
  "Tablette_weiss_Zink",
  "Tablette_weiss_oval",
  "Weichkapsel_braun",
  "Weichkapsel_transparent"
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
    // background: 'lightgreen',
    // border: `5px solid ${props.color}`,
    marginBottom: 10
  }),
  gPaper: {
    height: 140,
    width: '80%',
    // border: '5px solid white',
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
  const [qrCode, setqrCode] = useState('Ground_Truth');
  const [isScanned, setIsScanned] = useState(false)
  const [notify, setNotify] = useState({ isOpen: false, message: '', type: '' })

  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);

  useEffect(() => {
    async function getCameraStream() {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        // video: true,
        video: {
          width: { ideal: 1920},
          height: {ideal: 1080}
        }
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

  async function getGroundTruth() {
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
    const context = photoRef.current.getContext('2d');
    const {videoWidth, videoHeight} = videoRef.current;

    photoRef.current.width = videoWidth;
    photoRef.current.height = videoHeight;

    context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);
    // //const formData = new FormData();
    //
    // photoRef.current.toBlob((blob) => {
    //   // formData.append('image', blob);
    //   imageRef.current = blob;
    // })
    imageRef.current = await new Promise(resolve => photoRef.current.toBlob(resolve))

    const formData = new FormData();
    formData.append('image', imageRef.current);
    console.log("hier")
    const response = await fetch('/getGroundTruth', {
      method: "POST",
      body: formData,
    })


    // const response = await fetch('/detectMed', {
    //   method: "GET"
    //   //body: formData,
    // })

    if (response.status === 200) {
      setGTruth([])
      setResult([])
      const text = await response.json()
      // const qrCodeID = Object.keys(text)[0]
      // setqrCode(qrCodeID)
      setGTruth(text.groundtruth)
      // setResult(text.prediction)
      setqrCode(text.patientID)
      setIsScanned(true)
      setNotify({
        isOpen: true,
        message: 'Patient Data Scanned Successfully',
        type: 'success'
      })

      // console.log(text.prediction)
      // console.log(text.result)
    } else {
      alert("somtething wrong");
    }
  }

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
    const context = photoRef.current.getContext('2d');
    const {videoWidth, videoHeight} = videoRef.current;

    photoRef.current.width = videoWidth;
    photoRef.current.height = videoHeight;

    context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);
    imageRef.current = await new Promise(resolve => photoRef.current.toBlob(resolve))
    const formData = new FormData();
    formData.append('image', imageRef.current);
    const response = await fetch('/detectMed', {
      method: "POST",
      body: formData,
    })

    if (response.status === 200) {
      // setGTruth([])
      setResult([])
      const text = await response.json()
      // const qrCodeID = Object.keys(text)[0]
      // setqrCode(qrCodeID)
      // setGTruth(text.groundtruth)
      if (text.error) {
        // alert(text.error)
        setNotify({
          isOpen: true,
          message: text.error,
          type: 'error'
        })
      } else {
        // setResult(text.prediction)
        // alert(text.message)
        if (text.correct) {
          setNotify({
            isOpen: true,
            message: text.message,
            type: 'success'
          })
        } else {
          setNotify({
            isOpen: true,
            message: text.message,
            type: 'error'
          })
        }
        setGTruth(text.prediction)
        
      }
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
          <Button className={classes.button} variant="contained" color="primary" onClick={getGroundTruth}>Patient Data</Button>
          {/*<Button className={classes.button} variant="contained" color="primary" onClick={takePhoto}>Take Picture</Button>*/}
          {isScanned ? <Button className={classes.button} variant="contained" color="primary" onClick={detectMed}>Detect</Button> : <Button className={classes.button} variant="contained" color="primary" onClick={detectMed} disabled='true'>Detect</Button>}
          {/* <Button className={classes.button} variant="contained" color="primary" onClick={detectMed} disabled='true'>Detect</Button> */}
          <canvas className="streaming" ref={photoRef} />
        </div>
        <div className="Result" >
          <Notification notify={notify} setNotify={setNotify} />
          {isScanned ? <EnhancedTable qrCode={qrCode} planung={gTruth}/> : <Typography variant="h6" className={classes.title}>
              Please Scan Patient ID
            </Typography>}
          {/* <EnhancedTable qrCode={qrCode}/> */}
          {/* <div className="GroundTruth">
            <Typography variant="h6" className={classes.title}>
              {qrCode}
            </Typography>
            <Grid container direction="column" >
              {gTruth.map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.gPaper} >
                    <ul>
                      {value.map(name => <li key={name.id}> {med_list_name[name.id] + ":" + name.amount} </li>)}
                    </ul>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </div>
          <div className="Prediction">
            <Typography variant="h6" className={classes.title}>
              Detection
            </Typography>
            <Grid container direction="column" >
              {result.map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.paper} style={ value.result ? { background: 'lightgreen' } : { background: 'orangered' }}>
                    <ul>
                      {value.detectedMed.map(name => <li key={name.id}> {med_list_name[name.id] + ":" + name.amount} </li>)}
                    </ul>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </div> */}
        </div>
      </Box>
    </div>
  );
}

export default Home;
