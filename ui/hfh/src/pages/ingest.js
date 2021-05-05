import React, {Fragment} from 'react';
import {useLocation} from "react-router-dom";
import SingleLayout from "../layout/single";
import {Segment, Label, Table, Input, Button} from "semantic-ui-react";
import { upload } from "../services/c2dcrm";
import { MessageDialog} from "../components/message-dialog";

const IngestPage = props => {
    const [data_file, set_data_file] = React.useState(null);
    const [namespace, set_namespace] = React.useState('');
    const [data_endpoint, set_data_endpoint] = React.useState('');

    // Dialog States
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [dialogTitle, setDialogTitle] = React.useState('');
    const [dialogMessage, setDialogMessage] = React.useState('');
    const [dialogDescription, setDialogDescription] = React.useState('');
    const [isError, setIsError] = React.useState(false);

    const search = useLocation().search;
    const applicationToken = new URLSearchParams(search).get('token');
    const applicationId = localStorage.getItem('application_id');

    const onFileChange = event => set_data_file(event.target.files);
    const onNamespaceChange =  (e, { value})  => set_namespace(value);
    const onDataEndpointChange =  (e, { value})  => set_data_endpoint(value);

    const onMessageDialogOk =  e  => {
        setDialogOpen(false);
        props.history.push("/pages/start");
    }

    const writeData = () => {
        if (namespace.trim()==='') {
            alert('Please enter Namespace');
            return;
        }
        if (data_endpoint.trim()==='') {
            alert('Please enter Data Endpoint');
            return;
        }
        if (data_file===null) {
            alert('Please select a Data File');
            return;
        }
        upload(data_file, applicationToken, namespace, data_endpoint, onUploadSuccess, onUploadFailure);
    }

    const onUploadSuccess = response => {
        setDialogTitle('Success');
        setDialogMessage('Data Ingestion Completed');
        setDialogDescription('Please check your PDA.');
        setIsError(false);
        setDialogOpen(true);
    }
    const onUploadFailure = response => {
        setDialogTitle('Unsuccessful');
        setDialogMessage('Data Ingestion Failed.');
        setDialogDescription('Please try again.');
        setIsError(true);
        setDialogOpen(true);
    }

    return (
        <SingleLayout>
            <Fragment>
                <MessageDialog open={dialogOpen}
                               title={dialogTitle}
                               message={dialogMessage}
                               description={dialogDescription}
                               isError={isError}
                               onOkClick={onMessageDialogOk}/>
                <Segment padded>
                    <Label color={'blue'} ribbon>Ingestion</Label>
                    <Table definition>
                        <Table.Body>
                            <Table.Row>
                                <Table.Cell width={'four'}>Application Id</Table.Cell>
                                <Table.Cell>{ applicationId }</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell>Namespace</Table.Cell>
                                <Table.Cell>
                                    <Input
                                        fluid
                                        placeholder={'Namespace to write the data into'}
                                        name={'namespace'}
                                        onChange={onNamespaceChange}
                                    />
                                </Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell>Data Endpoint</Table.Cell>
                                <Table.Cell>
                                    <Input
                                        fluid
                                        placeholder={'Data Endpoint to write the data into'}
                                        name={'data_endpoint'}
                                        onChange={onDataEndpointChange}
                                    />
                                </Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell>Data File</Table.Cell>
                                <Table.Cell>
                                    <Input
                                        fluid
                                        placeholder={'Data File in CSV format'}
                                        name={'data_file'}
                                        type={'file'}
                                        accept={'.csv'}
                                        onChange={onFileChange}
                                    />
                                </Table.Cell>
                            </Table.Row>
                        </Table.Body>
                    </Table>
                    <Button color={'red'} onClick={writeData}>Write Data into PDA</Button>
                </Segment>
            </Fragment>

        </SingleLayout>
    )
}

export default IngestPage;
