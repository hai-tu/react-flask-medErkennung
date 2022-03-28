import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { lighten, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import DeleteIcon from '@material-ui/icons/Delete';
import AddBox from '@material-ui/icons/AddBox'
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';
import SaveIcon from '@material-ui/icons/Save';
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

function createData(name, dose, time, correct) {
  return {name, dose, time, correct};
}

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

const headCells = [
  { id: 'name', numeric: false, disablePadding: true, label: 'Medicine Name' },
  { id: 'dose', numeric: true, disablePadding: false, label: 'Dosierung (mg)' },
  { id: 'time', numeric: true, disablePadding: false, label: 'Geplante Einnahme' },
];

function EnhancedTableHead(props) {
  const { classes, onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort } = props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{ 'aria-label': 'select all desserts' }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? 'right' : 'left'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <span className={classes.visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </span>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  classes: PropTypes.object.isRequired,
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(['asc', 'desc']).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
};

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    minWidth: 275,
  },
  table_section: {
    width: '100%',
    height: '100%',
    marginBottom: theme.spacing(2),
  },
  table: {
    minWidth: 750,
  },
  visuallyHidden: {
    border: 0,
    clip: 'rect(0 0 0 0)',
    height: 1,
    margin: -1,
    overflow: 'hidden',
    padding: 0,
    position: 'absolute',
    top: 20,
    width: 1,
  },
  info_section: {
    width: '70%',
    height: '100%',
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    display: 'flex',
    flexDirection: 'row',
    textAlign: 'left',
  },

  add_section: {
    width: '80%',
    height: '100%',
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    display: 'flex',
    flexDirection: 'row',
    // textAlign: 'left',
  },

  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
  toolbar_root: {
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(1),
  },
  toolbar_highlight:
    theme.palette.type === 'light'
      ? {
          color: theme.palette.secondary.main,
          backgroundColor: lighten(theme.palette.secondary.light, 0.85),
        }
      : {
          color: theme.palette.text.primary,
          backgroundColor: theme.palette.secondary.dark,
        },
  toolbar_title: {
    flex: '1 1 100%',
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));

export default function EnhancedTable(props) {
  const classes = useStyles();
  const [order, setOrder] = React.useState('asc');
  const [orderBy, setOrderBy] = React.useState('calories');
  const [selected, setSelected] = React.useState([]);
  const [page, setPage] = React.useState(0);
  const [dense, setDense] = React.useState(false);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const [rowElem, setRowElem] = React.useState([]);
  const [med, setMed] = React.useState('');
  const [dose, setDose] = React.useState('');
  const [time, setTime] = React.useState('');
  const [infor, setInfor] = React.useState({})
  const [notify, setNotify] = React.useState({ isOpen: false, message: '', type: '' })

  
  // console.log(props.info)
  React.useEffect(() => {
    const rows = [];
    for (const element of props.planung) {
      rows.push(createData(element[0], element[1], element[2], element[3]))
    }
    setRowElem(rows)
    setInfor(props.info)
  }, [props]);
  // console.log(rowElem)
  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };
  // console.log("infor hier", infor)
  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelecteds = rowElem.map((n) => n.name);
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, name, time) => {
    const main_key = name + ';' +  time
    const selectedIndex = selected.indexOf(main_key);
    // console.log("selectedIndex", selectedIndex)
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, main_key);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1),
      );
    }
    // console.log(newSelected)
    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChangeDense = (event) => {
    setDense(event.target.checked);
  };

  const isSelected = (name) => selected.indexOf(name) !== -1;

  const handleDelete = () => {

    const newPlanung = []
    for (var i = 0; i < rowElem.length; i++) {
      const keyWord = rowElem[i].name + ';' + rowElem[i].time

      if (!selected.includes(keyWord)) {
        newPlanung.push(rowElem[i])
      }
    }
    // console.log(newPlanung)
    setRowElem(newPlanung)
    setSelected([])
  }
  
  const handleMedChange = (event) => {
    setMed(event.target.value);
  };

  const handleDoseChange = (event) => {
    setDose(event.target.value);
  };

  const handleTimeChange = (event) => {
    setTime(event.target.value);
  };

  const handleAdd = () => {
    if (med === '' || dose === '' || time === '') {
      alert("Please input all required information")
      return
    }
    const newPlanung = rowElem
    const addElem = createData(med, dose, time, true)
    newPlanung.push(addElem)
    setSelected([])
    setRowElem(newPlanung)
  }

  async function handleSaveData() {
    // const formData = new FormData();
    // const med_table = rowElem
    const med_data = {}
    med_data['meds'] = rowElem
    // formData.append('data', med_table);
    const response = await fetch('/saveData', {
      method: "POST",
      header: {'Content-Type': 'application/json'},
      body: JSON.stringify(med_data)
    })

    if (response.status === 200) {
      // setGTruth([])
      // setResult([])
      const text = await response.json()
      // console.log(text)
      if (text.error) {
        setNotify({
          isOpen: true,
          message: text.error,
          type: 'error'
        })
      } else {
        // console.log("get hier")
        setNotify({
          isOpen: true,
          message: text.success,
          type: 'success'
        })
      }
      //   setGTruth(text.prediction)
        
      // }
    } else {
      alert("somtething wrong");
    }
  }

  const emptyRows = rowsPerPage - Math.min(rowsPerPage, rowElem.length - page * rowsPerPage);

  return (
    <div className={classes.root}>
        <Paper className={classes.info_section}>
          <Card className={classes.root}>
            <CardContent>
              <Typography variant="h5" component="h2">
                {infor.name}
              </Typography>
              <br/>
              <Typography className={classes.pos} color="textSecondary">
                Stationäre Pflege Seit: {infor.admission_time}
              </Typography>
              <Typography variant="body2" component="p">
                Wohnbereich: {infor.room}
              </Typography>
              <Typography variant="body2" component="p">
                Bemerkung: {infor.remark}
              </Typography>
            </CardContent>
          </Card> 
        </Paper>
        <Notification notify={notify} setNotify={setNotify} />
        <Paper className={classes.add_section}>
          <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Medicine</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={med}
              onChange={handleMedChange}
            >
              {med_list_name.map((name) => (
                <MenuItem value={name}>{name}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField id="filled-basic" label="Dosierung (mg)" variant="filled" onChange={handleDoseChange} />
          <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Time</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={time}
              onChange={handleTimeChange}
            >
              <MenuItem value={'morgens'}>morgens</MenuItem>
              <MenuItem value={'mittags'}>mittags</MenuItem>
              <MenuItem value={'abends'}>abends</MenuItem>
              <MenuItem value={'nachts'}>nachts</MenuItem>
            </Select>
          </FormControl>
          <Tooltip title="Add New Medicine">
            <IconButton aria-label="Add New Medicine" onClick={handleAdd}>
              <AddBox/>
            </IconButton>
          </Tooltip>
        </Paper>

        <Paper className={classes.table_section}>
          <Toolbar
            className={clsx(classes.toolbar_root, {
              [classes.toolbar_highlight]: selected.length > 0,
            })}
          >
            {selected.length > 0 ? (
              <Typography className={classes.toolbar_title} color="inherit" variant="subtitle1" component="div">
                {selected.length} selected
              </Typography>
            ) : (
              <Typography className={classes.toolbar_title} variant="h6" id="tableTitle" component="div">
                Planung
              </Typography>
            )}

            {selected.length > 0 ? (
              <Tooltip title="Delete">
                <IconButton aria-label="delete" onClick={handleDelete}>
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            ) : (
              <Tooltip title="Add New Medicine">
                <IconButton aria-label="Add New Medicine" onClick={handleSaveData}>
                  <SaveIcon/>
                </IconButton>
              </Tooltip>
            )}
          </Toolbar>
          <TableContainer>
            <Table
              className={classes.table}
              aria-labelledby="tableTitle"
              size={dense ? 'small' : 'medium'}
              aria-label="enhanced table"
            >
              <EnhancedTableHead
                classes={classes}
                numSelected={selected.length}
                order={order}
                orderBy={orderBy}
                onSelectAllClick={handleSelectAllClick}
                onRequestSort={handleRequestSort}
                rowCount={rowElem.length}
              />
              <TableBody>
                {stableSort(rowElem, getComparator(order, orderBy))
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => {
                    const isItemSelected = isSelected(row.name + ';' +  row.time);
                    // const isItemSelected = isSelected(row.name);
                    const labelId = `enhanced-table-checkbox-${index}`;

                    return (
                      <TableRow
                        hover
                        onClick={(event) => handleClick(event, row.name, row.time)}
                        role="checkbox"
                        aria-checked={isItemSelected}
                        tabIndex={-1}
                        key={row.name+row.time}
                        selected={isItemSelected}
                        style={ row.correct ? { background: 'transparent' } : { background: 'orangered' }}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            checked={isItemSelected}
                            inputProps={{ 'aria-labelledby': labelId }}
                          />
                        </TableCell>
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {row.name}
                        </TableCell>
                        <TableCell align="right">{row.dose}</TableCell>
                        <TableCell align="right">{row.time}</TableCell>
                      </TableRow>
                    );
                  })}
                {emptyRows > 0 && (
                  <TableRow style={{ height: (dense ? 33 : 53) * emptyRows }}>
                    <TableCell colSpan={6} />
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={rowElem.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
        <FormControlLabel
          control={<Switch checked={dense} onChange={handleChangeDense} />}
          label="Dense padding"
        />
    </div>
  );
}