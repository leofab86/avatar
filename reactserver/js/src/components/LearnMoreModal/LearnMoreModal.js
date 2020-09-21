import React from 'react';
import styles from './styles.scss';


export default function LearnMoreModal({ header, content }) {
    return (
        <div className={styles.container}>
            <h2 className={styles.header}>{header}</h2>
            {content}
        </div>
    )

}