import React from 'react';
import Container from 'react-bootstrap/esm/Container';

const PageTitle = (props) => {
    const {title, subtitle} = props
  
    return (
      <>
        <Container>
          <h1>{title}</h1>
          <h3>{subtitle}</h3>
        </Container>
      </>
    )
  }
  
  export default PageTitle;