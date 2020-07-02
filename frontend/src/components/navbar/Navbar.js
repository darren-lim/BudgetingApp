import React, { Component } from "react";
import {Link, withRouter} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Cookies from "js-cookie";

import "./Navbar.css"

class Navbar extends Component {
    constructor(props){
        super(props);
        this.state = {
        }

        this.handleLogout = this.handleLogout.bind(this)
    }

    handleLogout = () => {
        Cookies.remove("token")
        this.props.deleteLogin()
        this.props.history.push("/")

    }

    render(){
        return(
            <nav className = "navbar navbar-dark bg-dark navbar-expand-sm" >
                {console.log("Navbar Render")}
                <Link to = "/" className = "navbar-brand">Home</Link>
                <div className = "w-100">
                    <ul className = "navbar-nav ml-auto">
                        {this.props.isLoggedIn ?
                            <React.Fragment>
                                <li className = "navbar-item">
                                    <button className = "logoutButton"
                                            onClick = {() => this.handleLogout()}>
                                        Logout
                                    </button>
                                </li>
                            </React.Fragment>
                            :
                            <React.Fragment>
                                <li className = "navbar-item">
                                    <Link to = "/total" className = "nav-link" >
                                        Total
                                    </Link>
                                </li>
                                <li className = "navbar-item">
                                    <Link to = "/register" className = "nav-link" >
                                        Register
                                    </Link>
                                </li>
                                <li className = "navbar-item">
                                    <Link to = "/login" className = "nav-link">
                                        Login
                                    </Link>
                                </li>
                            </React.Fragment>
                        }
                    </ul>
                </div>
            </nav>
        )
    }

}

export default withRouter(Navbar);