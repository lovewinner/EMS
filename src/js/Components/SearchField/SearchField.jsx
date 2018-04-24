import React from 'react'
import AutoComplete from 'material-ui/AutoComplete'

const colors = [
    'Red',
    'Orange',
    'Yellow',
    'Green',
    'Blue',
    'Purple',
    'Black',
    'White',
];

export default class SearchField extends React.Component {
    constructor() {
        super()
        this.state = {
            searchText: '',
        }
    }

    handleUpdateInput = (searchText) => {
        this.setState({
            searchText: searchText,
        });
    };

    handleNewRequest = () => {
        this.setState({
            searchText: '',
        });
    };

    render() {

        return (
            <div class="search_component">
                <i class="material-icons">search</i>
                <input type="text" 
                    placeholder="请输入实验名称的关键字..." 
                    style={{ borderBottom: "none!important"}}
                />
            </div>
        )
    }
}