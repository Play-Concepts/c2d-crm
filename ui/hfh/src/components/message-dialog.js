import React from "react";
import {Modal, Header, Button, Icon} from "semantic-ui-react";
import PropTypes from "prop-types";

export const MessageDialog = ({open, title, message, description, okLabel, onOkClick, isError}) => {

    let iconStr = isError ? 'exclamation triangle' : 'comment outline';
    let headerColor = isError ? 'red' : 'green';
    let okButtonLabel = okLabel ? okLabel : 'OK';

    return (
        <Modal open={open}>
            <Header icon={iconStr} color={headerColor} content={title} />
            <Modal.Content>
                <p>
                    {message}
                </p>
                <p>
                    {description}
                </p>
            </Modal.Content>
            <Modal.Actions>
                <Button name={'okBtn'} color='green' inverted onClick={onOkClick}>
                    <Icon name='checkmark' /> {okButtonLabel}
                </Button>
            </Modal.Actions>
        </Modal>
    );
};

MessageDialog.propTypes = {
    open: PropTypes.bool,
    isError: PropTypes.bool,
    title: PropTypes.string,
    description: PropTypes.string,
    message: PropTypes.string,
    onOkClick: PropTypes.func
};