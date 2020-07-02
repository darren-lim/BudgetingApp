import React, {Component} from "react";
import {Form, Button} from "react-bootstrap"
import {Link} from "react-router-dom"
import Cookies from "js-cookie"
import axios from "axios";

import Register from "../register/Register"


class Login extends Component{
    constructor(props){
        super(props);
        this.state = {
            username: "",
            password: "",
            loginCheck: "",
        }
        
        this.handleLogin = this.handleLogin.bind(this)
        this.handleChange = this.handleChange.bind(this)
    }

    handleLogin = (e) => {
        e.preventDefault()
        const loginUser = {
            username: this.state.username,
            password: this.state.password,
        }

        axios.post("api/auth/login", loginUser,{"Content-Type": "application/json"})
            .then(res => {
                Cookies.set("token",res.data.token, {expires:7})
                console.log("Login Success")
                console.log(res)
                this.props.setLogin(res)
                this.props.history.push("/")
            })
            .catch(err => {
                console.log("Login Error" + err)
                this.setState({
                    loginCheck: "Invalid Username or Password",
                })
            } )

    }

    handleChange = (e) =>{
        // Changes state with current information
        this.setState({
            [e.target.name]:e.target.value
        })
    }

    render(){
        return(
            <div>
                <Form className =  "col-sm-8">
                    <Form.Group controlId="formBasicName">
                        <Form.Label>Username</Form.Label>
                        <Form.Control 
                            type="name" 
                            name = "username"
                            placeholder="username"
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

                    <Button 
                        variant="outline-secondary"
                        onClick = {(e) => this.handleLogin(e)}>
                        Login
                    </Button>
                    <p>
                        Register here <Link to = "/register">Register</Link>
                        <br/>
                        {this.state.loginCheck}
                    </p>

                </Form>
            </div>
        )
    }
}

export default Login;