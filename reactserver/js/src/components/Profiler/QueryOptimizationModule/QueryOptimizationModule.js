import React, {Fragment, useState, useEffect} from 'react';
import { getDatabaseProfile } from 'actions/api';
import ProfilerModule from 'components/Profiler/ProfilerModule/ProfilerModule';
import ReactJsonModal from "./ReactJsonModal";
import ChildDepthSection from "./ChildDepthSection";
import LoadingTimer from "./LoadingTimer";
import styles from './styles.scss';

let requestId;

export default function QueryOptimizationModule ({ selectedDbProfile }) {
    const [dbProfileJson, setJson] = useState(null);
    const [timerActive, setTimerActive] = useState(false);
    const [queryConfig, setQueryConfig] = useState({});

    useEffect(function resetJson_onConfigChange () {
        setJson(null);
        requestId = null;
        setTimerActive(false)
    }, [selectedDbProfile, queryConfig]);

    const getDbProfile = () => {
        setJson(null);
        setTimerActive(true);
        const timeStamp = Date.now();
        requestId = timeStamp;
        getDatabaseProfile(selectedDbProfile.db_profile_id, queryConfig)
            .then(json => {
                if (timeStamp === requestId) {
                    if (process.env.NODE_ENV === 'development') {
                        console.log(json);
                    }
                    setTimerActive(false);
                    setJson({...json.db_profile[0], timing_data: json.timing_data})
                }
            });
    };

    return (
        <ProfilerModule title={'Query Optimization'}>
            {!selectedDbProfile ? (
                <h3>Select or Create a DB Model</h3>
            ) : (
                <Fragment>
                    <h3>Query Optimization</h3>
                    <p>
                        Try the different query parameters below and observe how they affect the request time.
                    </p>

                    <h3 className={styles.selectedDbHeader}>Selected Database Model:</h3>
                    <h3 className={styles.selectedDbName}>== {selectedDbProfile.db_profile_name} ==</h3>
                    <span>
                        {selectedDbProfile &&
                            `( teachers: ${selectedDbProfile.teachers
                                }, classes: ${selectedDbProfile.classes
                                }, students: ${selectedDbProfile.students} )`
                        }
                    </span>

                    <ChildDepthSection setQueryConfig={setQueryConfig}/>

                    <div className={styles.requestRow}>
                        <button className={'profilerButton'} onClick={getDbProfile}>Request Data</button>
                        {' '}
                        Request time:
                        <LoadingTimer
                            timerActive={timerActive}
                            resetDependencies={[selectedDbProfile, queryConfig]}
                        />
                    </div>

                    {dbProfileJson && <ReactJsonModal dbProfileJson={dbProfileJson}/>}
                </Fragment>
            )}
        </ProfilerModule>
    )
}