import React, { useState } from 'react';

import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'

import Button from 'react-bootstrap/Button';

class Modal2 extends React.Component {
  static Title = ({ children }) => <h2>{children}</h2>;
  static Body = ({ children }) => <section>{children}</section>;

  render() {
    return (
      <div>
        {this.props.children}
      </div>
    );
  };
};

const ExampleNavbar = ({children},props) => {

//        static Title = ({ children }) => <h2>{children}</h2>;
//        static Body = ({ children }) => <section>{children}</section>;

        return(
        <Navbar collapseOnSelect expand="lg" bg={props.bg} variant="dark" fixed="top">
          <Navbar.Brand href="#home">
                <children.title/>
          </Navbar.Brand>

          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#features">Features</Nav.Link>
              <Nav.Link href="#pricing">Pricing</Nav.Link>
              <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
              </NavDropdown>
            </Nav>
            <Nav>
              <Nav.Link href="#deets">More deets</Nav.Link>
              <Nav.Link eventKey={2} href="#memes">
                Dank memes
              </Nav.Link>
            </Nav>
        </Navbar.Collapse>
        </Navbar>

    );
};

const ExampleNavbar2 = ({ children }) => {
  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" sticky="top" fixed="top">
        <Navbar.Brand href="#home">Navbar</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#features">Features</Nav.Link>
          <Nav.Link href="#pricing">Pricing</Nav.Link>
        </Nav>
        <Form inline>
            <FormControl type="text" placeholder="Search" className="mr-sm-2" />
            <Button variant="outline-info">Search</Button>
        </Form>

        <div show = {false}>
            {children}
         </div>
      </Navbar>
    </>
  );
};


export default ExampleNavbar
