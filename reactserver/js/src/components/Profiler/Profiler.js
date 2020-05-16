import React, { useState } from 'react';
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad } from 'actions/api';
import DataConfigModule from "./DataConfigModule";
import QueryOptimizationModule from "./QueryOptimizationModule";
import styles from './styles.scss';


export default function Profiler () {
    const {getFromStore} = useStore();
    const dbProfiles = getFromStore('db_profiles');
    const [selectedDbProfile, setSelectedDbProfile] = useState(dbProfiles?.[0]);

    useHydrateStoreOnPageLoad(!dbProfiles);

    return (
        <div className={styles.profilerContainer}>
            <h2 className={styles.profilerHeader}>Distributed System Profiler</h2>

            <p className={styles.profilerDescription}>
                Use this UI to configure a distributed system, then profile it under load
                and compare with other configurations to understand the nuances of setting up an efficient system.
            </p>

            <div className={styles.profilerModuleContainer}>
                <DataConfigModule
                    dbProfiles={dbProfiles}
                    selectedDbProfile={selectedDbProfile}
                    setSelectedDbProfile={setSelectedDbProfile}
                />

                <QueryOptimizationModule selectedDbProfile={selectedDbProfile}/>
            </div>
        </div>
    )
}