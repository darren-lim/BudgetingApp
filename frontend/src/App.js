import React, { Component } from "react";
import { render } from "react-dom";

// Using HashRouter so reloading don't look into backend
import {HashRouter as Router, Route, Switch, Redirect} from "react-router-dom";

import './App.css';
import Navbar from "./components/navbar/Navbar";
import Home from "./components/home/Home";
import Login from "./components/login/Login"
import Register from "./components/register/Register"
import Cookies from "js-cookie"
import axios from "axios";


// Notes: Need to figure out how to login in before rendering components.
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      isLoggedIn: false,
    };
    this.nextPath     = this.nextPath.bind(this)
    this.setLogin     = this.setLogin.bind(this)
    this.deleteLogin  = this.deleteLogin.bind(this)
    this.checkLogin   = this.checkLogin.bind(this)
    
  }

  nextPath = (path) => {
    this.props.history.push(path);
  }

  setLogin = (res) => {
    this.setState({
      username: res.data.user.username,
      isLoggedIn: true
    })
  }

  deleteLogin = () => {
    this.setState({
      username:"",
      isLoggedIn: false
    })
  }

  checkLogin = () => {
    if (Cookies.get("token") && !this.state.isLoggedIn){
      axios.get("/api/auth/user", {headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${Cookies.get("token")}`
      }})
        .then(res => {
          this.setState({
            username:res.data.username,
            isLoggedIn:true
          })
          console.log("User has Logged In (App)")
        })
        .catch(err => {
          console.log("Checking Logged In Error" + err)
        })
    }
  }


  componentDidMount = () => {
    console.log("App componentDidMount")
    this.checkLogin()
  }



  render() {
    return (
      <Router>
        {console.log("App Render")}
        <Navbar
          {...this.props}
          isLoggedIn = {this.state.isLoggedIn}
          nextPath = {this.nextPath}
          deleteLogin = {this.deleteLogin}
           />
        <Switch>
          <Route exact path = "/" render = {props => (
              <Home {...props}
                username = {this.state.username}
                isLoggedIn = {this.state.isLoggedIn}
                checkLogin = {this.checkLogin}/>
            )}/>
          <Route path = "/register" render = {props => (
            <Register {...props} 
                      setLogin = {this.setLogin}
              />
          )} />
          <Route path = "/login" render = {props => (
            <Login {...props}
                    setLogin = {this.setLogin}
              />
          )} />
        </Switch>
      </Router>
    
      
    )}
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
