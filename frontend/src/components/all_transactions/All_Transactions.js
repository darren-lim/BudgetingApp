import React, { Component } from "react";
import {Link} from "react-router-dom"
import Cookies from "js-cookie"
import axios from "axios";

class All_Transactions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            transactions: []
        }

    }

    componentDidMount = () => {
        console.log("all transactions componentDidMount");
        this.props.checkLogin();
        axios.get(`/apiapi/all_transactions`)
          .then(res => {
            this.setState({
                transactions: res.data
            });
          })
            .catch(err=> {
                console.log("transaction get error: " + err)
            })
        console.log(this.state.transactions);
    };

    render() {
         return(
             <div>
                 <h1>
                     {console.log("transactions Render")}
                     {console.log(this.props.username)}
                      Transaction Page
                </h1>
                <ul>
                    {this.state.transactions.map((transaction) => (
                        <li key={transaction.id}>
                            {transaction.t_type}
                            <br/>
                            {transaction.amount}
                            <br/>
                            {transaction.source}
                            <br/>
                            {transaction.month}, {transaction.year}
                        </li>
                    ))}
                </ul>
             </div>

         )
    }
}


export default All_Transactions;