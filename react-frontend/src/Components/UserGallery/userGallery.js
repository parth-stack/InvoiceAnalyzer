import React from 'react'
import './style.css'
import Brick from '../UserCards/brick'
import Form from '../Form/form'

class UserGallery extends React.Component{

    constructor(props){
        super(props)
        this.state = {uploaded:null,invalid:null,vendor:null,amount:null}
        // this.fetchContent = this.fetchContent.bind(this);
    }

    fetchContent = () =>{
        const api = sessionStorage.getItem("api")
        const url = api +`/api/v1?query=status`
        
        var request = new XMLHttpRequest();
        request.open('GET', url, false);  // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
            let obj = JSON.parse(request.responseText)
            this.setState({uploaded:obj['uploaded'],invalid:obj['invalid'],vendor:obj['vendor'],amount:obj['amount']})
        }
    }

    deleteContent = () =>{
        const api = sessionStorage.getItem("api")
        const url = api +`/api/v1?query=clear`
        
        fetch(url, {method: "GET"}).then(response => {}).then(result => {window.location.reload()}
        ).catch(error => {console.log(error)})
    }

    componentDidMount(){
        this.fetchContent()
    }

    render = () =>{
        // console.log(this.state.data)
        return (
            <div>
                <div className="wallContainer">
                    <Brick heading="Uploaded" name={this.state.uploaded}/>
                    <Brick heading="Invalid" name={this.state.invalid}/>
                    <Brick heading="Vendors" name={this.state.vendor}/>
                    <Brick heading="Amount" name={this.state.amount}/>
                </div>
                <div className="formContainer">
                    <Form fetching={this.fetchContent}/>
                </div>
                <button className="addButton" onClick={this.deleteContent}>Delete Database</button>
            </div> 
        )
    }
}

export default UserGallery