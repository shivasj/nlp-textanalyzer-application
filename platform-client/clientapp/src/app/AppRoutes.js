import React from "react";
import { Route, Switch } from 'react-router-dom';
import Home from "../components/Home";
import Dashboard from "../components/Dashboard";
import ArticleSources from "../components/ArticleSources";
import Error404 from '../components/Error/404';


const AppRouter = ( props ) => {

    console.log("================================== AppRouter ======================================");

    return (
        <React.Fragment>
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/dashboard" exact component={Dashboard} />
                <Route path="/article_sources" exact component={ArticleSources} />
                <Route component={Error404} />
            </Switch>
        </React.Fragment>
    );
}

export default AppRouter;