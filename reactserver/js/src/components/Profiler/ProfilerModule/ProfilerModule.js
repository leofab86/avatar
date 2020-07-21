import React, {useState} from 'react'
import styles from './styles.scss'


export default function ProfilerModule ({ title, children }) {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className={styles.profilerModule}>
            <div onClick={() => setExpanded(!expanded)} className={styles.profilerModuleBar}>{title}</div>
            {expanded && (
                <div className={styles.profilerModuleChildContainer}>{children}</div>
            )}
        </div>
    )
}