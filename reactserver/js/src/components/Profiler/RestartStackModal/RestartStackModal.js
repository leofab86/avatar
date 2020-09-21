import React from 'react';
import { useStore } from 'store';
import { turnOffStack, checkUserAndRestartStack } from 'actions/api'
import styles from './styles.scss';

export default function RestartStackModal () {
    const {closeModal, hydrateStore} = useStore();

    const reactivate = () => {
        checkUserAndRestartStack().then(user => hydrateStore.user(user));
        closeModal()
    };

    const turnOff = () => {
        turnOffStack().then(user => hydrateStore.user(user))
        closeModal()
    };

    return (
        <div className={styles.restartStackModal}>
            <h2>Your stack is deactivated</h2>
            <p>Your stack has timed out and is de-activated.</p>
            <p>Would you like to start a new application stack to profile?</p>
            <div className={styles.buttonContainer}>
                <button onClick={reactivate}>Re-activate</button>
                <button onClick={turnOff}>Keep off</button>
            </div>
        </div>
    )
}