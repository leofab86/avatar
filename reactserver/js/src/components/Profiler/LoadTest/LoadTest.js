import React from 'react';
import { loadTestStart, loadTestCheck } from 'actions/api';


function checkProgress(testId) {
    setTimeout(() => {
        loadTestCheck(testId)
            .then(r => {
                console.log('check: ', r.load_test.completion)
                if(r.load_test.completion !== "100") {
                    checkProgress(testId)
                }
            })
    }, 1000)

}

function runLoadTest () {
    loadTestStart()
        .then(r => {
            console.log('start: ', r);
            checkProgress(r.test_id)
        })
}

export default function LoadTest () {

    return (
        <div>
            <button onClick={runLoadTest}>Start Load Test</button>
        </div>
    )
}