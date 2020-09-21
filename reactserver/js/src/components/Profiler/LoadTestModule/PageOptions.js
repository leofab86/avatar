import React from 'react';
import styles from "./styles.scss";


export default function PageOptions ({ssr, setListSize, listSize, setWithApi, withApi}) {
    const dataSizeConfig = {
        title: 'Data size',
        setter: setListSize,
        state: listSize,
        options: [
            // {label: 'Static Content (no data)', id: 'none_data_checkbox', activeCondition: 'none'},
            {label: 'Small List', id: 'small_data_checkbox', activeCondition: 'small'},
            {label: 'Large List', id: 'large_data_checkbox', activeCondition: 'large'},
        ]
    };
    const dataRetrievalConfig = {
        title: 'Data retrieval',
            setter: setWithApi,
            state: withApi,
            options: [
                {label: 'During server side rendering', id: 'without_api_checkbox', activeCondition: false},
                {label: 'Subsequent API call', id: 'with_api_checkbox', activeCondition: true},
            ]
    };
    const config = [dataSizeConfig];
    if(ssr && listSize !== 'none') {
        config.push(dataRetrievalConfig)
    }

    return (
        <div>
            {config.map(({title, setter, state, options}) =>
                <div key={title}>
                    <strong>{title}: </strong>
                    <br/>
                    <div className={styles.pageOptionsList}>
                        {options.map(({activeCondition, id, label}) =>
                            <div key={id}>
                                <input
                                    checked={state === activeCondition}
                                    onChange={() => setter(activeCondition)}
                                    className={styles.pageOptionCheckBox}
                                    type='checkbox'
                                    id={id}
                                />
                                <label className={styles.pageOptionLabel} htmlFor={id}>
                                    {label}
                                </label>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}