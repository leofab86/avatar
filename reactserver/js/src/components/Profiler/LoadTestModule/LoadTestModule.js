import React, {useState, useLayoutEffect, useRef} from 'react';
import cn from 'classnames';
import { useStore } from 'store';
import { loadTestStart, loadTestCheck } from 'actions/api';
import ProfilerModule from 'components/Profiler/ProfilerModule/ProfilerModule';
import PageOptions from "./PageOptions";
import styles from './styles.scss'

const autoScaleSystemOrigin = 'http://monolith-auto-scale-test-network-6916b92cd9344764.elb.us-east-1.amazonaws.com';
const graphTimeMax = 5000;

export default function LoadTestModule () {
    const [loadTestStatus, setLoading] = useState(false);
    const [pageType, setPageType] = useState('ssr');
    const [listSize, setListSize] = useState('none');
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
                />
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
        loadTestStart(previewConfigUrl)
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

    return (
        <ProfilerModule title={'Auto Scale Load Test'}>
            <h3>Auto Scale Load Test</h3>

            <p>
                Now that we've optimized back-end querying, let's explore how to improve performance when under
                high traffic load.
            </p>

            <h3>Auto Scaling</h3>

            <p>
                An auto scaling setup through AWS is an efficient way to manage high traffic load. Especially when
                your business needs require bursts of high traffic as opposed to consistent loads on your system.
                Below, you can configure what type of web-page to load test. Different configurations
                have different pros and cons for different business needs and these will affect server load times.
                Preview the page to get further details and profile the performance implications of your configuration.
            </p>

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
                    href={`${autoScaleSystemOrigin}/profiler/preview/${previewConfigUrl}`}
                >
                    <button className={styles.previewPageButton}>Preview Page</button>
                </a>
            </div>

            <p>
                Once you are ready you can launch the load test. You will see a real time graph of average request
                times per second. Each bar of the graph is clickable to get details about that batch of requests, such
                as the breakdown of timings as the request makes its way through the server.
                (learn more about profiling server timings)
            </p>

            <p>
                To see the auto scaling system in action, the load test is 10 minutes long. The auto scaling system
                starts with one server instance, then as it recognizes the burst of traffic caused by the load test
                will scale up to 3 server instances. There is about a 5 minute delay before the 2 extra instances come
                online so you will be able to observe in real time in the graph as request times drop when they come online.
                (learn more about how the load test is built using AWS Lambda and DynamoDB architecture)
            </p>

            <p>
                You don't have to watch the load test for the whole 10 minutes! You can move on to the next module
                and come back to review the results later, or float the graph window so you can keep an eye
                on it as you explore the other modules.
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