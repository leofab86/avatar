import React from 'react';
import styles from './styles.scss';


export default function ProgressBar ({ progress }) {
    return (
        <div className={styles.progressBar}>
            <div className={styles.progressBarFill} style={{ width: `${progress <= 5 ? 5 :progress}%` }}/>
        </div>
    )
}