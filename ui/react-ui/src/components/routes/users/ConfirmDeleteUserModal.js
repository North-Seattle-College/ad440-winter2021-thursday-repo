import React, { useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

export function ConfirmDeleteUserModal(props) {

  const [user, setUser] = useState(props.user);
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (props.user)
    {
      setUser(props.user);
      setShow(true);
    }
  }, [props.user]);

  return (
    <>
      <Modal show={show} onHide={props.handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Delete User: </Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this user: {user.firstName + ' ' + user.lastName}?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={props.handleClose}>
            Cancel
            </Button>
          <Button variant="primary" onClick={() => props.handleDelete(user.userId)}>
            Confrim
            </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
