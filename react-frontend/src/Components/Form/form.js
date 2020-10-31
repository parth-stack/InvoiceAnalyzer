import React from 'react';
import './style.css'
import { post } from 'axios';


class Form extends React.Component {

    constructor(props) {
        super(props);
        this.state = {selectedFile: null , table:null };
    }

    onFileChange = event => { 
        this.setState({selectedFile: event.target.files[0]}); 
    };

    onSubmit = (event) => {
        event.preventDefault() // Stop form submit
        
        const api = sessionStorage.getItem("api")
        const url = api +'/data';
        
        const formData = new FormData();
        formData.append('inputFile',this.state.selectedFile)
        const config = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }
        post(url, formData,config).then(
            (response)=>{this.setState({table:response.data});this.props.fetching();}
        )
    }

    render = () => {
        return (
            <div className="form-container">
                <p>---- Upload Invoices ----</p>
                <input
                    id="inputFile"
                    type="file" onChange={this.onFileChange} accept=".xls,.xlsx"/>
                <input
                    onClick={this.onSubmit}
                    className="submit-btn"
                    type="submit" />
                <div className="result" dangerouslySetInnerHTML={{ __html: this.state.table }} />
            </div>
        );
    }
}

export default Form;
