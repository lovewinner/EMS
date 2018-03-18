import React from "react"

export default class Layout extends React.Component {
    constructor() {
        super();
        this.state = {
            title: "Welcome",
            name: "Jiarong"
        }
    }

    handleClick() {
        this.setState(prevState => ({
            name: "Alien"
        }));
    }

    render() {
        return (
            <div>

                <h1>{this.state.title}, 你好! {this.state.name}</h1>
                <button onClick={this.handleClick.bind(this)}>Click!</button>
            </div>
        );
    }
}
