import React, {useRef} from 'react';
import cn from 'classnames';
import { useStore } from 'store';
import { useClickOutside } from 'utils/hooks';
import styles from './styles.scss';


export default function GlobalModal () {
    const {getFromStore, closeModal} = useStore();
    const { Component, options } = getFromStore('modalState');
    const modalRef = useRef(null);

    const { reactJsonModal } = options;

    useClickOutside({
        container: modalRef,
        handler: closeModal,
        listenerConditional: Component
    }, [Component]);

    return !Component ? null : (
        <div className={styles.globalModalOverlay}>
            <div className={cn(styles.globalModal, reactJsonModal && styles.reactJsonModal)} ref={modalRef}>
                <span className={styles.close} onClick={closeModal}>X</span>
                {Component}
            </div>
        </div>
    )
}