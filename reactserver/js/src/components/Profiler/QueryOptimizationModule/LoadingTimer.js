import React, {useEffect} from 'react';
import { useTimer } from './hooks'
import styles from './styles.scss';

export default function LoadingTimer ({ timerActive, hideWhenZero, resetDependencies }) {
    const {time, setIsActive, reset} = useTimer();

    useEffect(function toggleTimer () {
        if(timerActive) reset();
        setIsActive(timerActive)
    }, [timerActive]);

    useEffect(function resetTimer () {
        reset();
    }, resetDependencies);

    return hideWhenZero && time === 0 ? null : (
        <span className={styles.timer}>{(time/1000).toFixed(1)} seconds</span>
    )
}