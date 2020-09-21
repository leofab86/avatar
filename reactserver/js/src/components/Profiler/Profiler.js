import React, { useState, useEffect } from 'react';
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad, checkUser, checkUserAndRestartStack } from 'actions/api';
import { useEffectOnUpdate } from 'utils/hooks';
import DataConfigModule from "./DataConfigModule";
import QueryOptimizationModule from "./QueryOptimizationModule";
import LoadTestModule from './LoadTestModule';
import LoginModal from './LoginModal';
import RestartStackModal from './RestartStackModal';
import CachingModule from "./CachingModule";
import MicroservicesModule from "./MicroservicesModule";
import styles from './styles.scss';

let checkInterval;

export default function Profiler () {
    const {getFromStore, openModal, hydrateStore} = useStore();
    const user = getFromStore('user');
    const dbProfiles = getFromStore('db_profiles');

    const [openModule, setOpen] = useState(null);
    const [selectedDbProfile, setSelectedDbProfile] = useState(dbProfiles?.[0]);

    useHydrateStoreOnPageLoad(!dbProfiles);

    useEffect(() => {
        if(!user) {
            openModal(<LoginModal/>)
        } else {
            checkUser().then(r => hydrateStore.user(r));
            return () => clearInterval(checkInterval)
        }
    }, []);

    useEffectOnUpdate(() => {
        function checkUserInterval () {
            checkUser().then(r => hydrateStore.user(r));
        }
        function reactToStatus (status) {
            if(status !== 'OFF') {
                if(status === 'DELETE_IN_PROGRESS' || status === 'DELETE_COMPLETE') {
                    openModal(<RestartStackModal/>)
                } else {
                    if(status === 'CHECKING') {
                        checkUserAndRestartStack().then(r => hydrateStore.user(r))
                    }
                    if(!checkInterval) {
                        checkInterval = setInterval(checkUserInterval,50000);
                    }
                }
            } else {
                clearInterval(checkInterval);
                checkInterval = null;
            }
        }
        reactToStatus(user.server_group_status);
    }, [user]);

    const restart = () => checkUserAndRestartStack().then(user => hydrateStore.user(user))

    let stackStatus = user ? user.server_group_status : <button onClick={() => openModal(<LoginModal/>)}>Please sign in</button>;
    stackStatus = user?.server_group_status === 'OFF' ? <span>Off <button onClick={restart}>Turn back on</button></span> : stackStatus;

    return (
        <div className={styles.profilerContainer}>
            <h2 className={styles.profilerHeader}>Avatar Profiler</h2>
            <h3 className={styles.stackStatus}>Stack Status: {stackStatus}</h3>

            <ul className={styles.profilerDescription}>
                <li>
                    Use each module below to configure various parts of the technology stack
                </li>
                <li>
                    The modules will explore different challenges engineers may face setting up these systems
                </li>
                <li>
                    Profile and observe live analytics of the applications in action
                </li>
            </ul>

            <div className={styles.profilerModuleContainer}>
                <DataConfigModule
                    isOpen={openModule === 'DataConfigModule'}
                    setOpen={isOpen => setOpen(isOpen ? null : 'DataConfigModule')}
                    dbProfiles={dbProfiles}
                    selectedDbProfile={selectedDbProfile}
                    setSelectedDbProfile={setSelectedDbProfile}
                />

                <QueryOptimizationModule
                    isOpen={openModule === 'QueryOptimizationModule'}
                    setOpen={isOpen => setOpen(isOpen ? null : 'QueryOptimizationModule')}
                    selectedDbProfile={selectedDbProfile}
                />

                <LoadTestModule
                    isOpen={openModule === 'LoadTestModule'}
                    setOpen={isOpen => setOpen(isOpen ? null : 'LoadTestModule')}
                    stackStatus={user?.server_group_status}
                    stackAddress={user?.server_group_address}
                />

                <CachingModule
                    isOpen={openModule === 'CachingModule'}
                    setOpen={isOpen => setOpen(isOpen ? null : 'CachingModule')}
                />

                <MicroservicesModule
                    isOpen={openModule === 'MicroservicesModule'}
                    setOpen={isOpen => setOpen(isOpen ? null : 'MicroservicesModule')}
                />
            </div>
        </div>
    )
}