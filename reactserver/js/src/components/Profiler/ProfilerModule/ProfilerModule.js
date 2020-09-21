import React from 'react'
import { useStore } from 'store';
import { checkUserAndRestartStack } from 'actions/api';
import styles from './styles.scss'


export default function ProfilerModule ({ title, isOpen, setOpen, stackStatus, children }) {
    const {hydrateStore} = useStore();

    const restart = () => checkUserAndRestartStack().then(user => hydrateStore.user(user))

    let content;
    switch (stackStatus) {
        case 'OFF':
        case 'DELETE_IN_PROGRESS':
        case 'DELETE_COMPLETE':
            content = <p>This module requires your application stack to be running. <button onClick={restart}>Turn back on</button></p>;
            break;
        case 'CHECKING':
        case 'CREATE_IN_PROGRESS':
        case 'CREATE_COMPLETE':
            content = <p>Please wait, stack is coming online, waiting for READY state - Stack status: {stackStatus}</p>
            break;
        default:
            content = children
    }

    return (
        <div className={styles.profilerModule}>
            <div onClick={() => setOpen(isOpen)} className={styles.profilerModuleBar}>{title}</div>
            {isOpen && (
                <div className={styles.profilerModuleChildContainer}>
                    {content}
                </div>
            )}
        </div>
    )
}