import React from 'react';
import SingleLayout from "../layout/single";
import { Button, Form, Segment, Label, List } from "semantic-ui-react";
import { sign_in} from "../services/hatters";
import {CALLBACK_URL} from "../services/constants";

const StartPage = () => {
    const [application_id, set_application_id] = React.useState('');

    const handleChange = (e, { value}) => {
        set_application_id(value);
    }

    const handleClick = () => {
        sign_in(application_id, CALLBACK_URL);
    }

    return (
        <SingleLayout>
            <Form size='large'>
                <Segment stacked>
                    <Segment>
                        <Label color='blue' ribbon>
                            Instructions
                        </Label>
                        <p />
                        <List ordered>
                            <List.Item>
                                If you haven't, create your own application at the <a href={"https://developers.dataswift.io"}>Dataswift Developers Dashboard</a>.
                            </List.Item>
                            <List.Item>
                                Make sure you have <strong>Web</strong> selected under <strong>Platforms</strong>, and you have an entry <Label color={'green'} basic>https://data.hackfromhome.com/auth/callback</Label> in the <strong>OAuth Redirect URI(s)</strong>
                            </List.Item>
                            <List.Item>
                                Take note of your <Label color={'green'} basic>namespace</Label> and <Label color={'green'} basic>application id</Label>.
                            </List.Item>
                            <List.Item>
                                Enter your <Label color={'green'} basic>Application Id</Label> below and click on the <strong>Start</strong> button.
                            </List.Item>
                            <List.Item>
                                Sign in with the email address of your Test PDA.
                            </List.Item>
                        </List>
                    </Segment>
                    <Form.Input
                        fluid
                        icon='lock'
                        iconPosition='left'
                        label='Application Id'
                        placeholder='Application Id'
                        name={'application_id'}
                        onChange={handleChange}
                    />

                    <Button primary fluid size='large' onClick={handleClick}>
                       Start
                    </Button>
                </Segment>
            </Form>
        </SingleLayout>
    )
}

export default StartPage;
