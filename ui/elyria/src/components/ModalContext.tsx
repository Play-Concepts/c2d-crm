import React, { useCallback, useState, createContext, useContext } from 'react';
import Modal, { ModalProps } from '@material-ui/core/Modal';

export type ModalState = {
  open: boolean;
  component?: React.ComponentType<any>;
  componentProps?: any;
  modalProps?: Omit<ModalProps, 'open' | 'children'>;
};

const defaultState: ModalState = {
  open: false,
};

type ContextType = {
  openModal: (state: ModalState) => void;
  isOpen: boolean;
};

export const ModalContext = createContext<ContextType>({ openModal: () => {}, isOpen: false });

const ModalProvider: React.FC = ({ children }) => {
  const [modalState, setModalState] = useState(defaultState);

  const openModal = useCallback((state: ModalState) => setModalState(state), []);

  const closeModal = () => setModalState(defaultState);

  const { component: Component } = modalState;

  return (
    <ModalContext.Provider value={{ openModal, isOpen: modalState.open }}>
      {children}
      <Modal open={modalState.open} onClose={closeModal} className="ds-context-modal" {...modalState.modalProps}>
        <>{Component && <Component onClose={closeModal} {...modalState.componentProps} />}</>
      </Modal>
    </ModalContext.Provider>
  );
};

export const useModalContext = () => useContext(ModalContext);

export default ModalProvider;
