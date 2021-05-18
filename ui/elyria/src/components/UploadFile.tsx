import React, { ChangeEvent, useState } from 'react';

import { Box, Typography, Button, ListItem, withStyles, LinearProgress } from '@material-ui/core';
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
  selectedFiles: FileList | null;
  currentFile?: File;
  progress: number;
  message: string;
  isError: boolean;
  fileInfos: File[];
};

const UploadFile: React.FC = () => {
  const { token } = useAuth();
  const [state, setState] = useState<FileUploadState>({
    selectedFiles: null,
    currentFile: undefined,
    progress: 0,
    message: '',
    isError: false,
    fileInfos: [],
  });

  const upload = () => {
    if (!state.selectedFiles || state.selectedFiles?.length === 0) return;

    let currentFile = state.selectedFiles[0];

    setState({ ...state, progress: 0, currentFile: currentFile });

    uploadCsvFile(currentFile, token, (event) => {
      setState({
        ...state,
        progress: Math.round((100 * event.loaded) / event.total),
      });
    })
      .then((response) => {
        setState({
          ...state,
          message: response.data.message,
          isError: false,
        });
        // return UploadService.getFiles();
      })
      .catch(() => {
        setState({
          ...state,
          progress: 0,
          message: 'Could not upload the file!',
          currentFile: undefined,
          isError: true,
        });
      });

    setState({
      ...state,
      selectedFiles: null,
    });
  };

  const selectFile = (event: ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, selectedFiles: event.target.files });
  };

  const { selectedFiles, currentFile, progress, message, fileInfos, isError } = state;

  return (
    <div className="mg20">
      {currentFile && (
        <Box className="mb25" display="flex" alignItems="center">
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
        <Button className="btn-choose" variant="outlined" component="span">
          Choose Files
        </Button>
      </label>
      <div className="file-name">{selectedFiles && selectedFiles.length > 0 ? selectedFiles[0].name : null}</div>
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

      <Typography variant="h6" className="list-header">
        List of Files
      </Typography>
      <ul className="list-group">
        {fileInfos &&
          fileInfos.map((file, index) => (
            <ListItem divider key={index}>
              {/*<a href={file.url}>{file.name}</a>*/}
            </ListItem>
          ))}
      </ul>
    </div>
  );
};

export default UploadFile;
