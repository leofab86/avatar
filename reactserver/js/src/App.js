import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, StaticRouter, Switch, Route } from "react-router-dom";
import qs from 'query-string';
import Home from 'components/Home';
import DetailsPage from "components/DetailsPage";
import Profiler from "components/Profiler";
import GlobalModal from "components/GlobalModal";
import Preview from "components/Profiler/Preview/Preview"
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

                    <Route path='/profiler/preview/'>
                        {({ staticContext, location }) => {
                            const queryParams = staticContext?.query_params
                                ? staticContext.query_params
                                : qs.parse(location.search);
                            return (
                                <Preview
                                    spa={store.spa}
                                    withApi={queryParams.with_api === 'true'}
                                    dataSize={queryParams.data_size}
                                />
                            )
                        }}
                    </Route>


                </Switch>
            )}
            <GlobalModal />
        </StoreProvider>
    )
}

if(typeof window !== 'undefined'){
    const data = window.__data__ ? JSON.parse(window.__data__) : {};
    console.log(data);
    if(data.spa) {
        ReactDOM.render(<App store={data}/>, document.getElementById('root'))
    } else {
        ReactDOM.hydrate(<App store={data}/>, document.getElementById('root'));
    }
}
