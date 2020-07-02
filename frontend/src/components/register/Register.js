import React, {Component} from 'react';
import {Form, Button} from "react-bootstrap"
import {Link} from "react-router-dom"
import axios from "axios"
import Cookies from "js-cookie"

import Login from "../login/Login"

class Register extends Component{
    constructor(props){
        super(props)

        this.state = {
            username: "",
            email: "",
            password:"",
            password2: "",
            errorCheck: "",
        }

        this.handleChange       = this.handleChange.bind(this)
        this.handleRegister     = this.handleRegister.bind(this)
    }

    handleChange = (e) =>{
        // Changes state with current information
        this.setState({
            [e.target.name]:e.target.value
        })
    }

    handleRegister = (e) => {
        e.preventDefault()
        if (this.state.password != this.state.password2){
            this.setState({
                errorCheck: "Password does not match"
            })
        } else {
            const registerUser = {
                username: this.state.username,
                email: this.state.email,
                password: this.state.password,
            }
            axios.post("api/auth/register", registerUser, {"Content-Type": "application/json"})
                .then(res => {
                    Cookies.set("token",res.data.token, {expires:7})
                    console.log("Registration Success")
                    this.props.setLogin(res)
                    this.props.history.push("/") 
                   
                })
                .catch(err => {
                    console.log("Registration Error " + err )
                    this.setState({
                        errorCheck: "Dupilcate Registration"
                    })
                })
        }
        

    }


    render(){
        return(
            <div>
                {console.log("Register Render")}
                <Form className =  "col-sm-8">
                    <Form.Group controlId="formBasicName">
                        <Form.Label>Username</Form.Label>
                        <Form.Control 
                            type="name" 
                            name = "username"
                            placeholder="username"
                            onChange = {(e) => this.handleChange(e)} />
                    </Form.Group>

                    <Form.Group controlId="formBasicEmail">
                        <Form.Label>Email</Form.Label>
                        <Form.Control 
                            type="email" 
                            name = "email"
                            placeholder="email"
                            onChange = {(e) => this.handleChange(e)} />
                    </Form.Group>
                
                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control 
                            type="password"
                            name = "password" 
                            placeholder="Password"
                            onChange = {(e) => this.handleChange(e)} />
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword2">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control 
                            type="password"
                            name = "password2" 
                            placeholder="Confirm Password"
                            onChange = {(e) => this.handleChange(e)} />
                    </Form.Group>

                    <Button 
                        variant="outline-secondary"
                        onClick = {(e) => this.handleRegister(e)}>
                        Register
                    </Button>
                    <p>
                        Login here <Link to = "/login">Login</Link>
                        <br/>
                        {this.state.errorCheck}
                        {console.log(this.state.errorCheck)}
                    </p>
                </Form>
            </div>
        )
    }
}

export default Register;