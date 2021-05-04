import React, {createRef} from "react";
import { Header } from "../components/header";
import {Container, Grid, Sticky} from "semantic-ui-react";

const SingleLayout = props => {
    const contextRef = createRef();
    return (
        <div ref={contextRef}>
            <Sticky context={contextRef}>
                <Header />
            </Sticky>
            <Container style={{minHeight: '75vh', width: '85vw', paddingBlockStart: 15, paddingLeft: 15, paddingRight: 15, paddingBlockEnd: 20}}>
                <Grid textAlign='left' verticalAlign='top'>
                    <Grid.Column>
                        { props.children}
                    </Grid.Column>
                </Grid>
            </Container>
        </div>
    );
}
export default SingleLayout;