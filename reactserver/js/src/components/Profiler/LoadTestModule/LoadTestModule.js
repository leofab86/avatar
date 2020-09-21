import React, {useState, useLayoutEffect, useRef} from 'react';
import cn from 'classnames';
import { useStore } from 'store';
import { loadTestStart, loadTestCheck } from 'actions/api';
import ProfilerModule from 'components/Profiler/ProfilerModule/ProfilerModule';
import LearnMoreModal from 'components/LearnMoreModal';
import PageOptions from "./PageOptions";
import styles from './styles.scss'

const graphTimeMax = 5000;

export default function LoadTestModule ({ isOpen, setOpen, stackStatus, stackAddress }) {
    const [loadTestStatus, setLoading] = useState(false);
    const [pageType, setPageType] = useState('ssr');
    const [listSize, setListSize] = useState('small');
    const [withApi, setWithApi] = useState(false);
    const [graph, setGraph] = useState([]);
    const [highestAverage, setHighestAverage] = useState(0);
    const graphRef = useRef(null);

    const [ReactJson, setReactJson] = useState(null);

    const { openModal } = useStore();

    const openReactJsonModal = (json) => {
        function open (ReactJsonModule = ReactJson) {
            openModal(
                <ReactJsonModule
                    src={json}
                    theme="monokai"
                    name={'Request Batch'}
                    collapsed={false}
                    indentWidth={2}
                    groupArraysAfterLength={false}
                    displayObjectSize={true}
                    displayDataTypes={false}
                    enableClipboard={false}
                    shouldCollapse={({name}) => name !== 'Request Batch'}
                />,
                { reactJsonModal: true }
            );
        }
        if (!ReactJson) {
            import('react-json-view').then(ReactJsonModule => {
                setReactJson(() => ReactJsonModule.default)
                open(ReactJsonModule.default)
            })
        } else {
            open()
        }
    };


    const usesApi = withApi || pageType === 'spa';

    const previewConfigUrl = `${pageType}?data_size=${listSize !== 'none' ? `${listSize}&with_api=${pageType === 'spa' || withApi}` : 'none'}`;

    useLayoutEffect(() => {
        if(graphRef.current) {
            graphRef.current.scrollLeft = graphRef.current.scrollWidth
        }
    }, [graph])

    function checkProgress(testId, batchRequest) {
        setTimeout(() => {
            loadTestCheck(testId, batchRequest)
                .then(r => {
                    if(r.load_test.results.length) {
                        setLoading('running');
                        const { averageHtml, averageWithJs, averageWithCss, failures, instances } = calculateAverage(r.load_test.results[0])
                        setGraph(prevState => ([
                            ...prevState,
                            {requests: r.load_test.results[0], averageHtml, averageWithJs, averageWithCss, instances, failures}
                        ]));
                        const averageType = usesApi ? averageWithJs : averageWithCss;
                        setHighestAverage(prevAverage => {
                            if(averageType > graphTimeMax) return graphTimeMax;
                            return averageType > prevAverage ? averageType : prevAverage
                        })
                    }
                    if(r.load_test.results.length === 0) {
                        checkProgress(testId, batchRequest)
                    } else if(r.load_test.completion !== 100) {
                        checkProgress(testId, batchRequest + 1)
                    }
                })
        }, 1000)
    }

    function runLoadTest () {
        setLoading('Generating resources...');
        loadTestStart(stackAddress, previewConfigUrl)
            .then(r => {
                setLoading('Launching load test...');
                console.log('start: ', r);
                checkProgress(r.test_id, 1)
            })
    }

    function calculateAverage(arrayOfRequests) {
        let sum = 0;
        let sumWithJs = 0;
        let sumWithCss = 0;
        let failures = 0;
        const instances = [];
        arrayOfRequests.forEach(request => {
            if(!request.duration) failures++;
            sum = sum + (request.duration || 10000);
            sumWithJs = sumWithJs + (request.durationWithJs || 10000);
            sumWithCss = sumWithCss + (request.durationWithCss || 10000)
            if(!instances.includes(request.instance)) {
                instances.push(request.instance)
            }
        });
        return {
            averageHtml: Math.floor(sum/arrayOfRequests.length),
            averageWithJs: Math.floor(sumWithJs/arrayOfRequests.length),
            averageWithCss: Math.floor(sumWithCss/arrayOfRequests.length),
            instances,
            failures
        }
    }

    const loadTestLearnMore = () => openModal(
        <LearnMoreModal
            header={'Custom, Serverless Load Test'}
            content={
                <React.Fragment>
                    <p>
                        This load test is designed using
                        {' '}<a target='_blank' href='https://aws.amazon.com/lambda/'>AWS Lambda</a> and
                        {' '}<a target='_blank' href='https://aws.amazon.com/dynamodb/'>Dynamo DB</a>.
                    </p>
                    <p>
                        These are lightweight AWS services that cost very little and yet can handle just about any
                        functionality traditionally reserved for server instances. Lambda handles the code that you
                        want to run while Dynamo DB provides persistence.
                    </p>
                    <p>
                        By being serverless and automatically partitioning compute time as necessary, the developer
                        is saved the dev ops related responsibilities of setting up a server, keeping it running
                        smoothly and deploying an application. AWS does this for you, leaving the developer to focus on the code.
                    </p>
                    <p>
                        In this case, the AWS Lambda function simply sends out a burst of 42 https requests to a url
                        on your running stack. Once it gets back the html response, it sends out subsequent requests
                        for the css and js resources to simulate how a browser would interact with the html.
                        It records details about the requests and saves them on Dynamo DB, which
                        are then retrieved here to create the live graph.
                    </p>
                </React.Fragment>
            }
        />
    );

    return (
        <ProfilerModule title={'Auto Scale Load Test'} isOpen={isOpen} setOpen={setOpen} stackStatus={stackStatus}>
            <h3>Auto Scale Load Test</h3>

            <p>
                Now that we've optimized back-end querying, let's explore how to improve performance when under
                high traffic load.
            </p>

            <h3>Auto Scaling</h3>

            <p>
                An auto scaling setup through AWS is an efficient way to manage high traffic load.
                Below, you can configure what type of web-page to load test. Different configurations
                have different pros and cons for different business needs and these will affect server load times.
                Preview the page to get further details and profile the performance implications of your configuration.
            </p>
            <p>
                (NOTE: the first couple of hits to your server stack tend to be a little slow as there is some warming
                up the system needs to do. Just request a couple of Previews in quick succession to get more accurate
                load times)
            </p>
            <p>TODO: Make a few automatic requests when user first opens this module to warm it up for them</p>

            <div className={styles.pageOptionsContainer}>
                <h4 className={styles.pageOptionsHeader}>Select Page Type: </h4>
                <select value={pageType} onChange={e => setPageType(e.target.value)}>
                    <option value='ssr'>Server Side Rendering</option>
                    <option value='spa'>Single Page App</option>
                </select>

                <br/><br/>

                <PageOptions
                    ssr={pageType === 'ssr'}
                    setListSize={setListSize}
                    listSize={listSize}
                    setWithApi={setWithApi}
                    withApi={withApi}
                />

                <a
                    target='_blank'
                    href={`${stackAddress}/profiler/preview/${previewConfigUrl}`}
                >
                    <button className={styles.previewPageButton}>Preview Page</button>
                </a>
            </div>

            <p>
                Once you are ready you can launch the load test
                {' '}<span onClick={loadTestLearnMore} className={styles.learnMore}>(learn more about the custom load test app)</span>.
                You will see a real time graph of average request times per second. Each bar of the graph is clickable to
                get details about that batch of requests, such as the breakdown of timings for each request as it makes
                its way through the server.
            </p>

            <p>
                The auto scaling system stack responds to this burst of traffic by starting up 2 extra
                instances to help handle the load. This takes about 5 minutes for the system to trigger an alarm due
                to the high network traffic and spin up the new servers. So you will be able to see in real-time 5 minutes
                into the test as the request times drop once the system has scaled up.
            </p>

            <p>TODO: Find a way to streamline this experience, no one wants to wait 5 minutes!!</p>

            <p>
                Try hitting the Preview Page button a couple of times during the load test to experience what this high
                traffic feels like to the end user. Notice the slower response before the system has scaled up.
            </p>

            <button disabled={loadTestStatus} onClick={runLoadTest}>Start Load Test</button>

            {loadTestStatus && loadTestStatus !== 'running' && (
                <p>{loadTestStatus}</p>
            )}
            {loadTestStatus === 'running' && (
                <div ref={graphRef} className={styles.graph}>
                    {highestAverage !== 0 &&
                        graph.map((dataSet, i) =>
                            <div onClick={() => openReactJsonModal(dataSet)} key={i} className={styles.dataPoint} style={{
                                height: `${(usesApi ? dataSet.averageWithJs : dataSet.averageWithCss) / highestAverage * 240}px`
                            }}>
                                {dataSet.failures > 0 && (
                                    <div className={styles.failures} style={{
                                        height: `${dataSet.failures * 2}px`,
                                        top: '0'
                                    }} />
                                )}
                                <div className={cn(styles.dataPointPopup, styles.dataPointPopupHovered)}>
                                    {usesApi ? dataSet.averageWithJs : dataSet.averageWithCss}
                                </div>
                            </div>
                        )
                    }
                </div>
            )}
        </ProfilerModule>
    )
}