import React from 'react'

export default class Detail extends React.Component {
    constructor() {
        super()
        this.state = {
            user: {
                user_id: 1111,
                user_name: '木村拓哉'
            },
            experiment: {
                experiment_id: 1111,
                experiment_text: 'This is the experiment text',
                experiment_vidoe: 'This is the experiment video',
                experiment_flash: 'This is the experiment flash',
                experiment_extra: 'this is the experiment extra'
            }
        }
    }

    componentDidMount() {
        console.log(this.props)
    }

    render() {
        return (
            <div style={{marginTop: '150px'}}>
                <h2>This is Details</h2>
            </div>
        )
    }
}