import React from 'react';
import {useHistory} from "react-router-dom";
import Button from 'react-bootstrap/Button';

var BackButton = () => {
  const history = useHistory();

  return (
    <Button 
      variant="dark" 
      style={{marginLeft: '1rem', marginBottom: '2rem'}} 
      onClick={() => history.push('/')}
    >Back
    </Button>
  )
}

export default BackButton;