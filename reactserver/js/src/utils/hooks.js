import {useEffect, useRef} from 'react';

export function useClickOutside ({container, handler, listenerConditional = true}, dependencies) {
  useEffect(() => {
    if(listenerConditional) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, dependencies);
  function handleClickOutside (e) {
    if(!container.current.contains(e.target)) {
      handler()
    }
  }
}

export function useEffectOnUpdate(fn, inputs) {
  const didMountRef = useRef(false);

  useEffect(() => {
    if (didMountRef.current)
      fn();
    else
      didMountRef.current = true;
  }, inputs);
}