import React, {useRef} from 'react';
import { useStore } from 'store';
import { useClickOutside } from 'utils/hooks';
import styles from './styles.scss';


export default function GlobalModal () {
    const {getFromStore, closeModal} = useStore();
    const { Component } = getFromStore('modalState');
    const modalRef = useRef(null);

    useClickOutside({
        container: modalRef,
        handler: closeModal,
        listenerConditional: Component
    }, [Component]);

    return !Component ? null : (
        <div className={styles.globalModalOverlay}>
            <div className={styles.globalModal} ref={modalRef}>
                {Component}
            </div>
        </div>
    )
}