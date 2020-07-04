import React, {useState, useLayoutEffect, useRef} from 'react';
import { loadTestStart, loadTestCheck } from 'actions/api';
import styles from './styles.scss'


export default function LoadTest () {
    const [graph, setGraph] = useState([]);
    const [highestAverage, setHighestAverage] = useState(0);
    const graphRef = useRef(null);

    useLayoutEffect(() => {
        graphRef.current.scrollLeft = graphRef.current.scrollWidth
    }, [graph])

    function checkProgress(testId, batchRequest) {
        setTimeout(() => {
            loadTestCheck(testId, batchRequest)
                .then(r => {
                    if(r.load_test.results.length && batchRequest !== 'final') {
                        const average = calculateAverage(r.load_test.results[0])
                        setGraph(prevState => ([
                            ...prevState,
                            {requests: r.load_test.results[0], average}
                        ]));
                        setHighestAverage(prevAverage => {
                            return average > prevAverage ? average : prevAverage
                        })
                    }
                    if(r.load_test.results.length === 0) {
                        checkProgress(testId, batchRequest)
                    } else if(r.load_test.completion !== 100) {
                        checkProgress(testId, batchRequest + 1)
                    } else if (batchRequest !== 'final') {
                        checkProgress(testId, 'final')
                    }
                })
        }, 1000)

    }

    function runLoadTest () {
        loadTestStart()
            .then(r => {
                console.log('start: ', r);
                checkProgress(r.test_id, 1)
            })
    }

    function calculateAverage(arrayOfRequests) {
        let sum = 0
        arrayOfRequests.forEach(request => {
            sum = sum + request.duration
        })
        return Math.floor(sum/arrayOfRequests.length)
    }

    return (
        <div>
            <button onClick={runLoadTest}>Start Load Test</button>

            <div ref={graphRef} className={styles.graph}>
                {highestAverage !== 0 &&
                    graph.map((dataSet, i) =>
                        <div onClick={() => console.log(dataSet)} key={i} className={styles.dataPoint} style={{
                            height: `${dataSet.average / highestAverage * 240}px`
                        }}>
                            <div className={`${styles.dataPointPopup} ${styles.dataPointPopupHovered}`}>
                                {dataSet.average}
                            </div>
                        </div>
                    )
                }

            </div>
        </div>
    )
}