import React, {useState, Fragment} from 'react';
import { useStore } from 'store';
import styles from "./styles.scss";


export default function ReactJsonModal ({ dbProfileJson }) {
    const [ReactJson, setReactJson] = useState(null);
    if (!ReactJson) {
        import('react-json-view').then(ReactJsonModule => {
            setReactJson(() => ReactJsonModule.default)
        })
    }
    const { openModal } = useStore();

    // TODO: bug where any item with same name is open as well. Need to create separate component for the openModal
    //  part that tracks first render and turns off shouldCollapse
    const shouldCollapse = ({name}) => name !== dbProfileJson.db_profile_name;

    const openReactJsonModal = () => openModal(
        <ReactJson
            src={dbProfileJson}
            theme="monokai"
            name={dbProfileJson.db_profile_name}
            collapsed={false}
            indentWidth={2}
            groupArraysAfterLength={false}
            displayObjectSize={true}
            displayDataTypes={false}
            enableClipboard={false}
            shouldCollapse={shouldCollapse}
        />
    );

    return !ReactJson ? null : (
        <Fragment>
            <h4 className={styles.reactJsonHeader}>Inspect the data:</h4>
            <div className={styles.reactJsonContainer}>
                <ReactJson
                    src={dbProfileJson}
                    theme="monokai"
                    name={dbProfileJson.db_profile_name}
                    collapsed={true}
                    indentWidth={2}
                    groupArraysAfterLength={false}
                    displayObjectSize={true}
                    displayDataTypes={false}
                    enableClipboard={false}
                />
                <div className={styles.reactJsonBlocker} onClick={openReactJsonModal}/>
            </div>
        </Fragment>
    )
}