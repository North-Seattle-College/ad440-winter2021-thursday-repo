import React, { useEffect, useState } from 'react';
import Toast from 'react-bootstrap/Toast';

export function ToastMessage(props) {

  const [message, setMessage] = useState(props.message);

  useEffect(() => {
    setMessage(props.message);
  }, [props.message]);

  return (
    <>
      <Toast
        style={{
          position: 'fixed',
          top: 20,
          right: 20,
        }}
        show={message}
        onClose={props.closeToast}
        delay={3000}
        autohide>
        <Toast.Header>
          <strong className="mr-auto">Deleted</strong>
        </Toast.Header>
        <Toast.Body>{message}</Toast.Body>
      </Toast>
    </>
  );
}
