import React from 'react'
import AppBar from 'material-ui/AppBar'
import Chip from 'material-ui/Chip'
import Avatar from 'material-ui/Avatar'
import IconButton from 'material-ui/IconButton'
import IconMenu from 'material-ui/IconMenu'
import MenuItem from 'material-ui/MenuItem'
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';


export default class Nav extends React.Component {
    constructor() {
        super()
    }

    render () {
        return (
            <AppBar 
                title="动力系实验管理平台"
                titleStyle={{ fontSize: "16px", fontWeight: "bold"}}
                showMenuIconButton={false}
                iconElementRight={
                    <span>
                        <Chip
                            onRequestDelete={() => {}}
                            style={{margin:".5em 1em", fontWeight: 'bold'}}
                        >
                            <Avatar size={32}  >A</Avatar>
                            木村拓哉
                        </Chip>
                    </span>
                    }
                style={{
                    position: 'fixed',
                    top: '0'
                }}
            />
        )
    }
}