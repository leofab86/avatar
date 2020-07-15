import React from 'react';
import styles from './styles.scss';


export default function ClassList ({ list }) {

    return (
        <div>
            <h1>Class List</h1>
            {list.map((schoolClass, i) =>
                <div className={styles.classCard} key={i}>
                    <p>Class Id: {schoolClass.class_id}</p>
                    <p>Subject: {schoolClass.class_type}</p>
                </div>
            )}
        </div>
    )
}