import React from 'react';
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';

var BootstrapTable = (props) => {
  var {heatherItems, rows} = props;

  return (
    <div className='table-container'>
      <div>
        <Table striped bordered hover>
          <thead>
            <tr>
              {heatherItems.map((item, index) => <th key={index}>{item}</th>)}
            </tr>
          </thead>
          {rows.map(row => (
            <tbody key={row[heatherItems[0]]}>
              <tr>{heatherItems.map(item => <td key={item}>{row[item]}</td>)}</tr>
            </tbody>
          ))}
        </Table>
      </div>
    </div>

  )
}

export default BootstrapTable;