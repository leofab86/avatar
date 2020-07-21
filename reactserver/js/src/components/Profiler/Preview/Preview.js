import React, {useState, useLayoutEffect} from 'react';
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad } from 'actions/api'
import SchoolList from "./SchoolList";
import ClassList from "./ClassList";
import styles from './styles.scss'


export default function Preview ({ spa, withApi, dataSize }) {
    const {getFromStore} = useStore();
    const [perf, setPerf] = useState(null);

    const data = getFromStore(dataSize === 'small' ? 'db_profiles' : 'classes');

    if(withApi) {
        useHydrateStoreOnPageLoad(!data?.length)
    }

    useLayoutEffect(() => {
        if(data?.length && typeof performance !== 'undefined') {
            if(withApi) {
                setTimeout(() => {
                     performance.mark('data-paint')
                }, 10)
            }
            function checkPaints () {
                setTimeout(() => {
                    if(performance.getEntriesByName('first-paint').length) {
                        const perf = {
                            fcp: performance.getEntriesByName('first-paint')[0].startTime,
                        };
                        if(withApi) {
                            perf.fmp = performance.getEntriesByName('data-paint')[0].startTime
                        }
                        setPerf(perf)
                    } else {
                        checkPaints()
                    }
                }, 200)
            }
            checkPaints()
        }
    }, [data]);

    let content;

    if(dataSize === 'small') {
        content = <SchoolList list={data || []} />
    } else if(dataSize === 'large') {
        content = <ClassList list={data || []} />
    } else {
        content = <h2>Static Content</h2>
    }

    return (
        <div className={styles.previewContainer}>
            <div className={styles.previewDescription}>
                <h1>Preview</h1>

                <div>
                    <p><strong>Page Type: </strong>{spa ? 'Single Page App (SPA)' : 'Server Side Rendering (SSR)'}</p>
                    <p><strong>Data Size: </strong>{dataSize === 'none' ? 'Static content (no data)' : dataSize}</p>
                    {dataSize !== 'none' && (
                        <p>
                            <strong>Data Retrieval: </strong>
                            {withApi ? 'using subsequent API call' : 'during server side rendering'}
                        </p>
                    )}

                    {spa && (
                        <div>
                            <p>
                                Single Page App configurations return minimal html from the server and let the javascript
                                on the client do the work of rendering components. This means that the user experience is
                                delayed by the javascript bundle loading. This can be especially painful in cases where
                                the bundle is particularly large and where the connection and client platform isn't so
                                powerful.
                            </p>
                            <p>
                                The advantage of SPAs is that they cause less load on the server. The important metrics
                                for SPA are First Contentful Paint, which occurs after the javascript bundle is loaded,
                                and First Meaningful Paint, which occurs when the majority of the content is loaded if
                                the page is making an api call for data.
                            </p>

                        </div>
                    )}
                    {!spa && (
                        <div>
                            <p>
                                Server Side Rendering returns the page request with the fully formed html structure. This
                                is often perceived as a faster loading experience, though this can vary depending on
                                the content of the page. Another theoretical advantage of Server Side Rendering is it
                                can improve SEO in case search engine crawlers struggle with rendering javascript
                                applications, though signs point to this not being a serious concern anymore.
                            </p>
                            {!withApi && (
                                <p>
                                    For a server side rendered application that retrieves data
                                    on the server, the only metric necessary is First Contentful Paint, which is when
                                    the pre-rendered html from the original request is painted. The only things delaying
                                    this are the complexity of the data retrieval and the css. This configuration should
                                    generally provide the fastest time to fully rendered content.
                                </p>
                            )}
                            {withApi && (
                                <p>
                                    For a server side rendered application that retrieves data using an api call after
                                    initial load, there are two metrics, First Contentful Paint and First Meaningful Paint.
                                    First Contentful paint shows the time it takes to render the static content, usually
                                    the frame or container components. First Meaningful Paint indicates when the data
                                    from the api gets rendered. The advantage of this configuration is that it usually
                                    leads to the quickest first paint, since the server rendering only renders the simple
                                    static content and doesn't wait for data retrieval. The First Meaningful Paint has
                                    to wait for both the javascript bundle and the api call.
                                </p>
                            )}
                            <p>
                                The disadvantage with server side rendered pages is that it tends to be a greater load
                                on the server and increased system complexity, since the server is taking on some of the work
                                to render the html instead of letting the client do it.
                            </p>

                        </div>
                    )}

                    <br/>

                    {perf && (
                        <div>
                            {perf.fcp && <p><strong>First Contentful Paint:</strong> {perf.fcp}</p>}
                            {perf.fmp && <p><strong>First Meaningful Paint:</strong> {perf.fmp}</p>}
                        </div>
                    )}

                </div>
            </div>
            {content}
        </div>
    )

}