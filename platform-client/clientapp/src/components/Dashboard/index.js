import React, { useState, useEffect, useRef } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';

import DataServices from '../../services/DataServices';


const styles = theme => ({
    root: {
        flexGrow: 1,

    },
    grow: {
        flexGrow: 1,
    },
    main: {
        backgroundColor: "#f2f2f2",
        paddingLeft: theme.spacing(3),
        paddingRight: theme.spacing(3),
        paddingBottom: theme.spacing(2),
        paddingTop: 15,
        zIndex: theme.zIndex.drawer + 1,
    },
    gridContainer: {
        marginBottom: 10
    },
    chartContainer: {
        backgroundColor: "#ffffff",
    },
    datePickerContainer:{

    },
    dashboardToolbar :{
        backgroundColor: "#ffffff",
        marginBottom: 10,
    },
    pageTitle:{
        fontWeight: 800
    }
});

const Dashboard = ( props ) => {
    const {classes} = props;
    const { history } = props;
    
    console.log("================================== Dashboard ======================================");


    return (
        <div className={classes.root}>
            <main className={classes.main}>
                Dashboard comes here...
            </main>
        </div>
    );
};

export default withStyles( styles )( Dashboard );