import React from 'react'
import { Snackbar, makeStyles } from '@material-ui/core'
import { Alert } from '@material-ui/lab'

export default function Notification (props) {
  const useStyles = makeStyles(theme => ({
    root: {
      top: theme.spacing(12),
      left: theme.spacing(42)
    }
  }))

  const { notify, setNotify } = props
  const classes = useStyles()

  const handleClose = (reason) => {
    if (reason === 'clickaway') {
      return
    }
    setNotify({
      ...notify,
      isOpen: false
    })
  }

  return (
        <Snackbar
            className={classes.root}
            open={notify.isOpen}
            autoHideDuration={3000}
            anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
            onClose={handleClose}>
            <Alert
                severity={notify.type}
                onClose={handleClose}>
                {notify.message}
            </Alert>
        </Snackbar>
  )
}
