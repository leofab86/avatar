import React, {useState, useEffect} from 'react';
import styles from './styles.scss'


export default function ChildDepthSection ({ setQueryConfig, resetJson }) {
    const [teacherLevels, setTeacherLevels] = useState(0);
    const [classLevels, setClassLevels] = useState(0);
    const [studentLevels, setStudentLevels] = useState(0);
    const [prefetchRelated, setPrefetchRelated] = useState(false);
    const [customOptimization, setCustomOptimization] = useState(false);

    useEffect(function setQueryConfig_onConfigChange () {
        setQueryConfig(prevState => ({
            ...prevState,
            'teacher_levels': teacherLevels,
            'class_levels': classLevels,
            'student_levels': studentLevels,
            'prefetch_related': prefetchRelated,
            'custom_optimization': customOptimization
        }))
    }, [teacherLevels, classLevels, studentLevels, prefetchRelated, customOptimization]);

    return (
        <div className={styles.childDepthSection}>
            <h4 className={styles.childDepthHeader}>Child Depth:</h4>

            <p>
                Select which pieces of data to retrieve with your query and how deeply to
                retrieve that data's children.
            </p>

            <div className={styles.selectColumn}>
                <span>
                    Teachers:
                    {' '}
                    <select value={teacherLevels} onChange={e => setTeacherLevels(e.target.value)}>
                        <option value={0}>Not Included</option>
                        <option value={1}>Only Teachers</option>
                        <option value={2}>Teachers with Classes</option>
                        <option value={3}>Teachers with Classes with Students</option>
                    </select>
                </span>
                <span>
                    Classes:
                    {' '}
                    <select value={classLevels} onChange={e => setClassLevels(e.target.value)}>
                        <option value={0}>Not Included</option>
                        <option value={1}>Only Classes</option>
                        <option value={2}>Classes with Students</option>
                        <option value={3}>Classes with Students with Classes</option>
                    </select>
                </span>
                <span>
                    Students:
                    {' '}
                    <select value={studentLevels} onChange={e => setStudentLevels(e.target.value)}>
                        <option value={0}>Not Included</option>
                        <option value={1}>Only Students</option>
                        <option value={2}>Students with Classes</option>
                        <option value={3}>Students with Classes with Students</option>
                    </select>
                </span>
            </div>

            <p>
                Retrieving nested hierarchical data using common abstractions like ORMs or frameworks without
                understanding how they structure their database queries can cause N+1 query problems
                (where a unique query is made for each of the children!)
            </p>
            <p>
                Try to do a request with 3 levels of depth for Classes data on a large data set to see how inefficient this is.
            </p>
            <p>
                You
                will be able to inspect the data after it returns. Note the "timing_data.queries" values. With a large
                data set and 3 levels of depth, the returned json can be around 4MB, which is not a trivial amount of
                data to query and serialize.
            </p>
            <p>
                Now try the Prefetch Related option below (this is an ORM configuration that reduces queries by getting
                related data all at once). Notice the improved time and inspect the "timing_data.queries" of the response to see how this
                changes.
            </p>
            <p>
                Finally, after extensive profiling, I discovered the biggest cause of the slow requests was actually a popular
                library that I was using to serialize my json responses. After switching to manual serialization I was able
                to cut down the request times dramatically. Try out Custom Optimization below with a maxed out data request.
            </p>
            <p>
                This exercise demonstrates the importance of profiling and being able to dig into the details of how
                common abstractions work, as sometimes even popular libraries and tools may do more harm than good.
            </p>

            <div className={styles.checkboxContainer}>
                <input
                    checked={prefetchRelated}
                    onChange={() => {setPrefetchRelated(!prefetchRelated); setCustomOptimization(false)}}
                    className={styles.optimizationCheckBox}
                    type='checkbox'
                    id='prefetch_related_checkbox'
                />
                <label className={styles.optimizationLabel} htmlFor='prefetch_related_checkbox'>
                    Prefetch Related
                </label>
            </div>

            <div className={styles.checkboxContainer}>
                <input
                    checked={customOptimization}
                    onChange={() => {setCustomOptimization(!customOptimization); setPrefetchRelated(false)}}
                    className={styles.optimizationCheckBox}
                    type='checkbox'
                    id='custom_optimization_checkbox'
                />
                <label className={styles.optimizationLabel} htmlFor='custom_optimization_checkbox'>
                    Custom Optimization
                </label>
            </div>


        </div>
    )
}