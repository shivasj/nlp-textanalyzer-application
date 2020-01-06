import React, {useEffect, useRef, useState} from 'react';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';

import moment from 'moment';
import _ from 'lodash';

import DataServices from "../../services/DataServices";


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
    cardHeader :{
        paddingBottom: 0,
    },
    cardContent :{
        paddingTop: 3,
    },
});

const Home = ( props ) => {
    const {classes} = props;
    const { history } = props;

    console.log("================================== Home ======================================");

    // Component Data
    const [day, setDay] = useState(0);
    const [hours, setHours] = useState(24);
    const [summarizeRatio, setSummarizeRatio] = useState(0.10);
    const [summarizeWordCount, setSummarizeWordCount] = useState(75);
    const [articles, setArticles] = useState(null);

    // Load data
    useEffect(() => {
        DataServices.GetArticles(day, hours, summarizeRatio, summarizeWordCount)
            .then(function (response) {
                console.log(response);
                setArticles(response.data);
            })
    }, [day,hours, summarizeRatio, summarizeWordCount]);


    function formatArticleContent(article_content,article_url) {

        article_content = article_content+ "&nbsp;<a target='_blank' href='"+article_url+"'>Read article...</a>"

        return article_content;
    }
    function displayDayButton(dayNum){
        let date  = moment(new Date()).subtract(dayNum,'days');

        return date.format("MMM-DD");
    }
    function formatDayButton(dayNum) {
        if(dayNum == day){
            return true;
        }else{
            return false;
        }
    }

    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Grid container spacing={3} className={classes.gridContainer}>
                    <Grid item md={12} xs={12} >
                        <Toolbar variant="dense" className={classes.dashboardToolbar}>
                            <div></div>
                            <div className={classes.grow} />
                            <div>
                                <ButtonGroup size="small" variant="text" aria-label="small outlined button group">
                                    <Button disabled={formatDayButton(0)} onClick={()=>setDay(0)}>{displayDayButton(0)}</Button>
                                    <Button disabled={formatDayButton(1)} onClick={()=>setDay(1)}>{displayDayButton(1)}</Button>
                                    <Button disabled={formatDayButton(2)} onClick={()=>setDay(2)}>{displayDayButton(2)}</Button>
                                    <Button disabled={formatDayButton(3)} onClick={()=>setDay(3)}>{displayDayButton(3)}</Button>
                                    <Button disabled={formatDayButton(4)} onClick={()=>setDay(4)}>{displayDayButton(4)}</Button>
                                </ButtonGroup>
                            </div>
                            <div>&nbsp;&nbsp;&nbsp;</div>
                            <div>
                                <TextField
                                    id="outlined-size-small"
                                    label="Word Count"
                                    variant="outlined"
                                    size="small"
                                    value={summarizeWordCount}
                                    onChange={(e)=>setSummarizeWordCount(e.target.value)}
                                />
                            </div>
                            <div>&nbsp;&nbsp;&nbsp;</div>
                            <div>
                                <TextField
                                    id="outlined-size-small"
                                    label="Ratio"
                                    variant="outlined"
                                    size="small"
                                    value={summarizeRatio}
                                    onChange={(e)=>setSummarizeRatio(e.target.value)}
                                />
                            </div>
                        </Toolbar>
                    </Grid>
                </Grid>

                <Grid container spacing={3} className={classes.gridContainer}>
                    <Grid item md={2} xs={12} >
                        Left Panel...
                    </Grid>
                    <Grid item md={10} xs={12} >

                        <Grid container spacing={2}>

                            {
                                articles && articles.map((row,index) => (
                                    <Grid item xs={4} key={index}>
                                        <Card className={classes.card}>
                                            <CardHeader
                                                title={row["article_title"]}
                                                subheader={moment.unix(row["article_dts"]).format("MMM-DD-YYYY")+' | '+row["source"]}
                                                className={classes.cardHeader}
                                            />
                                            <CardContent>
                                                <Typography variant="body2" color="textSecondary" component="span">
                                                    <div dangerouslySetInnerHTML={{ __html: formatArticleContent(row["article_content"],row["article_link"]) }} />
                                                </Typography>
                                            </CardContent>
                                        </Card>
                                    </Grid>
                                ))
                            }
                        </Grid>
                    </Grid>
                </Grid>
            </main>
        </div>
    );
};

export default withStyles( styles )( Home );