import React, {useState, useEffect, useRef, useDebugValue} from 'react';
import {Container, Button, Box, Typography} from '@material-ui/core'
// import { AppBar, Toolbar, IconButton, Grid, Paper, TextField} from '@material-ui/core';
// import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import './GroundTruth.css';
import styled from 'styled-components';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
//import Task from './task';
import {initialData, saved_data} from './initial-data';
import Column from './column';
//import { teal } from '@material-ui/core/colors';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
//import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import QRCode from "qrcode.react"
//import CommentIcon from '@material-ui/icons/Comment';


const useStyles = makeStyles((theme) => ({
  button: {
    margin: '1em 0 1em 0',
    width: '20%',
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
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
}));

const med_names = ["weichkapsel_transparent","weichkapsel_braun","kapsel_weiss_gelb_orange","kapsel_weiss_gelb","kapsel_weiss","dragee_blau","dragee_pink","tablette_beige_oval","tablette_weiss_oval","tablette_braun_rund","tablette_blau_rund","tablette_weiss_zink","tablette_weiss_10mm","tablette_weiss_8mm","tablette_weiss_7mm"]
const med_list = []
for (const [i, med_name] of med_names.entries()) {
  const med_o = {id: i.toString(), name: med_name}
  med_list.push(med_o)
}

const finalSpaceCharacters = [
  {
    id: 'gary',
    name: 'Gary Goodspeed'
  },
  {
    id: 'cato',
    name: 'Little Cato'
  }
]

function GroundTruth() {
  const videoRef = useRef();
  const photoRef = useRef();
  const classes = useStyles();
  const imageRef = useRef();
  const [result, setResult] = useState([]);
  const [qrCode, setqrCode] = useState('PatienID');
  const [savedData, setSavedData] = useState(saved_data);
  const [patient, setPatient] = useState(false)
  const [checked, setChecked] = useState([]);
  const [patientList, setPatientList] = useState([]);

  const [characters, updateCharacters] = useState(med_list);
  const [medBox, updateMedBox] = useState(finalSpaceCharacters);
  const [state, setState] = useState(initialData)
  const [qrValue, setQrValue] = useState("qrcode");

  useEffect(async function getPatientList() {
    // Update the document title using the browser API
    const response = await fetch('/getPatientID', {
      method: "GET"
    })
    console.log("initial load")
    if (response.status === 200) {
      const text = await response.json()
      console.log(text)
      setPatientList(text.list)
    }
  }, []);

  function handleOnDragEnd(result) {
    if (!result.destination) return;

    const items = Array.from(characters);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    updateCharacters(items);
  }

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

  // const takePhoto = () => {
  //   const context = photoRef.current.getContext('2d');
  //   const {videoWidth, videoHeight} = videoRef.current;

  //   photoRef.current.width = videoWidth;
  //   photoRef.current.height = videoHeight;

  //   context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);

  //   photoRef.current.toBlob((blob) => {
  //     imageRef.current = blob;
  //   })
  // }

  async function detect() {
    const context = photoRef.current.getContext('2d');
    const {videoWidth, videoHeight} = videoRef.current;

    photoRef.current.width = videoWidth;
    photoRef.current.height = videoHeight;

    context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);
    imageRef.current = await new Promise(resolve => photoRef.current.toBlob(resolve))

    console.log(imageRef.current)
    if (imageRef.current) {
      const formData = new FormData();
      formData.append('image', imageRef.current);
      const response = await fetch('/detect', {
        method: "POST",
        body: formData,
      })
      let outputData = []
      if (response.status === 200) {
        const text = await response.json()
        const qrCodeID = Object.keys(text)[0]
        setqrCode(qrCodeID)
        setSavedData(text[qrCodeID])
        const output = text[qrCodeID]
        console.log("output", output)
        let newColumns = state.columns

        for (const [key, value] of Object.entries(output)) {
          //console.log(key,value)
          //console.log("state is", state)
          //const firstColumn = state.columns[key]
          let newTaskIds = []
          for (const med of value["taskIds"]) {

            //state.columns[key]["taskIds"].push(med.med)
            newTaskIds.push(med.med)
            const dataBase = state.columns[key]["data"]
            state[dataBase][med.med].amount = med.amount
            //console.log("med hier", state[dataBase][med.med].amount)
            //state.columns[key]["data"][med.med].amount = med.amount
            //medList.push(med.med)
          }
          console.log("newColumns1", newColumns[key])
          newColumns[key]["taskIds"] = newTaskIds
        }
        console.log("newColumns", newColumns)
        const newState = {
          ...state,
          columns: newColumns,
        };
        setState(newState)
      } else {
        alert("somtething wrong");
      }
    }
  }

  console.log("what is", savedData)


  const Container = styled.div`
    margin: 8px;
    display: flex;

  `;

  const Box_Container = styled.div`
    margin: 8px;
    display: flex;
    flex-direction: column;
  `;

  const Title = styled.h3`
    padding: 8px;
  `;
  const TaskList = styled.div`
    border: 1px solid lightgrey;
    border-radius: 2px;
    padding: 8px;
    margin-bottom: 8px;
  `;

  function handleOnDragEnd(result) {
    if (!result.destination) return;

    const items = Array.from(characters);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    updateCharacters(items);
  }

  function onDragEnd(result){
    const { destination, source, draggableId } = result;
    const toSaved = savedData
    // for (const [key, value] of Object.entries(state['columns'])) {
    //   if (key !== 'column-1') {
    //     const item = {}
    //     item.id = value.id
    //     item.taskIds = []
    //     saved_data1[key] = item
    //   }
    // }
    // console.log(saved_data1)
    // console.log(savedData)
    if (source.droppableId === "column-1" && !destination) {
      return;
    } else if (source.droppableId !== "column-1" && !destination) {
      const firstStart = state.columns[source.droppableId]
      //console.log("destination hier: ", destination)
      //return;
      const firtfinish = state.columns[source.droppableId];
      const newIds = Array.from(firstStart.taskIds);
      //const startTaskIds = Array.from(start.taskIds);
      const taskID1 = newIds[source.index];
      const tempState = state
      if (tempState[firtfinish['data']][taskID1]['amount'] > 1) {
        tempState[firtfinish['data']][taskID1]['amount'] = tempState[firtfinish['data']][taskID1]['amount'] - 1;
        setState(tempState);
        return;
      } else {
        newIds.splice(source.index, 1)
        const newColumn = {
          ...firstStart,
          taskIds: newIds,
        };

        const newState = {
          ...state,
          columns: {
            ...state.columns,
            [newColumn.id]: newColumn,
          },
        };
        setState(newState);
        return;
      }
      // tempState[finish['data']][taskID1]['amount'] = tempState[finish['data']][taskID1]['amount'] + 1
      // setState(tempState);
      // console.log("testing hier", tempState[finish['data']][taskID1]['amount'])
      // return


    } else if (source.droppableId !== "column-1" && destination) {
      return;
    }

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const start = state.columns[source.droppableId];
    //console.log("start", start)
    const finish = state.columns[destination.droppableId];

    //console.log("finish", finish)
    if (start === finish) {
      const newTaskIds = Array.from(start.taskIds);
      // console.log("newTaskIds", newTaskIds)
      // console.log("source.index", source.index)
      // console.log("destination.index", destination.index)
      const taskID = newTaskIds.splice(source.index, 1)
      newTaskIds.splice(destination.index, 0, taskID[0]);

      const newColumn = {
        ...start,
        taskIds: newTaskIds,
      };

      const newState = {
        ...state,
        columns: {
          ...state.columns,
          [newColumn.id]: newColumn,
        },
      };
      // console.log("newColumn", newColumn)
      // console.log("newState", newState)

      setState(newState);
      return;
    }

    // Moving from one list to another
    if (destination.droppableId === "column-1") {
      return;
    }
    const startTaskIds = Array.from(start.taskIds);
    const taskID1 = startTaskIds[source.index];
    //startTaskIds.splice(source.index, 1);
    // const newStart = {
    //   ...start,
    //   taskIds: startTaskIds,
    // };

    const ID_list = finish.taskIds
    console.log("checking", ID_list)
    //console.log(saved_data[finish.id].taskIds)
    //console.log("testing hier", state[finish['data']][taskID1])
    const tempState = state
    if (ID_list.includes(taskID1)) {
      tempState[finish['data']][taskID1]['amount'] = tempState[finish['data']][taskID1]['amount'] + 1
      setState(tempState);
      let i = 0
      for (const med of savedData[finish.id].taskIds) {
        if (med.med === taskID1) {
          savedData[finish.id].taskIds[i].amount = savedData[finish.id].taskIds[i].amount + 1
        }
        i = i + 1
      }
      //console.log("testing hier", tempState[finish['data']][taskID1]['amount'])
      //console.log("saved_data", savedData)
      //let outPut = JSON.stringify(savedData)
      //console.log("jsonString", outPut)
      return
    }

    const finishTaskIds = Array.from(finish.taskIds);
    finishTaskIds.splice(destination.index, 0, taskID1);
    //finishTaskIds.splice(destination.index, 0, draggableId);
    const newTaskIds = []
    for (const taskID of finishTaskIds) {
      console.log("finishtaskIDs", finishTaskIds)
      const medItem = {}
      medItem.med = taskID
      medItem.amount = tempState[finish['data']][taskID]["amount"]
      //saveDatas[finish.id].taskIds.push(medItem)
      newTaskIds.push(medItem)
    }
    const newSavedData = {
      ...savedData,
      [finish.id]: {
        ...savedData[finish.id],
        taskIds: newTaskIds
      }
    }
    //console.log("newSavedData", newSavedData)
    setSavedData(newSavedData)
    //console.log("saved_data", savedData)
    //console.log("toSaved", toSaved)
    const newFinish = {
      ...finish,
      taskIds: finishTaskIds,
    };
    //console.log("newFinish", newFinish)
    const newState = {
      ...state,
      columns: {
        ...state.columns,
        // [newStart.id]: newStart,
        [newFinish.id]: newFinish,
      },
    };
    setState(newState);
    // TODO: reorder our column
  };

  async function saveData() {

    //console.log("hier is", JSON.stringify(savedData))
    console.log(qrCode)
    const toSave = {}
    toSave[qrCode] = savedData
    const response = await fetch('/saveData', {
      method: "POST",
      header: {'Content-Type': 'application/json'},
      body: JSON.stringify(toSave)
    })

    if (response.status === 200) {
      const text = await response.json()
      console.log(text)
      setPatientList(text.list)
    }
  }

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };

  const loadData = async () => {
    if (checked.length > 1) {
      alert("Please select only one file to load")
      return
    }
    //console.log(checked.length)
    const data = {}
    data.fileName = checked[0]
    console.log("data", data)
    const response = await fetch('/loadPatientFile', {
      method: "POST",
      body: JSON.stringify(data)
    })

    if (response.status === 200) {
      const text = await response.json()
      const qrCodeID = Object.keys(text)[0]
      setqrCode(qrCodeID)
      setSavedData(text[qrCodeID])
      const output = text[qrCodeID]
      console.log("text", text)
      console.log("qrCodeID", qrCodeID)
      console.log("output", output)
      let newColumns = state.columns

      for (const [key, value] of Object.entries(output)) {
        //console.log(key,value)
        //console.log("state is", state)
        //const firstColumn = state.columns[key]
        let newTaskIds = []
        for (const med of value["taskIds"]) {

          //state.columns[key]["taskIds"].push(med.med)
          newTaskIds.push(med.med)
          const dataBase = state.columns[key]["data"]
          state[dataBase][med.med].amount = med.amount
          //console.log("med hier", state[dataBase][med.med].amount)
          //state.columns[key]["data"][med.med].amount = med.amount
          //medList.push(med.med)
        }
        console.log("newColumns1", newColumns[key])
        newColumns[key]["taskIds"] = newTaskIds
      }
      console.log("newColumns", newColumns)
      const newState = {
        ...state,
        columns: newColumns,
      };
      setState(newState)
    } else {
      alert("somtething wrong");
    }
  }

  const deleteData = async function() {
    console.log(checked)
    const data = {}
    data.fileName = checked
    const response = await fetch('/deletePatientFile', {
      method: "POST",
      body: JSON.stringify(data)
    })

    if (response.status === 200) {
      const text = await response.json()
      //console.log(text)
      setPatientList(text.list)
    }
    setChecked([])
    //setState(initialData)

  }

  const handleOnChange = event => {
    const { value } = event.target;
    setQrValue(value);
  };
  const downloadQRCode = () => {
    // Generate download with use canvas and stream
    const canvas = document.getElementById("qr-gen");
    const pngUrl = canvas
      .toDataURL("image/png")
      .replace("image/png", "image/octet-stream");
    let downloadLink = document.createElement("a");
    downloadLink.href = pngUrl;
    downloadLink.download = `${qrValue}.png`;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  };

  return (
    <div className="App">
      <Box bgcolor="lightblue" display="flex" flexDirection="row">
        <div className="Live-Section" >
          <video className="streaming" ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
          <Button className={classes.button} variant="contained" color="primary" onClick={detect}>Scan</Button>
          <canvas className="streaming" ref={photoRef} />
        </div>
        <div className="MedBox" >
          <div className="MedList">
            <Typography variant="h6" className={classes.title}>
              {qrCode}
            </Typography>
            <DragDropContext onDragEnd={onDragEnd}>
              <Container>
                {state.columnMed.map(columnId => {
                  const column = state.columns[columnId];
                  const tasks = column.taskIds.map(
                    taskId => state.medList[taskId],
                  );

                  return <Column key={column.id} column={column} tasks={tasks} />;
                })}
              </Container>
              <Box_Container>
                {state.columnOrder.map(columnId => {
                  const column = state.columns[columnId];
                  const tasks = column.taskIds.map(
                    taskId => state[column.data][taskId],
                  );

                  return <Column key={column.id} column={column} tasks={tasks} />;
                })}
              </Box_Container>
            </DragDropContext>
          </div>
        </div>
        <div className="lastColumn">
          <Button className={classes.button} variant="contained" color="primary" onClick={saveData}>Save File</Button>
          <div className="SavedData" >
            <List className={classes.root}>
              {patientList.map((value) => {
                const labelId = `checkbox-list-label-${value}`;

                return (
                  <ListItem key={value} role={undefined} dense button onClick={handleToggle(value)}>
                    <ListItemIcon>
                      <Checkbox
                        edge="start"
                        checked={checked.indexOf(value) !== -1}
                        tabIndex={-1}
                        disableRipple
                        inputProps={{ 'aria-labelledby': labelId }}
                      />
                    </ListItemIcon>
                    <ListItemText id={labelId} primary={value} />
                  </ListItem>
                );
              })}
            </List>
          </div>
          <Button className={classes.button} variant="contained" color="primary" onClick={loadData}>Load File</Button>
          <Button className={classes.button} variant="contained" color="primary" onClick={deleteData}>Delete File</Button>
          <div className="QRCode">
            <Typography variant="h6" color="primary" className={classes.title}>
              QR Code Generator
            </Typography>
            <input onChange={handleOnChange} placeholder="PatientID" />
            <br />
            <QRCode
              id="qr-gen"
              value={qrValue}
              size={290}
              level={"H"}
              includeMargin={true}
            />
            <p>
              <button type="button" onClick={downloadQRCode}>
                Download QR Code
              </button>
            </p>
          </div>
        </div>
      </Box>
    </div>
  );
}

export default GroundTruth;
