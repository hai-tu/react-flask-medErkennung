import React, {useState, useEffect, useRef} from 'react';
import {Button, Box, Typography} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles';
import './Home.css';
import EnhancedTable from './MedTable';
import Notification from './Notification';

const useStyles = makeStyles((theme) => ({
  button: {
    margin: '0 0 1em 0',
    width: '50%',
    height:'40px',
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
  const [infor, setInfor] = useState([]);
  // const [result, setResult] = useState([]);
  const [qrCode, setqrCode] = useState('Ground_Truth');
  const [isScanned, setIsScanned] = useState(false)
  const [notify, setNotify] = useState({ isOpen: false, message: '', type: '' })

  useEffect(() => {
    async function getCameraStream() {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        // video: true,
        video: {
          width: {ideal: 1920},
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

  /**
   * This is the function for "Patient Data" button, image is taken and
   * send to backend. Then the patient information and ground truth is
   * sent back to frontend, and store in gTruth and infor variable.
   */
  async function getGroundTruth() {
    const context = photoRef.current.getContext('2d');
    const {videoWidth, videoHeight} = videoRef.current;

    photoRef.current.width = videoWidth;
    photoRef.current.height = videoHeight;

    context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);

    imageRef.current = await new Promise(resolve => photoRef.current.toBlob(resolve))

    const formData = new FormData();
    formData.append('image', imageRef.current);
    // Image is send to backend hier.
    const response = await fetch('/getGroundTruth', {
      method: "POST",
      body: formData,
    })

    // Result sent back from backend is processed hier.
    if (response.status === 200) {
      setGTruth([])
      setInfor([])
      // setResult([])
      const text = await response.json()
      setGTruth(text.groundtruth)
      setInfor(text.patient_info)
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

  /**
   * This is the function for "Detect" button, the image on camera is
   * captured and sent to back end for processing. Then the compared
   * result is sent back to frontend and displayed in the "Planung" table.
   */
  async function detectMed() {
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
      // setResult([])
      const text = await response.json()
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

  const classes = useStyles();

  return (
    <div className="App">
      <Box bgcolor="lightblue" display="flex" flexDirection="row">
        <div className="Live-Section" >
          <video className="streaming" ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
          <Button className={classes.button} variant="contained" color="primary" onClick={getGroundTruth}>Patient Data</Button>
          {isScanned ? <Button className={classes.button} variant="contained" color="primary" onClick={detectMed}>Detect</Button> : <Button className={classes.button} variant="contained" color="primary" onClick={detectMed} disabled='true'>Detect</Button>}
          <canvas className="streaming" ref={photoRef} />
        </div>
        <div className="Result" >
          <Notification notify={notify} setNotify={setNotify} />
          {isScanned ? <EnhancedTable qrCode={qrCode} planung={gTruth} info={infor} /> : <Typography variant="h6" className={classes.title}>
              Please Scan Patient ID
            </Typography>}
        </div>
      </Box>
    </div>
  );
}

export default Home;
