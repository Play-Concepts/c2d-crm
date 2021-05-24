import React, { ChangeEvent, useState } from 'react';
import Alert from '@material-ui/lab/Alert';
import {
  Box,
  Typography,
  Button,
  withStyles,
  LinearProgress,
  Popover,
  createStyles,
  makeStyles,
  Theme,
} from '@material-ui/core';

import { uploadCsvFile } from '../services/c2dcrm';
import { useAuth } from '../hooks/useAuth';

const BorderLinearProgress = withStyles((theme) => ({
  root: {
    height: 15,
    borderRadius: 5,
  },
  colorPrimary: {
    backgroundColor: '#EEEEEE',
  },
  bar: {
    borderRadius: 5,
    backgroundColor: '#1a90ff',
  },
}))(LinearProgress);

type FileUploadState = {
  uploadCompleted: boolean;
  selectedFiles: FileList | null;
  currentFile?: File;
  progress: number;
  message: string;
  isError: boolean;
  fileInfos: File[];
};

type UploadFileProps = {
  onFileUploadCompleted: () => void;
};

const useStylesContent = makeStyles((theme: Theme) =>
  createStyles({
    uploadFilePopoverContent: {
      padding: '20px',
      display: 'flex',
      flexDirection: 'column',
    },
    progressWrapper: {
      marginBottom: '16px',
    },
    btnChoose: {
      marginBottom: '16px',
    },
    alertBanner: {
      marginBottom: '16px',
    },
    typography: {
      padding: theme.spacing(2),
    },
  }),
);

const UploadFile: React.FC<UploadFileProps> = ({ onFileUploadCompleted }) => {
  const classes = useStylesContent();
  const { token } = useAuth();
  const [state, setState] = useState<FileUploadState>({
    uploadCompleted: false,
    selectedFiles: null,
    currentFile: undefined,
    progress: 0,
    message: '',
    isError: false,
    fileInfos: [],
  });

  const upload = async () => {
    if (!state.selectedFiles || state.selectedFiles?.length === 0) return;

    let currentFile = state.selectedFiles[0];

    setState({ ...state, progress: 0, currentFile: currentFile });

    try {
      const response = await uploadCsvFile(currentFile, token, (event) => {
        setState({
          ...state,
          progress: Math.round((100 * event.loaded) / event.total),
        });
      });

      if (response) {
        setState({
          ...state,
          message: response.data.message,
          isError: false,
        });

        onFileUploadCompleted();

        setState({
          ...state,
          uploadCompleted: true,
          selectedFiles: null,
        });
      }
    } catch (e) {
      setState({
        ...state,
        progress: 0,
        message: 'Could not upload the file!',
        currentFile: undefined,
        uploadCompleted: false,
        isError: true,
      });
    }
  };

  const selectFile = (event: ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, selectedFiles: event.target.files });
  };

  const { selectedFiles, currentFile, progress, message, isError, uploadCompleted } = state;

  return (
    <div className={classes.uploadFilePopoverContent}>
      {uploadCompleted && <Alert className={classes.alertBanner}>Upload Completed</Alert>}
      {currentFile && (
        <Box className="progressWrapper" display="flex" alignItems="center">
          <Box width="100%" mr={1}>
            <BorderLinearProgress variant="determinate" value={progress} />
          </Box>
          <Box minWidth={35}>
            <Typography variant="body2" color="textSecondary">{`${progress}%`}</Typography>
          </Box>
        </Box>
      )}

      <label htmlFor="btn-upload">
        <input id="btn-upload" name="btn-upload" style={{ display: 'none' }} type="file" onChange={selectFile} />
        <Button className={classes.btnChoose} variant="outlined" component="span">
          Choose .CSV File
        </Button>
      </label>
      <Button
        className="btn-upload"
        color="primary"
        variant="contained"
        component="span"
        disabled={!selectedFiles}
        onClick={upload}
      >
        Upload
      </Button>

      <Typography variant="subtitle2" className={`upload-message ${isError ? 'error' : ''}`}>
        {message}
      </Typography>
    </div>
  );
};

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    openButton: {
      marginBottom: theme.spacing(4),
    },
    typography: {
      padding: theme.spacing(2),
    },
  }),
);

const UploadFilePopover: React.FC<UploadFileProps> = ({ onFileUploadCompleted }) => {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  return (
    <div>
      <Button className={classes.openButton} variant="contained" color="primary" onClick={handleClick}>
        Upload Citizens File
      </Button>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
      >
        <UploadFile onFileUploadCompleted={onFileUploadCompleted} />
      </Popover>
    </div>
  );
};

export default UploadFilePopover;
