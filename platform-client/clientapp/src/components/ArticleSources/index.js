import React, { useState, useEffect, useRef } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';
import Container from '@material-ui/core/Container';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Icon from '@material-ui/core/Icon';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import classNames from 'classnames';

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
    },
    formField:{
        marginBottom:20
    },
    bottomButtonControl:{
        paddingTop: 20,

    },
});

const ArticleSources = ( props ) => {
    const {classes} = props;
    const { history } = props;

    console.log("================================== Dashboard ======================================");

    // Component Data
    const [indexView, setindexView] = useState(true);
    const [isAdd, setIsAdd] = useState(true);
    const [reload, setReload] = useState(true);
    const [articleSourceList, setArticleSourceList] = useState(null);
    const [articleSource, setArticleSource] = useState({
        source:'',
        url:'',
        link_selector:'',
        time_selector:'',
        title_selector:'',
        content_selector:'',
        enabled:true,
    });

    // Load data
    useEffect(() => {
        DataServices.GetArticleSources()
            .then(function (response) {
                console.log(response);
                setArticleSourceList(response.data);
            })
    }, [indexView]);

    function AddArticleSource() {
        console.log("AddArticleSource...")
        setindexView(false);
        setIsAdd(true);
        setArticleSource({
            source:'',
            url:'',
            link_selector:'',
            time_selector:'',
            title_selector:'',
            content_selector:'',
            enabled:true,
        });
    }
    function CancelAddArticleSource() {
        setindexView(true);
        setArticleSource({
            source:'',
            url:'',
            link_selector:'',
            time_selector:'',
            title_selector:'',
            content_selector:'',
            enabled:true,
        });
    }
    function SaveArticleSource() {
        console.log(articleSource);

        DataServices.SaveArticleSource(articleSource)
            .then(function (response) {
                console.log(response.data);
            })

        setindexView(true);
    }
    function EditArticleSource(row) {
        setArticleSource(row);
        setindexView(false);
    }
    const UpdateField = e => {
        console.log(e.target.value)
        setArticleSource({
            ...articleSource,
            [e.target.name]: e.target.value
        });
    };
    
    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Toolbar variant="dense" className={classes.dashboardToolbar}>
                    <div></div>
                    <div className={classes.grow} />
                    <div>
                        <Button  className={classes.button} onClick={AddArticleSource}>
                            <Icon>add</Icon>
                            Add
                        </Button>
                    </div>
                </Toolbar>
                <Container maxWidth="md">
                    { indexView && (
                        <div style={{ backgroundColor: '#ffffff', height: '100vh' }}>
                            <Table className={classes.table}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Source</TableCell>
                                        <TableCell>URL</TableCell>
                                        <TableCell>Enabled</TableCell>
                                        <TableCell align="right"></TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {
                                        articleSourceList && articleSourceList.map((row,index) => (
                                            <TableRow key={index}>
                                                <TableCell component="th" scope="row">
                                                    {row.source}
                                                </TableCell>
                                                <TableCell>{row.url}</TableCell>
                                                <TableCell>{row.enabled?"True":"False"}</TableCell>
                                                <TableCell>
                                                    <Button className={classes.button} onClick={() => EditArticleSource(row)}>
                                                        <Icon>save</Icon>
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        ))
                                    }
                                </TableBody>
                            </Table>
                        </div>
                    ) }



                    { !indexView && (
                        <div style={{ backgroundColor: '#ffffff', height: '100vh', padding:20 }}>
                            <form noValidate autoComplete="off">
                                <TextField
                                    id="outlined-dense"
                                    label="Source"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="source"
                                    value={articleSource.source}
                                    onChange={UpdateField}
                                />
                                <TextField
                                    id="outlined-dense"
                                    label="URL"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="url"
                                    value={articleSource.url}
                                    onChange={UpdateField}
                                />
                                <TextField
                                    id="outlined-dense"
                                    label="Link Selector"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="link_selector"
                                    value={articleSource.link_selector}
                                    onChange={UpdateField}
                                />
                                <TextField
                                    id="outlined-dense"
                                    label="Time Selector"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="time_selector"
                                    value={articleSource.time_selector}
                                    onChange={UpdateField}
                                />
                                <TextField
                                    id="outlined-dense"
                                    label="Title Selector"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="title_selector"
                                    value={articleSource.title_selector}
                                    onChange={UpdateField}
                                />
                                <TextField
                                    id="outlined-dense"
                                    label="Content Selector"
                                    margin="dense"
                                    variant="outlined"
                                    fullWidth
                                    name="content_selector"
                                    value={articleSource.content_selector}
                                    onChange={UpdateField}
                                />
                                <FormControlLabel
                                    control={
                                        <Switch
                                            color="primary"
                                            name="enabled"
                                            value={articleSource.enabled}
                                            onChange={UpdateField}
                                        />
                                    }
                                    label="Enabled"
                                />
                            </form>
                            <div className={classes.bottomButtonControl}>
                                <Button color="primary" className={classes.button} onClick={SaveArticleSource}>
                                    <Icon>save</Icon>
                                    Save
                                </Button>
                                &nbsp;&nbsp;
                                <Button className={classes.button} onClick={CancelAddArticleSource}>
                                    <Icon>cancel</Icon>
                                    Cancel
                                </Button>
                            </div>
                        </div>
                    ) }
                </Container>
            </main>
        </div>
    );
};

export default withStyles( styles )( ArticleSources );