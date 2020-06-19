import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, StaticRouter, Switch, Route } from "react-router-dom";
import Home from 'components/Home';
import DetailsPage from "components/DetailsPage";
import Profiler from "components/Profiler";
import LoadTest from "components/Profiler/LoadTest"
import GlobalModal from "components/GlobalModal";
import { StoreProvider } from 'store'


export default function App ({ store, staticRouterProps }) {

    const renderRouter = children =>
        staticRouterProps ? (
            <StaticRouter {...staticRouterProps}>{children}</StaticRouter>
        ) : (
            <BrowserRouter>{children}</BrowserRouter>
        );

    return (
        <StoreProvider store={store}>
            {renderRouter(
                <Switch>
                    <Route path='/' exact>
                        <Home />
                    </Route>

                    <Route path='/details/:projectId'>
                        <DetailsPage />
                    </Route>

                    <Route path='/profiler' exact>
                        <Profiler />
                    </Route>

                    <Route path='/profiler/load_test' exact>
                        <LoadTest />
                    </Route>
                </Switch>
            )}
            <GlobalModal />
        </StoreProvider>
    )
}

if(typeof window !== 'undefined'){
    const data = JSON.parse(window.__data__);
    console.log(data);
    ReactDOM.hydrate(<App store={data}/>, document.getElementById('root'));
}
