import React, { Component } from "react";
import Cookies from "js-cookie"
import axios from "axios"


class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
        }
        
    }

    componentDidMount = () => {
        console.log("Home componentDidMount");
        this.props.checkLogin()
    };

    render() {
         return(
             <div>
                 <h1>
                     {console.log("Home Render")}
                     {console.log(this.props.username)}
                </h1>
                Home Page
             </div>
             
         )
    }
}


export default Home;